import logging
import argparse
import os
import json
from tqdm import tqdm
from collections import Counter
from datasets import load_dataset
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
from collections import Counter
from typing import List, Dict

logger = logging.getLogger()


def main() -> None:
    parser = argparse.ArgumentParser("")
    parser.add_argument("--start_idx", type=int)
    parser.add_argument("--end_idx", type=int)
    parser.add_argument("--dataset", type=str)
    parser.add_argument("--data_dir", type=str)
    parser.add_argument("--data_file_name", type=str)
    parser.add_argument("--log_dir", type=str)
    parser.add_argument("--log_file_name", type=str)
    args = parser.parse_args()

    handlers = [
        logging.FileHandler(os.path.join(args.log_dir, args.log_file_name)),
        logging.StreamHandler(),
    ]
    logging.basicConfig(
        format="[%(asctime)s] %(levelname)s: %(message)s",
        level=logging.DEBUG,
        datefmt="%d-%m-%Y %H:%M:%S",
        handlers=handlers,
    )
    logger.info(args)

    data = load_dataset(
        args.dataset,
        name="v1.1",
        split="train",
        cache_dir=".cache"
    )

    # TODO: Calculate frequency of common words in passage
    with open(os.path.join(args.data_dir, args.data_file_name), "r", encoding="utf-8") as f:
        lines = f.readlines()

    total_ratio = 0

    epochs = args.end_idx - args.start_idx + 1
    for epoch in tqdm(range(epochs)):
        line = lines[args.start_idx + epoch]
        data_dict = json.loads(line)
        if data_dict == {}:
            continue
        passage_text = data[args.start_idx +
                            epoch]["passages"]["passage_text"][0]
        passage_words = word_tokenize(passage_text)
        passage_word_num = len(passage_words)
        common_word_num = 0
        for k, v in data_dict.items():
            if int(v) == 0:
                continue
            common_word_num += int(v)
        common_word_ratio = common_word_num / passage_word_num
        total_ratio += common_word_ratio
    logger.info(f"total_ratio: {total_ratio/epochs:.6f}")


if __name__ == "__main__":
    main()
