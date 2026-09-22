#include "pch.h"
#include "CppUnitTest.h"
#include <unordered_map>

using namespace Microsoft::VisualStudio::CppUnitTestFramework;

namespace UnitTests1
{
    TEST_CLASS(UnitTest1)
    {
    public:
        TEST_METHOD(TestMethod1) {
            std::unordered_map<int, int> dict;
            for (int i = 0; i < 100; ++i) {
                dict[i] = i;
            }
            Assert::AreEqual((size_t)100, dict.size());
        }
        TEST_METHOD(TestMethod2) {
            std::unordered_map<int, int> dict;
            dict[5] = 100;
            Assert::AreEqual(100, dict[5]);
            Assert::IsTrue(dict.find(10) == dict.end());
        }
        TEST_METHOD(TestMethod3) {
            std::unordered_map<int, int> dict;
            Assert::IsTrue(dict.empty());
        }
    };
}