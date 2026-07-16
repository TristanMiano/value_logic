#pragma once

#include <cstdint>

#if defined(_WIN32)
#  if defined(VL_KERNEL_BUILD)
#    define VL_API extern "C" __declspec(dllexport)
#  else
#    define VL_API extern "C" __declspec(dllimport)
#  endif
#else
#  define VL_API extern "C" __attribute__((visibility("default")))
#endif

// Decode one caller-owned block.  The function allocates no memory and returns
// zero on success; the numbered failure codes are documented in the .cpp file.
VL_API int vl_decode_block_v1(
    std::int64_t row_count,
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
    float* refutation_relu) noexcept;
