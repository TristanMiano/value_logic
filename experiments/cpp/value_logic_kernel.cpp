// Data-oriented exact decoder for the value-logic experiment.
//
// Python calls this function once for an entire numeric block.  There are no
// Python objects, callbacks, ownership transfers, or hidden allocations in the
// interface.  Every input and output is a caller-owned contiguous array.

#include <algorithm>
#include <cmath>
#include <limits>

#include "value_logic_kernel.h"

namespace {

constexpr std::int8_t kRefuted = 0;
constexpr std::int8_t kOpen = 1;
constexpr std::int8_t kSupported = 2;

std::int8_t decode_region(
    const double lower,
    const double upper,
    const double threshold,
    const bool evidence_usable,
    const bool can_support,
    const bool can_refute) noexcept {
  if (!evidence_usable) {
    return kOpen;
  }
  if (upper <= threshold && can_support) {
    return kSupported;
  }
  if (lower > threshold && can_refute) {
    return kRefuted;
  }
  return kOpen;
}

std::int8_t argmax_three(const float* logits) noexcept {
  std::int8_t best = 0;
  if (logits[1] > logits[best]) {
    best = 1;
  }
  if (logits[2] > logits[best]) {
    best = 2;
  }
  return best;
}

double maximum_softmax_probability(const float* logits) noexcept {
  const double maximum = std::max(
      static_cast<double>(logits[0]),
      std::max(static_cast<double>(logits[1]), static_cast<double>(logits[2])));
  const double first = std::exp(static_cast<double>(logits[0]) - maximum);
  const double second = std::exp(static_cast<double>(logits[1]) - maximum);
  const double third = std::exp(static_cast<double>(logits[2]) - maximum);
  return std::max(first, std::max(second, third)) / (first + second + third);
}

}  // namespace

// Returns zero on success.  Positive return values identify malformed inputs:
// 1 = null pointer, 2 = negative row count, 3 = invalid schema, 4 = nonfinite
// model output or threshold, 5 = negative finite calibration radius.
int vl_decode_block_v1(
    const std::int64_t row_count,
    const float* structured_raw,
    const float* ce_logits,
    const std::int8_t* schema,
    const double* threshold,
    const std::uint8_t* evidence_present,
    const std::uint8_t* evidence_valid,
    const std::uint8_t* can_support,
    const std::uint8_t* can_refute,
    const double* eta,
    const double* center_eta,
    const std::uint8_t* binding_ok,
    const std::uint8_t* center_binding_ok,
    std::int8_t* structured_state,
    std::int8_t* center_state,
    std::int8_t* shadow_state,
    std::int8_t* ce_state,
    std::int8_t* self_confidence_state,
    float* support_margin,
    float* refutation_margin,
    float* support_relu,
    float* refutation_relu) noexcept {
  if (row_count < 0) {
    return 2;
  }
  if (row_count == 0) {
    return 0;
  }
  if (structured_raw == nullptr || ce_logits == nullptr || schema == nullptr ||
      threshold == nullptr || evidence_present == nullptr || evidence_valid == nullptr ||
      can_support == nullptr || can_refute == nullptr || eta == nullptr ||
      center_eta == nullptr || binding_ok == nullptr || center_binding_ok == nullptr ||
      structured_state == nullptr || center_state == nullptr || shadow_state == nullptr ||
      ce_state == nullptr || self_confidence_state == nullptr || support_margin == nullptr ||
      refutation_margin == nullptr || support_relu == nullptr || refutation_relu == nullptr) {
    return 1;
  }

  for (std::int64_t row = 0; row < row_count; ++row) {
    const std::int8_t local_schema = schema[row];
    if (local_schema != 0 && local_schema != 1) {
      return 3;
    }
    const double scale = local_schema == 0 ? 0.1 : 10.0;
    const std::int64_t center_index = local_schema == 0 ? 0 : 2;
    const std::int64_t radius_index = local_schema == 0 ? 1 : 3;
    const float* local_structured = structured_raw + 4 * row;
    const float* local_logits = ce_logits + 3 * row;
    const double local_threshold = threshold[row];
    for (int coordinate = 0; coordinate < 4; ++coordinate) {
      if (!std::isfinite(static_cast<double>(local_structured[coordinate]))) {
        return 4;
      }
    }
    for (int coordinate = 0; coordinate < 3; ++coordinate) {
      if (!std::isfinite(static_cast<double>(local_logits[coordinate]))) {
        return 4;
      }
    }
    if (!std::isfinite(local_threshold)) {
      return 4;
    }
    if ((std::isfinite(eta[row]) && eta[row] < 0.0) ||
        (std::isfinite(center_eta[row]) && center_eta[row] < 0.0)) {
      return 5;
    }

    const double center = static_cast<double>(local_structured[center_index]) * scale;
    const double learned_radius =
        std::max(0.0, static_cast<double>(local_structured[radius_index])) * scale;
    const bool present = evidence_present[row] != 0;
    const bool valid = evidence_valid[row] != 0;
    const bool supports = can_support[row] != 0;
    const bool refutes = can_refute[row] != 0;

    const double full_radius = learned_radius + eta[row];
    const double lower = center - full_radius;
    const double upper = center + full_radius;
    structured_state[row] = decode_region(
        lower,
        upper,
        local_threshold,
        binding_ok[row] != 0 && present && valid,
        supports,
        refutes);

    const double center_lower = center - center_eta[row];
    const double center_upper = center + center_eta[row];
    center_state[row] = decode_region(
        center_lower,
        center_upper,
        local_threshold,
        center_binding_ok[row] != 0 && present && valid,
        supports,
        refutes);

    shadow_state[row] = decode_region(
        center - learned_radius,
        center + learned_radius,
        local_threshold,
        present && valid,
        supports,
        refutes);

    std::int8_t direct = argmax_three(local_logits);
    if (!present || !valid || (direct == kSupported && !supports) ||
        (direct == kRefuted && !refutes)) {
      direct = kOpen;
    }
    ce_state[row] = direct;
    self_confidence_state[row] =
        maximum_softmax_probability(local_logits) >= 0.5 ? kSupported : kOpen;

    const double local_support_margin = local_threshold - upper;
    const double local_refutation_margin = lower - local_threshold;
    support_margin[row] = static_cast<float>(local_support_margin);
    refutation_margin[row] = static_cast<float>(local_refutation_margin);
    support_relu[row] =
        static_cast<float>(std::max(0.0, local_support_margin / scale));
    refutation_relu[row] =
        static_cast<float>(std::max(0.0, local_refutation_margin / scale));
  }
  return 0;
}
