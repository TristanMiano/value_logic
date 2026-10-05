"""Prospective F14 ordinary-training neural probe.

This module separates discovery (``prepare_neural``) from evaluation
(``evaluate_neural``).  The caller must durably freeze the returned discovery
artifact before generating any evaluation examples.  Only development streams
are used by ``development_smoke``.  No expected-cost labels enter training.
"""
from __future__ import annotations

import copy
import hashlib
import json
import math
import time
from dataclasses import dataclass
from typing import Any

import numpy as np


STRATA = ("mixed_near", "mixed_far", "preserve_other", "equal_target", "scale_separating")
G_FAMILY = ("identity", "inv_eta", "inv_one_minus_eta", "inv_total_cost")
SEARCH_CONTROLS = ("aligned", "random", "permuted_concept", "shuffled_donor", "untrained")


def defaults() -> dict[str, Any]:
    """Complete prospective configuration; freeze a JSON copy in F14."""
    return {
        "dtype": "float64", "rng": "PCG64", "numpy_version": "2.3.5", "width": 32, "subset_size": 8,
        "training_steps": 3000, "batch_size": 256, "learning_rate": 0.003,
        "adam_beta1": 0.9, "adam_beta2": 0.999, "adam_epsilon": 1e-8,
        "fit_samples": 1024, "selection_pairs_per_stratum": 128,
        "evaluation_pairs_per_stratum": 8192, "task_evaluation_samples": 8192,
        "candidate_count": 128, "decoder_ridge": 1e-6,
        "proposal_uniform_mixture": 0.25, "ranking_tie_tolerance": 1e-12,
        "strata": list(STRATA), "g_family": list(G_FAMILY),
        "controls": list(SEARCH_CONTROLS),
        "global_scale_control": 2.0, "g_separation_min": 0.05,
        "g_min_separating_pairs": 256, "pair_attempt_multiplier": 4000,
        "pair_batch_size": 4096, "gauge_tolerance": 1e-10,
        "gauge_scale_min": 0.125, "gauge_scale_max": 8.0,
        "development_seed": 1400401, "development_evaluation_seed": 1400491,
        "model_seeds": [1500401, 1500402, 1500403, 1500404, 1500405],
        "evaluation_seeds": [1500491, 1500492, 1500493, 1500494, 1500495],
        "smoke": {"training_steps": 128, "fit_samples": 256,
                  "candidate_count": 8, "selection_pairs_per_stratum": 16,
                  "evaluation_pairs_per_stratum": 32,
                  "task_evaluation_samples": 256,
                  "g_min_separating_pairs": 8},
    }


def _cfg(config: dict[str, Any]) -> dict[str, Any]:
    return config.get("neural", config)


def validate_config(config: dict[str, Any]) -> dict[str, Any]:
    c = _cfg(config)
    if c["dtype"] != "float64" or c["rng"] != "PCG64" or not 0 < c["subset_size"] < c["width"]:
        raise ValueError("Require float64 and a nonempty proper hidden subset.")
    if c["subset_size"] > 8 or c["width"] != 32:
        raise ValueError("F14 freezes width 32 and at most eight coordinates.")
    if tuple(c["strata"]) != STRATA or tuple(c["g_family"]) != G_FAMILY:
        raise ValueError("Unregistered pair stratum or high-level hypothesis.")
    if tuple(c["controls"]) != SEARCH_CONTROLS:
        raise ValueError("All matched search controls are required.")
    positive = ("training_steps", "batch_size", "fit_samples", "candidate_count",
                "selection_pairs_per_stratum", "evaluation_pairs_per_stratum",
                "task_evaluation_samples", "pair_batch_size")
    if any(not isinstance(c[k], int) or c[k] <= 0 for k in positive):
        raise ValueError("Counts must be positive integers.")
    if not 0 <= c["proposal_uniform_mixture"] <= 1 or c["decoder_ridge"] <= 0:
        raise ValueError("Invalid proposal mixture or ridge coefficient.")
    if len(c["model_seeds"]) != len(c["evaluation_seeds"]):
        raise ValueError("Each model needs one prospectively paired evaluation seed.")
    streams = [c["development_seed"], c["development_evaluation_seed"],
               *c["model_seeds"], *c["evaluation_seeds"]]
    if len(set(streams)) != len(streams):
        raise ValueError("Development, discovery and evaluation seeds must be disjoint.")
    return c


def _rng(seed: int, stream: int = 0) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(np.random.SeedSequence([int(seed), int(stream)])))


def canonical_hash(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                                     allow_nan=False).encode("utf-8")).hexdigest()


def array_hash(*arrays: np.ndarray) -> str:
    digest = hashlib.sha256()
    for a in arrays:
        a = np.ascontiguousarray(a, dtype=np.float64)
        digest.update(json.dumps(list(a.shape), separators=(",", ":")).encode("ascii"))
        digest.update(a.tobytes())
    return digest.hexdigest()


def sigmoid(z: np.ndarray) -> np.ndarray:
    z = np.asarray(z, dtype=np.float64)
    e = np.exp(-np.abs(z))
    return np.where(z >= 0, 1 / (1 + e), e / (1 + e))


def eta(x: np.ndarray) -> np.ndarray:
    return 0.5 + (x[:, 0] + x[:, 1]) / 8


