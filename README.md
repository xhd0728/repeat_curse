# Exploration of Repeat Curse

project updating, maybe do not work well.

## 0. Prepare

```shell
git clone https://github.com/xhd0728/repeat_curse.git
cd repeat_curse
conda create -n {env_name} python=3.9
pip install nltk datasets python-dotenv tqdm
conda activate {env_name}
```

```shell
cd config
# edit the file ".env.example" and fill your GOOGLE_API_KEY
mv .env.example .env
```

## 1. Generation

check before exec the script

```shell
bash script/run_generate.sh
```

## 2. Evaluation

check before exec the script

```shell
bash script/run_evaluate.sh
```