#!/bin/bash

# Define the tmux session name
SESSION="DarkStories"

# Pull the images if they don't exist
docker pull gergopool/educhat

# Check if the session exists
tmux has-session -t $SESSION 2>/dev/null


if [ $? != 0 ]; then
  # Create a new session and split the window into two panes
  tmux new-session -d -s $SESSION

  # Run the Docker containers in each pane
  tmux send-keys -t $SESSION:0.0 "cd docker; ./docker_run.sh -i -p 3000:3000 bash" C-m
  tmux send-keys -t $SESSION:0.0 "python3 run.py" C-m
fi

# Attach to the session
tmux attach-session -t $SESSION