def action_costs(x: np.ndarray) -> np.ndarray:
    q = eta(x)
    return np.column_stack((x[:, 2] * q, x[:, 3] * (1 - q)))


def scale_values(x: np.ndarray, g_id: str) -> np.ndarray:
    if g_id == "identity":
        return np.ones(len(x))
    if g_id == "inv_eta":
        return 1 / eta(x)
    if g_id == "inv_one_minus_eta":
        return 1 / (1 - eta(x))
    if g_id == "inv_total_cost":
        return 1 / action_costs(x).sum(axis=1)
    raise ValueError(f"Unknown high-level scale: {g_id}")


def concepts(x: np.ndarray, g_id: str = "identity") -> np.ndarray:
    return action_costs(x) * scale_values(x, g_id)[:, None]


def optimal_probability(x: np.ndarray) -> np.ndarray:
    j = action_costs(x)
    return j[:, 0] / j.sum(axis=1)


def high_prediction(base: np.ndarray, donor: np.ndarray, role: int,
                    g_id: str = "identity") -> np.ndarray:
    if role not in (0, 1):
        raise ValueError("Cost role is zero or one.")
    b, d = concepts(base, g_id), concepts(donor, g_id)
    return d[:, 0] / (d[:, 0] + b[:, 1]) if role == 0 else b[:, 0] / (b[:, 0] + d[:, 1])


def sample_inputs(rng: np.random.Generator, n: int) -> np.ndarray:
    return np.column_stack((rng.uniform(-1, 1, (n, 2)), rng.uniform(0.5, 2, (n, 2))))


def training_batch(rng: np.random.Generator, n: int) -> tuple[np.ndarray, np.ndarray]:
    x = sample_inputs(rng, n)
    # These binary stochastic outcomes are the ONLY network training labels.
    y = (rng.random(n) < eta(x)).astype(np.float64)
    return x, y


@dataclass
class MLP:
    w: np.ndarray
    b: np.ndarray
    v: np.ndarray
    beta: float

    @classmethod
    def initialize(cls, width: int, rng: np.random.Generator) -> "MLP":
        return cls(rng.normal(0, math.sqrt(2 / 4), (4, width)), np.zeros(width),
                   rng.normal(0, 1 / math.sqrt(width), width), 0.0)

    def hidden(self, x: np.ndarray) -> np.ndarray:
        return np.maximum(np.asarray(x, dtype=np.float64) @ self.w + self.b, 0)

    def probability(self, x: np.ndarray) -> np.ndarray:
        return sigmoid(self.hidden(x) @ self.v + self.beta)

    def to_dict(self) -> dict[str, Any]:
        return {"w": self.w.tolist(), "b": self.b.tolist(),
                "v": self.v.tolist(), "beta": float(self.beta)}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "MLP":
        return cls(np.array(data["w"], dtype=np.float64),
                   np.array(data["b"], dtype=np.float64),
                   np.array(data["v"], dtype=np.float64), float(data["beta"]))

    def gauge(self, permutation: np.ndarray, scales: np.ndarray) -> "MLP":
        n = len(self.v)
        if sorted(permutation.tolist()) != list(range(n)) or np.any(scales <= 0):
            raise ValueError("Gauge requires a permutation and strictly positive scales.")
        return MLP(self.w[:, permutation] * scales, self.b[permutation] * scales,
                   self.v[permutation] / scales, self.beta)


def loss_and_gradients(net: MLP, x: np.ndarray, y: np.ndarray):
    pre = x @ net.w + net.b
    h = np.maximum(pre, 0)
    z = h @ net.v + net.beta
    weights = x[:, 2] * y + x[:, 3] * (1 - y)
    loss = float(np.mean(weights * (np.logaddexp(0, z) - y * z)))
    dz = weights * (sigmoid(z) - y) / len(x)
    dh = dz[:, None] * net.v * (pre > 0)
    return loss, [x.T @ dh, dh.sum(axis=0), h.T @ dz, np.array(dz.sum())]


def train_network(config: dict[str, Any], seed: int, training_steps: int | None = None):
    c = validate_config(config)
    steps = c["training_steps"] if training_steps is None else training_steps
    if not isinstance(steps, int) or steps <= 0:
        raise ValueError("Training steps must be positive.")
    net = MLP.initialize(c["width"], _rng(seed, 0))
    initial = copy.deepcopy(net)
    rng = _rng(seed, 1)
    pars = [net.w, net.b, net.v, np.array(net.beta)]
    first = [np.zeros_like(p) for p in pars]
    second = [np.zeros_like(p) for p in pars]
    losses = []
    started_wall, started_cpu = time.perf_counter(), time.process_time()
    for step in range(1, steps + 1):
        x, y = training_batch(rng, c["batch_size"])
        loss, grad = loss_and_gradients(net, x, y)
        if not math.isfinite(loss) or any(not np.isfinite(g).all() for g in grad):
            raise FloatingPointError(f"Nonfinite ordinary training at step {step}")
        for i in range(4):
            first[i] *= c["adam_beta1"]
            first[i] += (1 - c["adam_beta1"]) * grad[i]
            second[i] *= c["adam_beta2"]
            second[i] += (1 - c["adam_beta2"]) * grad[i] ** 2
            m = first[i] / (1 - c["adam_beta1"] ** step)
            v = second[i] / (1 - c["adam_beta2"] ** step)
            pars[i] -= c["learning_rate"] * m / (np.sqrt(v) + c["adam_epsilon"])
        net.beta = float(pars[3])
        if step > steps - 64:
            losses.append(loss)
    resource = {"steps": steps, "batch_size": c["batch_size"],
                "stochastic_outcome_labels": steps * c["batch_size"],
                "expected_cost_training_labels": 0,
                "parameter_count": int(net.w.size + net.b.size + net.v.size + 1),
                "parameter_bytes": int(net.w.nbytes + net.b.nbytes + net.v.nbytes + 8),
                "last_at_most_64_mean_weighted_bce": float(np.mean(losses)),
                "wall_seconds": time.perf_counter() - started_wall,
                "cpu_seconds": time.process_time() - started_cpu}
    return net, initial, resource


