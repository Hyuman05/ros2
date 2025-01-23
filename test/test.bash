#!/bin/bash

# テスト結果追跡用変数
TEST_FAILED=0

# Test 1: Check translation for "こんにちは"
result_hello=$(ros2 service call /trigger person_msgs/srv/Trigger "{input: 'こんにちは'}" | grep -o 'Hello')
if [ "$result_hello" == "Hello" ]; then
    echo "Test Passed: 'こんにちは' was correctly translated to 'Hello'"
else
    echo "Test Failed: 'こんにちは' translation error"
    TEST_FAILED=1
fi

# Test 2: Check translation for "ありがとう"
result_thanks=$(ros2 service call /trigger person_msgs/srv/Trigger "{input: 'ありがとう'}" | grep -o 'Thank you')
if [ "$result_thanks" == "Thank you" ]; then
    echo "Test Passed: 'ありがとう' was correctly translated to 'Thank you'"
else
    echo "Test Failed: 'ありがとう' translation error"
    TEST_FAILED=1
fi

# Test 3: Check translation for "さようなら"
result_goodbye=$(ros2 service call /trigger person_msgs/srv/Trigger "{input: 'さようなら'}" | grep -o 'Goodbye')
if [ "$result_goodbye" == "Goodbye" ]; then
    echo "Test Passed: 'さようなら' was correctly translated to 'Goodbye'"
else
    echo "Test Failed: 'さようなら' translation error"
    TEST_FAILED=1
fi

# 結果の出力
if [ $TEST_FAILED -eq 0 ]; then
    echo "All tests passed!"
else
    echo "Some tests failed."
fi
