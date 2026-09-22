#include <iostream>
#include <vector>
#include <chrono>
#include <unordered_map>

void add_to_dict(int n) {
    std::unordered_map<int, int> dict;
    for (int i = 0; i < n; ++i) {
        dict[i] = i;
    }
}

template <typename Func, typename... Args>
auto measure_execution_time(Func&& func, Args&&... args) {
    auto start_time = std::chrono::high_resolution_clock::now();
    func(std::forward<Args>(args)...);
    auto end_time = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end_time - start_time);
    return duration.count();
}

int main() {
    setlocale(LC_ALL, "Russian");
    std::vector<int> sizes = { 10, 100, 500, 1000, 5000, 10000, 50000, 100000, 500000, 1000000, 5000000 };
    for (int n : sizes) {
        auto time = measure_execution_time(add_to_dict, n);
        std::cout << "Размер: " << n << "  Время выполнения: " << time << " мс" << std::endl;
    }
    return 0;
}