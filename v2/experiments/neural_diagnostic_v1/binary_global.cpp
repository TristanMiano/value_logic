// Exhaustive finite-float64 fixed-cardinality quadratic minimization.
// No pruning, randomized search, fast-math, or parallel threads.
// Contributor: ChatGPT (GPT-6 Astra Pro), F15-ND01.
#include <array>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <limits>

namespace {
constexpr int MAX_N = 32, MAX_K = 8;
int width, mass;
double gram[MAX_N][MAX_N], linear[MAX_N];
double minimum = std::numeric_limits<double>::infinity();
std::array<int, MAX_K> chosen{}, selected{};
std::uint64_t leaves = 0, nodes = 0;

void enumerate(int start, int depth, double value) {
    ++nodes;
    if (depth == mass) {
        ++leaves;
        // Increasing-index DFS is lexicographic. Exact equal values retain
        // the first subset; no numerical tie band can displace the minimum.
        if (value < minimum) {
            minimum = value;
            selected = chosen;
        }
        return;
    }
    for (int i = start; i <= width - (mass - depth); ++i) {
        double increment = gram[i][i] - 2.0 * linear[i];
        for (int j = 0; j < depth; ++j)
            increment += 2.0 * gram[i][chosen[j]];
        chosen[depth] = i;
        enumerate(i + 1, depth + 1, value + increment);
    }
}

std::uint64_t choose(int n, int k) {
    std::uint64_t result = 1;
    for (int i = 1; i <= k; ++i) result = result * (n - k + i) / i;
    return result;
}
}

int main() {
    double constant;
    if (!(std::cin >> width >> mass >> constant)
            || width <= 0 || width > MAX_N || mass <= 0 || mass > MAX_K
            || mass > width || !std::isfinite(constant)) return 2;
    for (int i = 0; i < width; ++i)
        if (!(std::cin >> linear[i]) || !std::isfinite(linear[i])) return 3;
    for (int i = 0; i < width; ++i)
        for (int j = 0; j < width; ++j)
            if (!(std::cin >> gram[i][j]) || !std::isfinite(gram[i][j])) return 4;
    std::string extra;
    if (std::cin >> extra) return 5;
    const auto started = std::chrono::steady_clock::now();
    enumerate(0, 0, constant);
    const double elapsed = std::chrono::duration<double>(
        std::chrono::steady_clock::now() - started).count();
    if (leaves != choose(width, mass) || !std::isfinite(minimum)) return 6;
    std::cout << std::setprecision(17)
        << "{\"schema\":\"f15-nd01-binary-global-native-v1\",\"width\":" << width
        << ",\"mass\":" << mass << ",\"enumerated_subsets\":" << leaves
        << ",\"recursion_nodes\":" << nodes << ",\"wall_seconds\":" << elapsed
        << ",\"minimum_computed_quadratic\":" << minimum << ",\"subset\":[";
    for (int i = 0; i < mass; ++i) std::cout << (i ? "," : "") << selected[i];
    std::cout << "]}\n";
    return 0;
}
