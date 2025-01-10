#!/bin/bash -evx

dir=~
[ "$1" != "" ] && dir="$1"

cd $dir/ros2_ws
colcon build
source $dir/.bashrc

# translate_question.launch.pyをバックグラウンドで起動
ros2 launch mypkg translate_question.launch.py &
LAUNCH_PID=$!
sleep 10  # ノードの起動を待機

# 'trigger'サービスが利用可能になるまで待機
echo "Checking if 'trigger' service is available..."
for i in {1..10}; do
    if ros2 service list | grep -q "/trigger"; then
        echo "'trigger' service is available."
        break
    else
        echo "Waiting for 'trigger' service to be available..."
        sleep 1  # 1秒待機
    fi
done

# サービスが見つからない場合はテスト失敗
if ! ros2 service list | grep -q "/trigger"; then
    echo "'trigger' service is not available. Test failed."
    kill $LAUNCH_PID
    exit 1
fi

echo "calling 'trigger' service with test input..."
REQUEST='{"japanese": "こんにちは"}'
RESPONSE=$(ros2 service call /trigger person_msgs/srv/Trigger "$REQUEST")

if echo "$RESPONSE" | grep -q "Hello"; then
    echo "Service responded correctly: $RESPONSE"
else
    echo "Unexpected response: $RESPONSE"
    kill $LAUNCH_PID
    exit 1
fi

# 次のテスト
TEST_WORDS=("ありがとう" "さようなら" "いぬ" "ねこ" "不明な単語")
EXPECTED=("thank you" "Goodbye" "Dog" "cat" "Unknown")

for i in "${!TEST_WORDS[@]}"; do
    # サービスに送るリクエストを構築
    REQUEST="{\"japanese\": \"${TEST_WORDS[$i]}\"}"
    RESPONSE=$(ros2 service call /trigger person_msgs/srv/Trigger "$REQUEST")

    # 期待される応答と比較
    if echo "$RESPONSE" | grep -q "${EXPECTED[$i]}"; then
        echo "Test passed for '${TEST_WORDS[$i]}'."
    else
        echo "Test failed for '${TEST_WORDS[$i]}'. Response: $RESPONSE"
        kill $LAUNCH_PID
        exit 1
    fi
done

# 終了処理
kill $LAUNCH_PID
exit 0
