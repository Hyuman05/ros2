#!/bin/bash
# ROS 2環境のセットアップ
source /opt/ros/humble/setup.bash
source ~/ros2_ws/install/setup.bash

# テスト結果追跡変数
TEST_FAILED=0

# トランスレーターをバックグラウンドで起動
ros2 run mypkg translator &
TRANSLATOR_PID=$!

# サービスが利用可能になるまで待機
sleep 2

# Test 1: Check translation for "こんにちは"
result_hello=$(ros2 service call /trigger person_msgs/srv/Trigger "{input: 'こんにちは'}" | grep -oP "(?<=output: ')[^']+")
if [ "$result_hello" == "Hello" ]; then
    echo "Test Passed: 'こんにちは' was correctly translated to 'Hello'"
else
    echo "Test Failed: 'こんにちは' translation error"
    TEST_FAILED=1
fi

# トランスレーターを停止
kill $TRANSLATOR_PID

# 終了ステータスを確認
if [ $TEST_FAILED -eq 0 ]; then
    echo "All tests passed!"
    exit 0
else
    echo "Some tests failed."
    exit 1
fi
