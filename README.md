# Exploration of Repeat Curse

project updating, maybe do not work well.

## 0. Prepare

```shell
git clone https://github.com/xhd0728/repeat_curse.git
cd repeat_curse
conda create -n {env_name} python=3.9
pip install nltk datasets python-dotenv
```

## 1. Generation

```shell
bash script/run_generate.sh
```

## 2. Evaluation

```shell
bash script/run_evaluate.sh
```