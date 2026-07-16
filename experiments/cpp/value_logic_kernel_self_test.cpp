#include "value_logic_kernel.h"

#include <cmath>
#include <cstdint>

int main() {
  const float structured[4] = {1.0F, 0.0F, 0.0F, 0.0F};
  const float logits[3] = {-2.0F, -1.0F, 3.0F};
  const std::int8_t schema[1] = {0};
  const double threshold[1] = {0.1};
  const std::uint8_t yes[1] = {1};
  const double eta[1] = {0.0};
  std::int8_t states[5] = {};
  float margins[4] = {};

  const int status = vl_decode_block_v1(
      1,
      structured,
      logits,
      schema,
      threshold,
      yes,
      yes,
      yes,
      yes,
      eta,
      eta,
      yes,
      yes,
      &states[0],
      &states[1],
      &states[2],
      &states[3],
      &states[4],
      &margins[0],
      &margins[1],
      &margins[2],
      &margins[3]);
  if (status != 0) {
    return 1;
  }
  // Equality at the inclusive upper boundary is Supported even though its
  // strict support surplus is zero.  This is a critical semantic edge case.
  if (states[0] != 2 || states[1] != 2 || states[2] != 2 || states[3] != 2) {
    return 2;
  }
  if (margins[0] != 0.0F || margins[2] != 0.0F) {
    return 3;
  }

  const std::int8_t invalid_schema[1] = {9};
  if (vl_decode_block_v1(
          1,
          structured,
          logits,
          invalid_schema,
          threshold,
          yes,
          yes,
          yes,
          yes,
          eta,
          eta,
          yes,
          yes,
          &states[0],
          &states[1],
          &states[2],
          &states[3],
          &states[4],
          &margins[0],
          &margins[1],
          &margins[2],
          &margins[3]) != 3) {
    return 4;
  }
  return 0;
}
