#!/bin/bash

python src/generate.py \
    --genereate_num 3 \
    --start_idx 0 \
    --end_idx 1000 \
    --sleeptime 1 \
    --dataset /root/Workspace/datasets/ms_marco/ms_marco.py \
    --save_dir /root/Workspace/repeat_curse/data \
    --save_file_name related_3.jsonl \
    --log_dir /root/Workspace/repeat_curse/log \
    --log_file_name generate_related_3.log
