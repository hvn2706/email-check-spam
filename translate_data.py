import pandas as pd
import numpy as np
import nltk
import re
import warnings

from bs4 import BeautifulSoup
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from nltk.tokenize import word_tokenize
from tqdm import tqdm
import threading

warnings.filterwarnings('ignore')

print("Loading data...")
data = pd.read_csv('dataset/completeSpamAssassin.csv')
data_translated = pd.read_csv('translated.csv')

data = data.drop(['Unnamed: 0'], axis=1)
data.rename(columns={'Label': 'Target', 'Body': 'Text'}, inplace=True)
data['Text'] = data['Text'].astype(str)
print(data.head())

data.dropna(inplace=True)

data.drop(data[data['Target'] == 0].index, inplace=True)

# data["No_of_Characters"] = data["Text"].apply(len)
# data["No_of_Words"] = data.apply(lambda row: nltk.word_tokenize(row["Text"]), axis=1).apply(len)
# data["No_of_sentence"] = data.apply(lambda row: nltk.sent_tokenize(row["Text"]), axis=1).apply(len)
# print(f"Total data before cleaning: {len(data.index)}")
# data = data[(data["No_of_Characters"] < 100000)]


# Defining a function to clean up the text
def clean(text):
    sms = re.sub('[^a-zA-Z]', ' ', text)  # Replacing all non-alphabetic characters with a space
    sms = sms.lower()  # converting to lowercase
    if sms == '':
        sms = np.nan
    return sms


def remove_tags(html):
    # parse html content
    soup = BeautifulSoup(html, "html.parser")

    for tmp_data in soup(['style', 'script']):
        # Remove tags
        tmp_data.decompose()

    # return data by retrieving the tag content
    return ' '.join(soup.stripped_strings)


data["Clean_Text"] = data["Text"].apply(remove_tags)
data["Clean_Text"] = data["Clean_Text"].apply(clean)
data = data.dropna()
print(f"Total data after cleaning: {len(data.index)}")

print("Loading model...")

model_name = "VietAI/envit5-translation"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)


def translate(input_text: str):
    input_text = 'en: ' + input_text
    output = model.generate(tokenizer([input_text], return_tensors="pt", padding=True).input_ids, max_length=512)
    trans_text = tokenizer.batch_decode(output, skip_special_tokens=True)[0]
    trans_text = trans_text.replace('vi: ', '')
    return trans_text


def translate_long_text(text):
    try:
        trans_text = ''
        if len(text) >= 100:
            words = word_tokenize(text)
            # split the text into chunks of 10 words
            chunks = [words[x:x + 10] for x in range(0, len(words), 10)]
            # translate each chunk separately
            for chunk in chunks:
                text2trans = ' '.join(chunk)
                trans_text += translate(text2trans) + ' '
        else:
            trans_text = translate(text)
        return trans_text
    except Exception as e:
        print(e)
        # print(text)
        return ''


data_trans = pd.DataFrame(columns=['translated', 'Target'])
# data_trans['Target'] = data['Target']

WORKERS = 1
worker_threads = []

print(f"Translate ...")

for i in tqdm(data.index):
    try:
        row = [translate_long_text(data.loc[i, 'Clean_Text']), data.loc[i, 'Target']]
        data_trans.loc[len(data_trans)] = row
    except Exception as e:
        print(f'index {i}: {e}')
        continue
    # if i % 10 == DATA_START % 10:
    data_trans.to_csv(f"translated.csv", mode='a', index=False, header=False)
    data_trans = pd.DataFrame(columns=['translated', 'Target'])

data_trans.to_csv(f"translated.csv", mode='a', index=False, header=False)