def make_pairs(config: dict[str, Any], seed: int, n: int, role: int,
               stream: int = 0) -> tuple[dict[str, tuple[np.ndarray, np.ndarray]], dict[str, Any]]:
    """Independent strata; no discarding of examples based on model predictions."""
    c = _cfg(config)
    result, generation = {}, {}
    for index, stratum in enumerate(STRATA):
        rng = _rng(seed, stream + index)
        bases, donors, accepted, attempted = [], [], 0, 0
        while accepted < n:
            k = min(c["pair_batch_size"], n * c["pair_attempt_multiplier"] - attempted)
            if k <= 0:
                raise RuntimeError(f"Pair generator exhausted frozen budget: {role}/{stratum}")
            b, d = sample_inputs(rng, k), sample_inputs(rng, k)
            jb = action_costs(b)
            if stratum in ("preserve_other", "equal_target"):
                fixed = 1 - role if stratum == "preserve_other" else role
                factor = eta(d) if fixed == 0 else 1 - eta(d)
                d[:, 2 + fixed] = jb[:, fixed] / factor
            jd = action_costs(d)
            pb, pd = optimal_probability(b), optimal_probability(d)
            ph = high_prediction(b, d, role)
            valid = np.all((d[:, 2:] >= 0.5) & (d[:, 2:] <= 2), axis=1)
            if stratum == "mixed_near":
                valid &= (np.abs(ph - 0.5) <= 0.04) & (np.abs(ph - pb) >= 0.05) & (np.abs(ph - pd) >= 0.05)
            elif stratum == "mixed_far":
                valid &= (np.abs(ph - 0.5) >= 0.15) & (np.abs(ph - pb) >= 0.05) & (np.abs(ph - pd) >= 0.05)
            elif stratum == "preserve_other":
                valid &= (np.abs(eta(d) - eta(b)) >= 0.08) & (np.abs(jd[:, role] - jb[:, role]) >= 0.1)
            elif stratum == "equal_target":
                valid &= (np.abs(eta(d) - eta(b)) >= 0.08) & (np.abs(jd[:, 1 - role] - jb[:, 1 - role]) >= 0.1)
            else:
                separation = np.min(np.column_stack([np.abs(high_prediction(b, d, role, g) - ph)
                                                      for g in G_FAMILY[1:]]), axis=1)
                valid &= (separation >= c["g_separation_min"]) & (np.abs(ph - pb) >= 0.05) & (np.abs(ph - pd) >= 0.025)
            selected = np.flatnonzero(valid)[:n - accepted]
            bases.append(b[selected])
            donors.append(d[selected])
            accepted += len(selected)
            attempted += k
        result[stratum] = (np.vstack(bases), np.vstack(donors))
        generation[stratum] = {"accepted": accepted, "proposals_generated": attempted}
    return result, generation


def _stack_pairs(pairs):
    return np.vstack([pairs[s][0] for s in STRATA]), np.vstack([pairs[s][1] for s in STRATA])


def fit_decoder(hidden: np.ndarray, targets: np.ndarray, subset: list[int], ridge: float):
    h = hidden[:, subset]
    mean, scale = h.mean(axis=0), h.std(axis=0)
    scale = np.where(scale > 1e-12, scale, 1.0)
    design = np.column_stack((np.ones(len(h)), (h - mean) / scale))
    gram = design.T @ design / len(h)
    penalty = np.eye(len(subset) + 1) * ridge
    penalty[0, 0] = 0
    beta = np.linalg.solve(gram + penalty, design.T @ targets / len(h))
    coefficient = beta[1:] / scale
    intercept = float(beta[0] - mean @ coefficient)
    pred = h @ coefficient + intercept
    nmse = float(np.mean((pred - targets) ** 2) / max(np.var(targets), 1e-12))
    return {"subset": subset, "coefficient": coefficient.tolist(), "intercept": intercept}, nmse


def decode(hidden: np.ndarray, decoder: dict[str, Any]):
    return hidden[:, decoder["subset"]] @ np.array(decoder["coefficient"]) + decoder["intercept"]


