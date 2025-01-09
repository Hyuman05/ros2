#!/bin/bash -evx

ros2 launch mypkg translate_question.launch.py &
LAUNCH_PID=$!
sleep 10

echo "Checking if 'triger' service is available..."
if ! ros2 service list | grep -q "/trigger"; then
    echo "'trigger' service is not available. Test failed."
    kill $LAUNCH_PID
    exit 1
fi

echo "calling 'trigger' service with test input..."
REQUEST='{"japanese": "こんにちは"}'
RESPONSE=$(ros2 servise call /trigger person_msgs/srv/Trigger "$REQUEST")

if echo "$RESPONSE" | grep -q "Hello"; then
    echo "Service responded correctly: $RESPONSE"
else
    echo "Unexpected response: $RESPONSE"
    kill $LAUNCH_PID
    exit 1
fi

TEST_WORDS=("ありがとう" "さようなら" "いぬ" "ねこ" "不明な単語")
EXPECTED=$("thank you" "Goodbye" "Dog" "cat" "Unknown")

for i in "${!TEST_WORDS[@]}"; do
    echo "Testing with word: ${TEST_WORDS[$i]}"
    REQUEST="{\"japanese\": \"${TEST_WORDS[$i]}\"}"
    RESPONSE=$(ros2 service call /trigger person_msgs/srv/Trigger "$REQUEST")
    if echo "$RESPONSE" | grep -q "${EXPECTED[$i]}"; then
        echo "Test passed for '${TEST_WORDS[$i]}': $RESPONSE"
    else
        echo "Test failed for '${TEST_WORDS}'.Response: $RESPONSE"
        kill $LAUNCH_PID
        exit 1
    fi
done

echo "ALL tests passed!"
kill $LAUNCH_PID
wait $LAUNCH_PID
exit 0



