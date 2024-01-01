import argparse
import logging
import os
import json
from datasets import load_dataset
from call_api import get_gemini

logger = logging.getLogger()


def gen_related_question(prompt, retry=3):
    if retry == 0:
        print("Error in gen_related_question")
        exit(1)
    _to_send = f"""
    Read the given passage and raise a question related to the passage.
    Passage:
    {prompt}
    """
    try:
        res_text = get_gemini(_to_send)
    except Exception as e:
        print(e)
        print(f"Error, retry={retry}")
        return gen_related_question(prompt, retry-1)
    return res_text


def gen_answer(passage, question, retry=3):
    if retry == 0:
        print("Error in gen_answer")
        exit(1)
    _to_send = f"""
    Read the given passage and question, then answer the question.
    Passage:
    {passage}
    Question:
    {question}
    """
    try:
        res_text = get_gemini(_to_send)
    except Exception as e:
        print(e)
        print(f"Error, retry={retry}")
        return gen_answer(passage, question, retry-1)
    return res_text


def main():
    parser = argparse.ArgumentParser("")
    parser.add_argument("--genereate_num", type=int)
    parser.add_argument("--start_idx", type=int)
    parser.add_argument("--end_idx", type=int)
    parser.add_argument("--sleeptime", type=float, default=1)
    parser.add_argument("--dataset", type=str)
    parser.add_argument("--save_dir", type=str)
    parser.add_argument("--save_file_name", type=str)
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

    # TODO: Generate questions
    with open(os.path.join(args.save_dir, args.save_file_name), "w", encoding="utf-8") as f:
        epochs = args.end_idx - args.start_idx + 1
        for epoch in range(epochs):
            for i in range(args.genereate_num):
                passage_text = data[args.start_idx +
                                    epoch]["passages"]["passage_text"][0]
                question_text = gen_related_question(passage_text)
                answer_text = gen_answer(passage_text, question_text)
                _tpm_data = {
                    "id": args.start_idx + epoch,
                    "question": question_text,
                    "answer": answer_text,
                }
                f.write(json.dumps(_tpm_data) + "\n")
                logger.info(f"epoch: {epoch}, idx: {i}")
            logger.info(f"epoch: {epoch} done")


if __name__ == '__main__':
    main()