def candidate_pool(hidden: np.ndarray, target: np.ndarray, config: dict[str, Any],
                   seed: int, control: str, role: int):
    c = _cfg(config)
    rng = _rng(seed, 50 + role)
    hc, yc = hidden - hidden.mean(axis=0), target - target.mean()
    denom = np.sqrt(np.sum(hc ** 2, axis=0) * np.sum(yc ** 2))
    corr = np.divide(np.abs(hc.T @ yc), denom, out=np.zeros(hidden.shape[1]), where=denom > 1e-12)
    fraction = c["proposal_uniform_mixture"]
    weights = fraction / hidden.shape[1] + (1 - fraction) * (corr + 1e-12) / np.sum(corr + 1e-12)
    k, count = c["subset_size"], c["candidate_count"]
    pool = []
    if control != "random":
        pool.append(sorted(np.argsort(-corr, kind="stable")[:k].tolist()))
    while len(pool) < count:
        # A duplicate proposal consumes its budget; no hidden resampling credit.
        subset = sorted(rng.choice(hidden.shape[1], size=k, replace=False,
                                   p=None if control == "random" else weights).tolist())
        pool.append(subset)
    return pool


def _swap_probabilities(net: MLP, hb: np.ndarray, hd: np.ndarray, subset: list[int]):
    return sigmoid(hb @ net.v + net.beta + (hd[:, subset] - hb[:, subset]) @ net.v[subset])


def _choose_candidate(scores: list[dict[str, float]], tolerance: float) -> int:
    # Lexicographic comparison after a predeclared numerical tie band. Primary
    # is actual interchanged-probability MSE, not baseline-adjusted agreement.
    best = 0
    keys = ("probability_mse", "effect_mse", "decoder_nmse")
    for index in range(1, len(scores)):
        for key in keys:
            delta = scores[index][key] - scores[best][key]
            if abs(delta) <= tolerance:
                continue
            if delta < 0:
                best = index
            break
    return best


def search_alignment(net: MLP, config: dict[str, Any], seed: int, g_id: str,
                     control: str, inputs: np.ndarray, pairs_by_role, wrong_pairs_by_role):
    c = _cfg(config)
    h = net.hidden(inputs)
    target = concepts(inputs, g_id)
    if control == "permuted_concept":
        target = target[_rng(seed, 61).permutation(len(target))]
    alignment = {"g_id": g_id, "control": control, "roles": []}
    for role in (0, 1):
        b, d = _stack_pairs(pairs_by_role[role])
        hb, hd = net.hidden(b), net.hidden(d)
        if control == "shuffled_donor":
            # Independent wrong donors from the same stratum marginal preserve
            # independent evaluation rows. A global permutation would not.
            _, wrong = _stack_pairs(wrong_pairs_by_role[role])
            hd = net.hidden(wrong)
        ph, pb = high_prediction(b, d, role, g_id), optimal_probability(b)
        pnet = sigmoid(hb @ net.v + net.beta)
        pool = candidate_pool(h, target[:, role], c, seed, control, role)
        scores, decoders = [], []
        for subset in pool:
            decoder, nmse = fit_decoder(h, target[:, role], subset, c["decoder_ridge"])
            pint = _swap_probabilities(net, hb, hd, subset)
            scores.append({"probability_mse": float(np.mean((pint - ph) ** 2)),
                           "effect_mse": float(np.mean(((pint - pnet) - (ph - pb)) ** 2)),
                           "decoder_nmse": nmse})
            decoders.append(decoder)
        index = _choose_candidate(scores, c["ranking_tie_tolerance"])
        contribution = h[:, pool[index]] @ net.v[pool[index]]
        log_target = (1 if role == 0 else -1) * np.log(concepts(inputs, g_id)[:, role])
        alignment["roles"].append({"role": role, "selected_index": index,
                                    "subset": pool[index], "decoder": decoders[index],
                                    "candidate_pool": pool, "candidate_scores": scores,
                                    "selection_score": scores[index],
                                    "log_contribution_offset": float(np.mean(contribution - log_target)),
                                    "candidate_evaluations": len(pool), "decoder_fits": len(pool),
                                    "selection_pair_evaluations": len(pool) * len(b)})
    alignment["overlap"] = sorted(set(alignment["roles"][0]["subset"]) & set(alignment["roles"][1]["subset"]))
    alignment["mean_selection_probability_mse"] = float(np.mean([r["selection_score"]["probability_mse"] for r in alignment["roles"]]))
    return alignment


