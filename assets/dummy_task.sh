#!/bin/bash

# Default fallback values
project_id="unknown"
instance_id="unknown"
uv_command="uv"

# Parse the arguments passed by the scheduler
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --project) project_id="$2"; shift ;;
        --instance) instance_id="$2"; shift ;;
        --uv) uv_command="$2"; shift ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

# Simulate workload and log output
echo "[$(date '+%Y-%m-%d %H:%M:%S')] START: Project '$project_id' (Instance: $instance_id)"
echo "            Using uv environment at: $uv_command"
echo "            Simulating data processing..."
sleep 2 # Simulate work
echo "[$(date '+%Y-%m-%d %H:%M:%S')] END:   Project '$project_id' completed."
echo "---------------------------------------------------"
