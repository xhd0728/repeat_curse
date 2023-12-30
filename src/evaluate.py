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

nltk.download('punkt')
nltk.download('wordnet')

stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()


def get_word_frequencies(strings: List[str]) -> Dict[str, List[int]]:
    all_text = ' '.join(strings)
    words = word_tokenize(all_text)
    # words = [stemmer.stem(word) for word in words]
    words = [lemmatizer.lemmatize(word) for word in words]
    word_freq = Counter(words)
    return word_freq


def get_common_words_frequency(strings: List[str]) -> Dict[str, List[int]]:
    common_word_freq = {}
    first_string_word_freq = get_word_frequencies([strings[0]])
    for word in first_string_word_freq.keys():
        if all(word in string for string in strings):
            common_word_freq[word] = [get_word_frequencies(
                [string])[word] for string in strings]
    return common_word_freq


def get_word_frequencies_in_passage(common_words: Dict[str, List[int]], passage: str):
    passage_words = word_tokenize(passage)
    passage_words = [lemmatizer.lemmatize(word) for word in passage_words]
    word_freq_in_passage = {word: passage_words.count(
        word) for word in common_words}
    return word_freq_in_passage


def main():
    parser = argparse.ArgumentParser("")
    parser.add_argument("--evaluate_num", type=int)
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

    # TODO: Evaluate Answer Only
    with open(os.path.join(args.data_dir, args.data_file_name), "r") as f:
        lines = f.readlines()
        epochs = args.end_idx - args.start_idx + 1
        for epoch in range(epochs):
            text_list = []
            for line in lines[epoch * args.evaluate_num: (epoch + 1) * args.evaluate_num]:
                text_list.append(json.loads(line).get("answer").lower())

            common_word_frequency = get_common_words_frequency(text_list)
            word_frequency_in_passage = get_word_frequencies_in_passage(
                common_word_frequency.keys(),
                data[epoch]["passages"]["passage_text"][0].lower()

            )
            logger.info(f"epoch={epoch} <json>" +
                        str(word_frequency_in_passage))


if __name__ == "__main__":
    main()
