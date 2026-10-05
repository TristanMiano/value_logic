// Generic synthetic-only feasibility benchmark. No model or experimental data.
// Contributor: ChatGPT (GPT-6 Astra Pro), F15-ND01.
#include <array>
#include <chrono>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <limits>

constexpr int N = 32, K = 8;
double gram[N][N], linear[N], best = std::numeric_limits<double>::infinity();
std::array<int, K> chosen{}, selected{};
std::uint64_t leaves = 0, nodes = 0;

void enumerate(int start, int depth, double value) {
    ++nodes;
    if (depth == K) {
        ++leaves;
        if (value < best) {
            best = value;
            selected = chosen;
        }
        return;
    }
    for (int i = start; i <= N - (K - depth); ++i) {
        double increment = gram[i][i] - 2.0 * linear[i];
        for (int j = 0; j < depth; ++j)
            increment += 2.0 * gram[i][chosen[j]];
        chosen[depth] = i;
        enumerate(i + 1, depth + 1, value + increment);
    }
}

int main() {
    // Positive-definite diagonal plus rank-one synthetic Gram matrix.
    for (int i = 0; i < N; ++i) {
        linear[i] = 0.03 * (i + 1);
        for (int j = 0; j < N; ++j)
            gram[i][j] = 0.000001 * (i + 1) * (j + 1)
                + (i == j ? 1.0 + 0.001 * i : 0.0);
    }
    const auto started = std::chrono::steady_clock::now();
    enumerate(0, 0, 10.0);
    const double elapsed = std::chrono::duration<double>(
        std::chrono::steady_clock::now() - started).count();
    std::cout << std::setprecision(17)
        << "{\"synthetic_only\":true,\"network_data_used\":false,\"subsets\":" << leaves
        << ",\"nodes\":" << nodes << ",\"wall_seconds\":" << elapsed
        << ",\"minimum\":" << best << ",\"subset\":[";
    for (int i = 0; i < K; ++i) std::cout << (i ? "," : "") << selected[i];
    std::cout << "]}\n";
    return leaves == 10518300 ? 0 : 1;
}
