#include "CppUnitTest.h"
#include <vector>
#include <algorithm>

using namespace Microsoft::VisualStudio::CppUnitTestFramework;

// Объявления функций сортировки (если они в другом файле/заголовке)
void insertionSort(std::vector<int>& arr);
void radixSort(std::vector<int>& arr);
void quickSort(std::vector<int>& arr, int low, int high);

namespace UnitTest1
{
    TEST_CLASS(UnitTest1)
    {
    public:
        
        // Тест 1: Сортировка вставками
        TEST_METHOD(TestMethod1)
        {
            std::vector<int> arr = { 99, 12, 54, 3, 87, 29, 41, 8 };
            insertionSort(arr);
            std::vector<int> expected = { 3, 8, 12, 29, 41, 54, 87, 99 };
            
            for (size_t i = 0; i < arr.size(); i++) {
                Assert::AreEqual(expected[i], arr[i]);
            }
        }

        // Тест 2: Поразрядная сортировка
        TEST_METHOD(TestMethod2)
        {
            std::vector<int> arr = { 170, 45, 75, 90, 802, 24, 2, 66 };
            radixSort(arr);
            std::vector<int> expected = { 2, 24, 45, 66, 75, 90, 170, 802 };
            
            for (size_t i = 0; i < arr.size(); i++) {
                Assert::AreEqual(expected[i], arr[i]);
            }
        }

        // Тест 3: Быстрая сортировка
        TEST_METHOD(TestMethod3)
        {
            std::vector<int> arr = { 34, 7, 23, 32, 5, 62, 1, 15 };
            quickSort(arr, 0, arr.size() - 1);
            std::vector<int> expected = { 1, 5, 7, 15, 23, 32, 34, 62 };
            
            for (size_t i = 0; i < arr.size(); i++) {
                Assert::AreEqual(expected[i], arr[i]);
            }
        }
    };
}