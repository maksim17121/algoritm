#include "pch.h"
#include "CppUnitTest.h"
#include "../ConsoleApplication2/ConsoleApplication2.cpp"

using namespace Microsoft::VisualStudio::CppUnitTestFramework;

double linear_func(double x) {
    return 2.0 * x;
}

namespace UnitTest2
{
    TEST_CLASS(UnitTest2)
    {
    public:
        TEST_METHOD(TestMethod1)
        {
            double result = simpson_rule(linear_func, 0.0, 2.0, 100);
            Assert::AreEqual(4.0, result, 0.00001, L"Значения не совпали для линейной функции");
        }
        TEST_METHOD(TestMethod2)
        {
            double r1 = simpson_rule(target_function, 1.0, 2.0, 100);
            double r2 = simpson_rule(target_function, 1.0, 2.0, 100);
            Assert::AreEqual(r1, r2, 0.00001, L"Результаты одного и того же расчета различаются");
        }
        TEST_METHOD(TestMethod3)
        {
            double result = simpson_rule(target_function, 1.5, 1.5, 100);
            Assert::AreEqual(0.0, result, 0.00001, L"Площадь на нулевом интервале должна быть 0");
        }
    };
}