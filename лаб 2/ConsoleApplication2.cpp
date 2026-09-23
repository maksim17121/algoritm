#include <iostream>
#include <cmath>
#include <locale>
#include <vector>

std::vector<int> steps = { 2, 4, 6, 10, 20, 50, 100 };

double simpson_rule(double (*f)(double), double a, double b, int n) {
    if (n % 2 == 1) n++;
    double h = (b - a) / n;
    double sum = f(a) + f(b);
    for (int i = 1; i < n; i += 2)
        sum += 4 * f(a + i * h);
    for (int i = 2; i < n; i += 2)
        sum += 2 * f(a + i * h);
    return (h / 3) * sum;
}

double target_function(double x) {
    return (3.0 * std::sin(x) + 5.0) - (-2.0 * std::cos(x) + 3.0);
}

int main() {
    setlocale(LC_ALL, "Russian");
    for (int n : steps) {
        double total_area = simpson_rule(target_function, 1.0, 2.0, n);
        std::cout << "Площадь при значении " << n << std::endl;
        std::cout << "Общая площадь закрашенной фигуры: " << total_area << std::endl;
    }
    return 0;
}