#!/bin/bash

set -ex

python src/evaluate.py \
    --evaluate_num 3 \
    --start_idx 0 \
    --end_idx 1000 \
    --dataset /root/Workspace/datasets/ms_marco/ms_marco.py \
    --data_dir /root/Workspace/repeat_curse/data \
    --data_file_name related_3.jsonl \
    --log_dir /root/Workspace/repeat_curse/log \
    --log_file_name evaluate_related_3.log