def prepare_neural(config: dict[str, Any], seed: int,
                   training_steps: int | None = None) -> dict[str, Any]:
    """Train and discover using one discovery seed. Never generate eval data."""
    c = validate_config(config)
    started_wall, started_cpu = time.perf_counter(), time.process_time()
    net, initial, training = train_network(c, seed, training_steps)
    inputs = sample_inputs(_rng(seed, 10), c["fit_samples"])
    pairs, generation, wrong_pairs, wrong_generation = [], [], [], []
    for role in (0, 1):
        p, resource = make_pairs(c, seed, c["selection_pairs_per_stratum"], role, 100 + 10 * role)
        pairs.append(p)
        generation.append(resource)
        wrong, wrong_resource = make_pairs(c, seed, c["selection_pairs_per_stratum"], role, 130 + 10 * role)
        wrong_pairs.append(wrong)
        wrong_generation.append(wrong_resource)
    alignments = {}
    for g_id in G_FAMILY:
        for control in SEARCH_CONTROLS:
            selected_net = initial if control == "untrained" else net
            alignments[f"{g_id}/{control}"] = search_alignment(selected_net, c, seed, g_id, control, inputs, pairs, wrong_pairs)
    # The competing family has three searches; its aggregate budget is reported.
    # Select the alternative once on discovery data, never by evaluation scores.
    selected_alternative = min(G_FAMILY[1:], key=lambda g: (alignments[f"{g}/aligned"]["mean_selection_probability_mse"], G_FAMILY.index(g)))
    result = {"schema": "f14-neural-discovery-v1", "discovery_seed": seed,
              "config_hash": canonical_hash(c), "config": copy.deepcopy(c),
              "network": net.to_dict(), "untrained_network": initial.to_dict(),
              "training": training, "alignments": alignments,
              "selected_alternative": selected_alternative,
              "selection_pair_generation": generation,
              "wrong_donor_generation": wrong_generation,
              "selection_data_hashes": {"decoder_inputs": array_hash(inputs),
                  "role_pairs": [array_hash(*_stack_pairs(p)) for p in pairs],
                  "wrong_donor_role_pairs": [array_hash(*_stack_pairs(p)) for p in wrong_pairs]},
              "evaluation_generated": False,
              "resource": {"hypotheses": len(G_FAMILY), "controls_per_hypothesis": len(SEARCH_CONTROLS),
                           "role_searches": len(G_FAMILY) * len(SEARCH_CONTROLS) * 2,
                           "candidate_evaluations": len(G_FAMILY) * len(SEARCH_CONTROLS) * 2 * c["candidate_count"],
                           "decoder_fits": len(G_FAMILY) * len(SEARCH_CONTROLS) * 2 * c["candidate_count"],
                           "input_hidden_forward_examples_per_search": c["fit_samples"] + 4 * len(STRATA) * c["selection_pairs_per_stratum"],
                           "additional_wrong_donor_hidden_examples": len(G_FAMILY) * 2 * len(STRATA) * c["selection_pairs_per_stratum"],
                           "selection_pair_evaluations": len(G_FAMILY) * len(SEARCH_CONTROLS) * 2 * c["candidate_count"] * len(STRATA) * c["selection_pairs_per_stratum"],
                           "alternative_family_search_multiplier": len(G_FAMILY) - 1,
                           "wall_seconds": time.perf_counter() - started_wall,
                           "cpu_seconds": time.process_time() - started_cpu}}
    result["artifact_hash"] = canonical_hash(result)
    return result


def transport_alignment(alignment: dict[str, Any], permutation: np.ndarray,
                        scales: np.ndarray) -> dict[str, Any]:
    """Transport selected coordinates/decoder; no fitting or searching."""
    result = copy.deepcopy(alignment)
    inverse = {int(old): new for new, old in enumerate(permutation)}
    for role in result["roles"]:
        old = role["subset"]
        role["subset"] = [inverse[i] for i in old]
        decoder = role["decoder"]
        new_subset = [inverse[i] for i in decoder["subset"]]
        decoder["coefficient"] = [float(a / scales[j]) for a, j in zip(decoder["coefficient"], new_subset)]
        decoder["subset"] = new_subset
    result["overlap"] = sorted(set(result["roles"][0]["subset"]) & set(result["roles"][1]["subset"]))
    return result


def _basic_error(actual: np.ndarray, expected: np.ndarray):
    error = actual - expected
    return {"n": len(error), "mae": float(np.mean(np.abs(error))),
            "mse": float(np.mean(error ** 2)), "rmse": float(np.sqrt(np.mean(error ** 2))),
            "max_absolute_error": float(np.max(np.abs(error))),
            "decision_agreement": float(np.mean((actual >= 0.5) == (expected >= 0.5)))}


def unused_duplicate_witness() -> dict[str, Any]:
    """F04 W7 constructed method check, never a trained-network result."""
    x = np.linspace(0.1, 2.0, 64)[:, None]
    net = MLP(np.ones((1, 2)), np.zeros(2), np.array([1.0, 0.0]), 0.0)
    h = net.hidden(x)
    # Exact decoder for either duplicate. W7 uses affine logit/output, not sigmoid.
    decoder_error = float(np.max(np.abs(h[:, 1] - x[:, 0])))
    donor = h[::-1]
    unused_effect = (donor[:, 1] - h[:, 1]) * net.v[1]
    used_effect = (donor[:, 0] - h[:, 0]) * net.v[0]
    return {"evidence": "constructed F04 W7 method validation", "decoder_max_error": decoder_error,
            "unused_logit_effect_max": float(np.max(np.abs(unused_effect))),
            "used_logit_effect_max": float(np.max(np.abs(used_effect))),
            "decoding_passes_and_unused_causal_use_fails": bool(decoder_error == 0 and np.all(unused_effect == 0) and np.max(np.abs(used_effect)) > 0)}


