#!/bin/bash

dir=~
[ "$1" != "" ] && dir="&1"

cd $dir/ros2_ws
colcon build
sourse $dir/.bashrc
timeout 10 ros2 launch mypkg translate_question.launch.py > /tmp/mypkg.log

cat /tmp/mypkg.log |
grep 'question: 10'
