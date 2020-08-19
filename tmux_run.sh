#!/bin/bash

echo -e "Tmux Run Collector" | logger -t Collector

cd /home/yepark/Production/UNeed/Collector
sudo -u yepark /usr/bin/tmux new-session -s "collector" -d -n "UNeed"
#sudo -u yepark /usr/bin/tmux set-option set-remain-on-exit on
sudo -u yepark /usr/bin/tmux send-keys -t "collector:UNeed" './run.sh' Enter

cd -

echo -e "Tmux Run Pair" | logger -t Pair

cd /home/yepark/Production/UNeed/Pair
sudo -u yepark /usr/bin/tmux new-session -s "pair" -d -n "UNeed"
#sudo -u yepark /usr/bin/tmux set-option set-remain-on-exit on
sudo -u yepark /usr/bin/tmux send-keys -t "pair:UNeed" './run.sh' Enter

cd -

echo -e "Tmux Run Dart" | logger -t Dart

cd /home/yepark/Production/UNeed/Dart
sudo -u yepark /usr/bin/tmux new-session -s "dart" -d -n "UNeed"
#sudo -u yepark /usr/bin/tmux set-option set-remain-on-exit on
sudo -u yepark /usr/bin/tmux send-keys -t "dart:UNeed" './run_dart.sh' Enter

cd -

echo -e "Tmux Run Expo" | logger -t Expo

cd /home/yepark/Production/UNeed/Dart
sudo -u yepark /usr/bin/tmux new-session -s "expo" -d -n "UNeed"
#sudo -u yepark /usr/bin/tmux set-option set-remain-on-exit on
sudo -u yepark /usr/bin/tmux send-keys -t "expo:UNeed" './run_expo.sh' Enter

cd -

echo -e "Tmux Run Watchdog" | logger -t Watchdog

cd /home/yepark/Production/UNeed/Watchdog
sudo -u yepark /usr/bin/tmux new-session -s "watchdog" -d -n "UNeed"
#sudo -u yepark /usr/bin/tmux set-option set-remain-on-exit on
sudo -u yepark /usr/bin/tmux send-keys -t "watchdog:UNeed" './run.sh' Enter

cd -
