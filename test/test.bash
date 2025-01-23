#!/bin/bash

# ソース設定
source /opt/ros/humble/setup.bash
source /root/ros2_ws/src/install/setup.bash

# ノード起動
ros2 launch mypkg translate_question.launch.py &
LAUNCH_PID=$!  # 起動プロセスのPIDを保存
# ノードが立ち上がるまで待機
sleep 5

# テスト結果追跡用変数
TEST_FAILED=0

# Test 1: Check translation for "こんにちは"
result_hello=$(ros2 topic echo /translation_topic --once | grep -o 'Hello')
if [ "$result_hello" == "Hello" ]; then
    echo "Test Passed: 'こんにちは' was correctly translated to 'Hello'"
else
    echo "Test Failed: 'こんにちは' translation error"
    TEST_FAILED=1
fi

# Test 2: Check translation for "ありがとう"
result_thanks=$(ros2 topic echo /translation_topic --once | grep -o 'Thank you')
if [ "$result_thanks" == "Thank you" ]; then
    echo "Test Passed: 'ありがとう' was correctly translated to 'Thank you'"
else
    echo "Test Failed: 'ありがとう' translation error"
    TEST_FAILED=1
fi

# Test 3: Check translation for "さようなら"
result_goodbye=$(ros2 topic echo /translation_topic --once | grep -o 'Goodbye')
if [ "$result_goodbye" == "Goodbye" ]; then
    echo "Test Passed: 'さようなら' was correctly translated to 'Goodbye'"
else
    echo "Test Failed: 'さようなら' translation error"
    TEST_FAILED=1
fi

# Test 4: Check translation for "いぬ"
result_dog=$(ros2 topic echo /translation_topic --once | grep -o 'Dog')
if [ "$result_dog" == "Dog" ]; then
    echo "Test Passed: 'いぬ' was correctly translated to 'Dog'"
else
    echo "Test Failed: 'いぬ' translation error"
    TEST_FAILED=1
fi

# Test 5: Check translation for "ねこ"
result_cat=$(ros2 topic echo /translation_topic --once | grep -o 'Cat')
if [ "$result_cat" == "Cat" ]; then
    echo "Test Passed: 'ねこ' was correctly translated to 'Cat'"
else
    echo "Test Failed: 'ねこ' translation error"
    TEST_FAILED=1
fi

# Test 6: Check translation for "Dog" (should return 'Unknown')
result_unknown=$(ros2 topic echo /translation_topic --once | grep -o 'Unknown')
if [ "$result_unknown" == "Unknown" ]; then
    echo "Test Passed: 'Dog' was correctly translated to 'Unknown'"
else
    echo "Test Failed: 'Dog' translation error"
    TEST_FAILED=1
fi

# 起動プロセスを停止
kill $LAUNCH_PID
pkill ros2

# テスト結果を終了コードとして返す
exit $TEST_FAILED