def _evaluate_alignment(net: MLP, alignment, pairs_by_role, wrong_pairs_by_role, config, seed):
    c = _cfg(config)
    result = {"g_id": alignment["g_id"], "control": alignment["control"],
              "overlap": alignment["overlap"], "roles": []}
    raw = {}
    for role in (0, 1):
        role_results, raw[role] = {}, {}
        for si, stratum in enumerate(STRATA):
            b, d = pairs_by_role[role][stratum]
            hb, hd = net.hidden(b), net.hidden(d)
            if alignment["control"] == "shuffled_donor":
                hd = net.hidden(wrong_pairs_by_role[role][stratum][1])
            subset = alignment["roles"][role]["subset"]
            pint = _swap_probabilities(net, hb, hd, subset)
            pb_net = sigmoid(hb @ net.v + net.beta)
            ph = high_prediction(b, d, role, alignment["g_id"])
            pb = optimal_probability(b)
            mixed = hb.copy()
            mixed[:, subset] = hd[:, subset]
            expected_concept = concepts(b, alignment["g_id"])
            expected_concept[:, role] = concepts(d, alignment["g_id"])[:, role]
            decoded = np.column_stack([decode(mixed, r["decoder"]) for r in alignment["roles"]])
            normalizer = np.maximum(np.std(concepts(b, alignment["g_id"]), axis=0), 1e-12)
            metrics = _basic_error(pint, ph)
            metrics["base_prediction"] = _basic_error(pb_net, pb)
            metrics["adjusted_effect_rmse"] = float(np.sqrt(np.mean(((pint - pb_net) - (ph - pb)) ** 2)))
            metrics["expected_effect_rms"] = float(np.sqrt(np.mean((ph - pb) ** 2)))
            metrics["observed_effect_rms"] = float(np.sqrt(np.mean((pint - pb_net) ** 2)))
            metrics["unchanged_target_output_effect_rms"] = float(np.sqrt(np.mean((pint - pb_net) ** 2))) if stratum == "equal_target" and alignment["g_id"] == "identity" else None
            metrics["target_decoder_nrmse"] = float(np.sqrt(np.mean((decoded[:, role] - expected_concept[:, role]) ** 2)) / normalizer[role])
            other = 1 - role
            metrics["untouched_decoder_nrmse"] = float(np.sqrt(np.mean((decoded[:, other] - expected_concept[:, other]) ** 2)) / normalizer[other])
            metrics["whole_layer_swap"] = _basic_error(sigmoid(hd @ net.v + net.beta), ph)
            metrics["no_swap"] = _basic_error(pb_net, ph)
            role_results[stratum] = metrics
            raw[role][stratum] = {"probability": pint, "expected": ph,
                                    "absolute_error": np.abs(pint - ph)}
        result["roles"].append(role_results)
    return result, raw


def _comparison_statistics(improvements: np.ndarray) -> dict[str, Any]:
    # Distribution-free confidence intervals / multiplicity are set in protocol;
    # retain sufficient bounded-sample moments for the caller to apply them.
    n = len(improvements)
    return {"n": n, "mean_paired_absolute_error_improvement": float(np.mean(improvements)),
            "sample_variance": float(np.var(improvements, ddof=1)) if n > 1 else 0.0,
            "minimum": float(np.min(improvements)), "maximum": float(np.max(improvements)),
            "sum": float(np.sum(improvements)), "sum_squares": float(np.sum(improvements ** 2))}


