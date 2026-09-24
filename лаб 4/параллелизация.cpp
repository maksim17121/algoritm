#include <iostream>
#include <vector>
#include <algorithm>
#include <chrono>
#include <thread>
#include <cstdlib>

using namespace std;

int partition(vector<int>& a, int low, int high) {
    int pivot = a[high];
    int i = low - 1;
    for (int j = low; j <= high - 1; ++j) {
        if (a[j] <= pivot) {
            ++i;
            swap(a[i], a[j]);
        }
    }
    swap(a[i + 1], a[high]);
    return i + 1;
}

void quickSort(vector<int>& a, int low, int high) {
    if (low < high) {
        int p = partition(a, low, high);
        quickSort(a, low, p - 1);
        quickSort(a, p + 1, high);
    }
}

void parallelQuickSort(vector<int>& a, int low, int high, int threads) {
    if (threads <= 1 || (high - low) < 1000) {
        quickSort(a, low, high);
        return;
    }
    int p = partition(a, low, high);
    thread leftThread(parallelQuickSort, ref(a), low, p - 1, threads / 2);
    parallelQuickSort(a, p + 1, high, threads / 2);
    leftThread.join();
}

double getTime(int size, int threadCount) {
    vector<int> a(size);
    for (int i = 0; i < size; ++i) a[i] = rand() % size;

    auto start = chrono::high_resolution_clock::now();

    if (threadCount == 1) {
        quickSort(a, 0, size - 1);
    }
    else {
        parallelQuickSort(a, 0, size - 1, threadCount);
    }

    auto end = chrono::high_resolution_clock::now();
    chrono::duration<double> diff = end - start;
    return diff.count();
}

int main() {
    setlocale(LC_ALL, "Russian");
    cout << "Тестирование параллельной быстрой сортировки..." << endl;

    int sizes[] = { 100, 1000, 10000, 20000, 30000, 40000, 50000 };
    int threads[] = { 1, 2, 4, 8 };

    for (int n : sizes) {
        cout << "\nРазмер массива: " << n << endl;
        for (int t : threads) {
            double timeTaken = getTime(n, t);
            cout << "Потоков: " << t << " | Время: " << timeTaken << " сек." << endl;
        }
    }

    return 0;
}