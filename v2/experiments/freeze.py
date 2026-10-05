"""F14 freeze integrity and prospective split validation.

This module never generates cases or trains a model. A manifest commits the
configuration, protocol and transitive local implementation before F15.
Contributor: ChatGPT (GPT-6 Astra Pro), F14.
"""
from __future__ import annotations

import argparse
import ast
import datetime
import hashlib
import importlib.metadata
import json
import math
import os
from pathlib import Path
import platform
import sys


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG = ROOT / "v2/experiments/config.v1.json"
DEFAULT_MANIFEST = ROOT / "v2/experiments/freeze.v1.json"
BASE_REVISION = "6ce41d7caaba8b66cf813fc5949a92f95d42766c"


def _unique_object(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            raise ValueError(f"Duplicate JSON field: {key}")
        value[key] = item
    return value


def load_json(path):
    def bad_number(value):
        raise ValueError(f"Nonfinite JSON number: {value}")
    def finite_float(value):
        number = float(value)
        if not math.isfinite(number):
            raise ValueError("Overflowed JSON float.")
        return number
    return json.loads(Path(path).read_text(encoding="utf-8"),
                      object_pairs_hook=_unique_object, parse_constant=bad_number,
                      parse_float=finite_float)


def canonical_bytes(value):
    return (json.dumps(value, sort_keys=True, indent=2, allow_nan=False)+"\n").encode("utf-8")


def digest_bytes(value):
    return hashlib.sha256(value).hexdigest()


def file_digest(path):
    return digest_bytes(Path(path).read_bytes())


def write_json(path, value, *, exclusive=False):
    """Write a complete UTF-8 artifact; exclusive mode preserves earlier runs."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb" if exclusive else "wb") as handle:
        handle.write(canonical_bytes(value))
        handle.flush()
        os.fsync(handle.fileno())


def environment():
    return {"utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "python": sys.version, "platform": platform.platform(),
            "machine": platform.machine(),
            "numpy": importlib.metadata.version("numpy"),
            "thread_environment": {key: os.environ.get(key) for key in
                ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS")},
            "bitwise_reproduction_across_hosts_promised": False}


def verify_environment(config):
    record = environment()
    if record["numpy"] != config["neural"]["numpy_version"]:
        raise ValueError("Install the frozen requirements-f14.txt before generating prospective data.")
    if platform.python_implementation() != "CPython" or sys.version_info[:2] != (3, 12):
        raise ValueError("The primary F14-v1 execution runtime is CPython 3.12.x.")
    if any(value != "1" for value in record["thread_environment"].values()):
        raise ValueError("Set OMP_NUM_THREADS, OPENBLAS_NUM_THREADS and MKL_NUM_THREADS to 1 before Python starts.")
    return record


def validate_config(config):
    from . import analysis, neural, retention
    if config.get("protocol_id") != "F14-v1" or config.get("schema_version") != 1:
        raise ValueError("Unknown F14 protocol identity.")
    if config.get("source_base_revision") != BASE_REVISION:
        raise ValueError("F14 must be based on the recorded C4 source revision.")
    policy = config["run_policy"]
    if policy["final_evaluation_task"] != "F15" or policy["retune_on_evaluation"] is not False:
        raise ValueError("The prospective F14/F15 boundary is required.")
    if policy["unexplained_failure_retries"] != 1:
        raise ValueError("At most one unchanged rerun is frozen for unexplained failures.")
    neural.validate_config(config["neural"])
    rc, ac = config["retention"], config["analysis"]
    required_retention = retention.defaults()
    if canonical_bytes({key: rc.get(key) for key in required_retention}) != canonical_bytes(required_retention):
        raise ValueError("Unversioned change to a retention generator or control.")
    if canonical_bytes(config["neural"]) != canonical_bytes(neural.defaults()):
        raise ValueError("Unversioned change to a neural generator, budget or control.")
    if rc["k"] != 3 or tuple(rc["methods"]) != retention.METHODS:
        raise ValueError("The bounded family and all ordinary controls are required.")
    if tuple(rc["variants"]) != retention.VARIANTS:
        raise ValueError("The predeclared retention strata must be preserved.")
    if ac != analysis.defaults():
        raise ValueError("Unversioned change to the prospective interpretation rules.")
    if len(config["neural"]["model_seeds"]) != 5:
        raise ValueError("Five prespecified neural replications are required.")
    if len(rc["evaluation_seeds"]) != 16:
        raise ValueError("Sixteen prespecified retention population seeds are required.")
    if rc["evaluation_seeds"] != list(range(15101, 15117)):
        raise ValueError("The F14-v1 retention seed registry cannot be relabeled.")
    if len(set(rc["evaluation_seeds"])) != 16:
        raise ValueError("Repeated retention populations are not independent replications.")
    dev = [*rc["development_seeds"], config["neural"]["development_seed"],
           config["neural"]["development_evaluation_seed"]]
    future = [*rc["evaluation_seeds"], *config["neural"]["model_seeds"],
              *config["neural"]["evaluation_seeds"]]
    if set(dev) & set(future):
        raise ValueError("A development seed cannot be relabeled as evaluation.")
    if any(isinstance(seed, bool) or not isinstance(seed, int) or seed < 0 for seed in dev+future):
        raise ValueError("Seed registry requires nonnegative integers.")
    return config


def bound_configuration(config, manifest_path=DEFAULT_MANIFEST):
    """Require the supplied configuration to be the manifest's actual object."""
    verification = verify_manifest(manifest_path)
    manifest = load_json(manifest_path)
    frozen = load_json(ROOT/manifest["config_path"])
    if canonical_bytes(config) != canonical_bytes(frozen):
        raise ValueError("Supplied configuration differs from the manifest-bound freeze.")
    return verification


def validate_prepared(prepared, config, seed):
    """Preflight every durable discovery artifact before any evaluation rows."""
    from . import neural
    nc = config["neural"]
    if (prepared.get("schema") != "f14-neural-discovery-v1"
            or prepared.get("discovery_seed") != seed or prepared.get("evaluation_generated") is not False
            or prepared.get("config") != nc or prepared.get("config_hash") != neural.canonical_hash(nc)):
        raise ValueError("Discovery artifact identity, split or configuration changed.")
    unhashed = {key: value for key, value in prepared.items() if key != "artifact_hash"}
    if prepared.get("artifact_hash") != neural.canonical_hash(unhashed):
        raise ValueError("Discovery artifact's internal hash is invalid.")
    for key in ("network", "untrained_network"):
        network = neural.MLP.from_dict(prepared[key])
        if (network.w.shape != (4, nc["width"]) or network.b.shape != (nc["width"],)
                or network.v.shape != (nc["width"],)
                or not all(neural.np.isfinite(x).all() for x in
                           (network.w, network.b, network.v, neural.np.array(network.beta)))):
            raise ValueError("Saved network dimensions or numerical values changed.")
    expected = {f"{g}/{c}" for g in neural.G_FAMILY for c in neural.SEARCH_CONTROLS}
    if set(prepared["alignments"]) != expected:
        raise ValueError("An alignment or matched control is missing.")
    for name, alignment in prepared["alignments"].items():
        if f"{alignment['g_id']}/{alignment['control']}" != name or len(alignment["roles"]) != 2:
            raise ValueError("Alignment identity or role count changed.")
        for role in alignment["roles"]:
            subset = role["subset"]
            if (len(subset) != nc["subset_size"] or len(set(subset)) != len(subset)
                    or any(type(i) is not int or not 0 <= i < nc["width"] for i in subset)):
                raise ValueError("Selected subset exceeds or changes the frozen capacity.")
            decoder = role["decoder"]
            if (decoder["subset"] != subset or len(decoder["coefficient"]) != len(subset)
                    or not all(math.isfinite(float(x)) for x in
                               [*decoder["coefficient"], decoder["intercept"]])):
                raise ValueError("Decoder does not match the saved subset or numerical contract.")
            if type(role["selected_index"]) is not int or not 0 <= role["selected_index"] < nc["candidate_count"]:
                raise ValueError("Invalid selected candidate index.")
            if (len(role["candidate_pool"]) != nc["candidate_count"]
                    or len(role["candidate_scores"]) != nc["candidate_count"]
                    or role["candidate_evaluations"] != nc["candidate_count"]
                    or role["decoder_fits"] != nc["candidate_count"]
                    or role["candidate_pool"][role["selected_index"]] != subset):
                raise ValueError("Selected alignment or matched search budget changed.")
    training = prepared["training"]
    if (training["steps"] != nc["training_steps"] or training["batch_size"] != nc["batch_size"]
            or training["stochastic_outcome_labels"] != nc["training_steps"]*nc["batch_size"]
            or training["expected_cost_training_labels"] != 0):
        raise ValueError("Discovery training was not the frozen ordinary outcome-only budget.")
    if prepared["resource"]["candidate_evaluations"] != 4*5*2*nc["candidate_count"]:
        raise ValueError("Recorded alignment search budget changed.")
    # Deserialization also rejects malformed dimensionality at the first use;
    # hashes bind complete numeric arrays before that use.
    return True


def _module_path(module):
    path = ROOT.joinpath(*module.split("."))
    file_path = path.with_suffix(".py")
    if file_path.is_file():
        return file_path
    if (path / "__init__.py").is_file():
        return path / "__init__.py"
    return None


def local_dependencies(paths):
    """Conservatively follow static local Python imports, never import code."""
    pending = list(paths)
    found = set()
    while pending:
        path = Path(pending.pop()).resolve()
        if path in found:
            continue
        path.relative_to(ROOT)
        found.add(path)
        if path.suffix != ".py":
            continue
        for ancestor in path.parents:
            if ancestor == ROOT:
                break
            initializer = ancestor/"__init__.py"
            if initializer.is_file():
                pending.append(initializer)
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        relative = path.relative_to(ROOT).with_suffix("")
        parts = list(relative.parts)
        package = parts[:-1]
        for node in ast.walk(tree):
            names = []
            if isinstance(node, ast.Import):
                names = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                prefix = package[:len(package)-node.level+1] if node.level else []
                if node.module:
                    prefix += node.module.split(".")
                names = [".".join(prefix)]
                names += [".".join(prefix+[alias.name]) for alias in node.names if alias.name != "*"]
            for name in names:
                dependency = _module_path(name)
                if dependency is not None:
                    pending.append(dependency)
    return sorted(found)


def manifest_paths(config_path):
    named = [ROOT/".gitattributes", config_path, ROOT/"v2/experiments/protocol.md",
             ROOT/"v2/experiments/requirements-f14.txt",
             ROOT/"v2/experiments/F14_design_notes.md",
             ROOT/"v2/experiments/neural_design.md",
             ROOT/"v2/experiments/retention_design.md"]
    named.append(ROOT/"v2/literature/07_f14_protocol_sources.md")
    modules = [ROOT/f"v2/experiments/{name}.py" for name in
               ("freeze", "runner", "analysis", "retention", "neural", "calibration")]
    modules += sorted((ROOT/"verification").glob("test_v2_f14*.py"))
    return sorted(set(named+local_dependencies(modules)))


def create_manifest(config_path=DEFAULT_CONFIG, destination=DEFAULT_MANIFEST):
    config_path, destination = Path(config_path).resolve(), Path(destination).resolve()
    config = validate_config(load_json(config_path))
    files = {str(p.relative_to(ROOT)).replace(os.sep, "/"):
             {"sha256": file_digest(p), "bytes": p.stat().st_size}
             for p in manifest_paths(config_path)}
    manifest = {"schema": "f14-freeze-manifest-v1", "protocol_id": config["protocol_id"],
                "source_base_revision": BASE_REVISION,
                "created_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "config_path": str(config_path.relative_to(ROOT)).replace(os.sep, "/"),
                "files": files, "evaluation_executed_at_freeze": False}
    write_json(destination, manifest, exclusive=True)
    return manifest


def verify_manifest(manifest_path=DEFAULT_MANIFEST):
    manifest_path = Path(manifest_path)
    manifest = load_json(manifest_path)
    if manifest["schema"] != "f14-freeze-manifest-v1" or manifest["evaluation_executed_at_freeze"] is not False:
        raise ValueError("Not an eligible prospective freeze.")
    for name, metadata in manifest["files"].items():
        path = (ROOT/name).resolve()
        path.relative_to(ROOT)
        if not path.is_file() or file_digest(path) != metadata["sha256"] or path.stat().st_size != metadata["bytes"]:
            raise ValueError(f"Frozen artifact changed or missing: {name}")
    config_path = ROOT/manifest["config_path"]
    config = validate_config(load_json(config_path))
    required = {str(p.relative_to(ROOT)).replace(os.sep, "/") for p in manifest_paths(config_path)}
    if set(manifest["files"]) != required:
        raise ValueError("Freeze does not cover its complete local implementation.")
    return {"verified": True, "protocol_id": config["protocol_id"],
            "manifest_sha256": file_digest(manifest_path),
            "config_sha256": file_digest(config_path), "files": len(required)}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("verify", "create"))
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    args = parser.parse_args(argv)
    result = create_manifest(args.config, args.manifest) if args.action == "create" else verify_manifest(args.manifest)
    print(json.dumps(result if args.action == "verify" else
                     {"created": str(args.manifest), "files": len(result["files"])}, indent=2))


if __name__ == "__main__":
    main()