def evaluate_neural(prepared: dict[str, Any], config: dict[str, Any], eval_seed: int,
                    n_per_stratum: int | None = None) -> dict[str, Any]:
    """Evaluate an already frozen discovery artifact; caller owns split gate."""
    c = validate_config(config)
    if prepared["config_hash"] != canonical_hash(c):
        raise ValueError("Discovery artifact/configuration mismatch.")
    unhashed = {k: v for k, v in prepared.items() if k != "artifact_hash"}
    if prepared["artifact_hash"] != canonical_hash(unhashed):
        raise ValueError("Discovery artifact hash mismatch.")
    if eval_seed == prepared["discovery_seed"]:
        raise ValueError("Evaluation cannot reuse the discovery seed.")
    started_wall, started_cpu = time.perf_counter(), time.process_time()
    n = c["evaluation_pairs_per_stratum"] if n_per_stratum is None else n_per_stratum
    pairs, generation, wrong_pairs, wrong_generation = [], [], [], []
    for role in (0, 1):
        p, gen = make_pairs(c, eval_seed, n, role, 200 + 10 * role)
        pairs.append(p)
        generation.append(gen)
        wrong, wrong_gen = make_pairs(c, eval_seed, n, role, 230 + 10 * role)
        wrong_pairs.append(wrong)
        wrong_generation.append(wrong_gen)
    net = MLP.from_dict(prepared["network"])
    initial = MLP.from_dict(prepared["untrained_network"])
    inputs = sample_inputs(_rng(eval_seed, 300), c["task_evaluation_samples"])
    learned = net.probability(inputs)
    target = optimal_probability(inputs)
    j = action_costs(inputs)
    action = learned >= 0.5
    expected_decision_cost = np.where(action, j[:, 1], j[:, 0])
    task = _basic_error(learned, target)
    task["mean_decision_regret"] = float(np.mean(expected_decision_cost - np.min(j, axis=1)))
    task["max_decision_regret"] = float(np.max(expected_decision_cost - np.min(j, axis=1)))
    eps = np.finfo(np.float64).eps
    p = np.clip(learned, eps, 1 - eps)
    task["expected_weighted_bce"] = float(np.mean(-j[:, 0] * np.log(p) - j[:, 1] * np.log1p(-p)))
    task["optimal_expected_weighted_bce"] = float(np.mean(-j[:, 0] * np.log(target) - j[:, 1] * np.log1p(-target)))
    evaluated, raw = {}, {}
    for name, alignment in prepared["alignments"].items():
        selected_net = initial if alignment["control"] == "untrained" else net
        evaluated[name], raw[name] = _evaluate_alignment(selected_net, alignment, pairs, wrong_pairs, c, eval_seed)
        hidden = selected_net.hidden(inputs)
        truth = concepts(inputs, alignment["g_id"])
        evaluated[name]["observational_decoder_nrmse"] = [float(np.sqrt(np.mean((decode(hidden, r["decoder"]) - truth[:, role]) ** 2)) / max(np.std(truth[:, role]), 1e-12)) for role, r in enumerate(alignment["roles"])]
        evaluated[name]["log_contribution_rmse"] = [float(np.sqrt(np.mean((hidden[:, r["subset"]] @ selected_net.v[r["subset"]] - (1 if role == 0 else -1) * np.log(truth[:, role]) - r["log_contribution_offset"]) ** 2))) for role, r in enumerate(alignment["roles"])]
    comparisons_by_g = {}
    for g in G_FAMILY:
        comparisons_by_g[g] = {}
        for control in SEARCH_CONTROLS[1:]:
            name = f"{g}/{control}"
            comparisons_by_g[g][control] = {}
            for role in (0, 1):
                for stratum in STRATA:
                    improvement = raw[name][role][stratum]["absolute_error"] - raw[f"{g}/aligned"][role][stratum]["absolute_error"]
                    comparisons_by_g[g][control][f"{role}/{stratum}"] = _comparison_statistics(improvement)
    alternatives = {}
    for g in G_FAMILY[1:]:
        alternatives[g] = {}
        for role in (0, 1):
            for stratum in STRATA:
                identity = raw["identity/aligned"][role][stratum]
                competing = raw[f"{g}/aligned"][role][stratum]
                mask = np.abs(identity["expected"] - competing["expected"]) >= c["g_separation_min"]
                # Each independently fitted alignment is judged against its own
                # counterfactual hypothesis on the same base/donor pairs.
                comparison = _comparison_statistics(competing["absolute_error"][mask] - identity["absolute_error"][mask]) if np.any(mask) else None
                alternatives[g][f"{role}/{stratum}"] = {"separating_pairs": int(mask.sum()),
                    "total_pairs": len(mask), "separating_fraction": float(mask.mean()),
                    "sufficient_separating_pairs": bool(mask.sum() >= c["g_min_separating_pairs"]),
                    "hypothesis_prediction_mae": float(np.mean(np.abs(identity["expected"] - competing["expected"]))),
                    "comparison": comparison}
                same_subset_error = np.abs(identity["probability"] - competing["expected"])
                alternatives[g][f"{role}/{stratum}"]["same_identity_subset_against_alternative"] = _basic_error(identity["probability"], competing["expected"])
                alternatives[g][f"{role}/{stratum}"]["same_identity_subset_comparison"] = _comparison_statistics(same_subset_error[mask] - identity["absolute_error"][mask]) if np.any(mask) else None
    alignment = prepared["alignments"]["identity/aligned"]
    grng = _rng(eval_seed, 500)
    permutation = grng.permutation(c["width"])
    scales = np.exp(grng.uniform(np.log(c["gauge_scale_min"]), np.log(c["gauge_scale_max"]), c["width"]))
    gauged = net.gauge(permutation, scales)
    transported = transport_alignment(alignment, permutation, scales)
    gauge_errors = {"observational_probability": float(np.max(np.abs(gauged.probability(inputs) - learned))),
                    "intervention_probability": 0.0, "decoder_value": 0.0}
    for role in (0, 1):
        b, d = _stack_pairs(pairs[role])
        oldb, oldd = net.hidden(b), net.hidden(d)
        newb, newd = gauged.hidden(b), gauged.hidden(d)
        old_p = _swap_probabilities(net, oldb, oldd, alignment["roles"][role]["subset"])
        new_p = _swap_probabilities(gauged, newb, newd, transported["roles"][role]["subset"])
        gauge_errors["intervention_probability"] = max(gauge_errors["intervention_probability"], float(np.max(np.abs(old_p - new_p))))
        old_mixed, new_mixed = oldb.copy(), newb.copy()
        old_s, new_s = alignment["roles"][role]["subset"], transported["roles"][role]["subset"]
        old_mixed[:, old_s], new_mixed[:, new_s] = oldd[:, old_s], newd[:, new_s]
        for other in (0, 1):
            error = np.max(np.abs(decode(old_mixed, alignment["roles"][other]["decoder"]) - decode(new_mixed, transported["roles"][other]["decoder"])))
            gauge_errors["decoder_value"] = max(gauge_errors["decoder_value"], float(error))
    gauge = {"errors": gauge_errors, "tolerance": c["gauge_tolerance"],
             "passed": all(v <= c["gauge_tolerance"] for v in gauge_errors.values()),
             "permutation": permutation.tolist(), "scales": scales.tolist(), "refits": 0}
    gauges_by_g = {"identity": gauge}
    for g in G_FAMILY[1:]:
        alternative = prepared["alignments"][f"{g}/aligned"]
        transported_g = transport_alignment(alternative, permutation, scales)
        errors_g = {"observational_probability": gauge_errors["observational_probability"],
                    "intervention_probability": 0.0, "decoder_value": 0.0}
        for role in (0, 1):
            b, d = _stack_pairs(pairs[role])
            oldb, oldd = net.hidden(b), net.hidden(d)
            newb, newd = gauged.hidden(b), gauged.hidden(d)
            old_s, new_s = alternative["roles"][role]["subset"], transported_g["roles"][role]["subset"]
            old_p = _swap_probabilities(net, oldb, oldd, old_s)
            new_p = _swap_probabilities(gauged, newb, newd, new_s)
            errors_g["intervention_probability"] = max(errors_g["intervention_probability"], float(np.max(np.abs(old_p - new_p))))
            oldb[:, old_s], newb[:, new_s] = oldd[:, old_s], newd[:, new_s]
            for other in (0, 1):
                error = np.max(np.abs(decode(oldb, alternative["roles"][other]["decoder"]) - decode(newb, transported_g["roles"][other]["decoder"])))
                errors_g["decoder_value"] = max(errors_g["decoder_value"], float(error))
        gauges_by_g[g] = {"errors": errors_g, "tolerance": c["gauge_tolerance"],
                         "passed": all(v <= c["gauge_tolerance"] for v in errors_g.values()),
                         "permutation": permutation.tolist(), "scales": scales.tolist(), "refits": 0}
    # Composition is an explicitly secondary diagnostic. Overlap can cause donor
    # precedence to matter even if each isolated role appears predictive.
    b, d0 = pairs[0]["mixed_far"]
    d1 = pairs[1]["mixed_far"][1]
    hb, h0, h1 = net.hidden(b), net.hidden(d0), net.hidden(d1)
    s0, s1 = [r["subset"] for r in alignment["roles"]]
    h01, h10 = hb.copy(), hb.copy()
    h01[:, s0], h01[:, s1] = h0[:, s0], h1[:, s1]
    h10[:, s1], h10[:, s0] = h1[:, s1], h0[:, s0]
    p01, p10 = sigmoid(h01 @ net.v + net.beta), sigmoid(h10 @ net.v + net.beta)
    j0, j1 = action_costs(d0)[:, 0], action_costs(d1)[:, 1]
    ph = j0 / (j0 + j1)
    composition = {"role0_then_role1": _basic_error(p01, ph), "role1_then_role0": _basic_error(p10, ph),
                   "order_probability_max_difference": float(np.max(np.abs(p01 - p10))),
                   "overlap_size": len(alignment["overlap"]), "primary_claim": False}
    global2 = copy.deepcopy(alignment)
    for r in global2["roles"]:
        r["decoder"]["coefficient"] = [c["global_scale_control"] * a for a in r["decoder"]["coefficient"]]
        r["decoder"]["intercept"] *= c["global_scale_control"]
    global_scale_error = max(float(np.max(np.abs(decode(net.hidden(inputs), r2["decoder"]) - c["global_scale_control"] * decode(net.hidden(inputs), r["decoder"])))) for r, r2 in zip(alignment["roles"], global2["roles"]))
    global_prediction_error = 0.0
    for role in (0, 1):
        base, donor = _stack_pairs(pairs[role])
        jb, jd = c["global_scale_control"] * action_costs(base), c["global_scale_control"] * action_costs(donor)
        pg = jd[:, 0] / (jd[:, 0] + jb[:, 1]) if role == 0 else jb[:, 0] / (jb[:, 0] + jd[:, 1])
        global_prediction_error = max(global_prediction_error, float(np.max(np.abs(pg - high_prediction(base, donor, role)))))
    task["decision_regret_bound"] = 1.375
    task["mean_normalized_decision_regret"] = task["mean_decision_regret"] / 1.375
    result = {"schema": "f14-neural-evaluation-v1", "discovery_artifact_hash": prepared["artifact_hash"],
              "evaluation_seed": eval_seed, "pairs_per_stratum": n, "task": task,
              "alignments": evaluated, "matched_control_comparisons": comparisons_by_g["identity"],
              "matched_control_comparisons_by_g": comparisons_by_g,
              "selected_alternative": prepared["selected_alternative"], "alternative_comparisons": alternatives,
              "gauge": gauge, "gauges_by_g": gauges_by_g, "global_scale_decoder_error": global_scale_error,
              "global_scale_prediction_error": global_prediction_error,
              "unused_duplicate_witness": unused_duplicate_witness(), "composition": composition,
              "pair_generation": generation, "wrong_donor_generation": wrong_generation,
              "evaluation_data_hashes": {"task_inputs": array_hash(inputs),
                   "role_pairs": [array_hash(*_stack_pairs(p)) for p in pairs],
                   "wrong_donor_role_pairs": [array_hash(*_stack_pairs(p)) for p in wrong_pairs]},
              "resource": {"wall_seconds": time.perf_counter() - started_wall,
                   "cpu_seconds": time.process_time() - started_cpu,
                   "pair_examples": 2 * len(STRATA) * n,
                   "alignment_role_pair_evaluations": len(evaluated) * 2 * len(STRATA) * n,
                   "alignment_refits": 0}}
    return result


def development_smoke(config: dict[str, Any] | None = None) -> dict[str, Any]:
    """Bounded end-to-end DEVELOPMENT check; never calls the evaluation seeds."""
    base = defaults() if config is None else copy.deepcopy(_cfg(config))
    c = copy.deepcopy(base)
    c.update(base["smoke"])
    prepared = prepare_neural(c, c["development_seed"])
    results = evaluate_neural(prepared, c, c["development_evaluation_seed"])
    return {"status": "development_only", "config": c, "prepared": prepared,
            "results": results, "held_out_evaluation_executed": False}
