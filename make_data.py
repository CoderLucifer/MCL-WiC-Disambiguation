import os
import json
import pandas as pd

def agg(data, label):
    lemma, text1, text2, word1, word2, lang, pos = [], [], [], [], [], [], []
    target = []
    for d, y in zip(data,label):
        text1.append(d['sentence1'])
        text2.append(d['sentence2'])
        word1.append(d['sentence1'][int(d['start1']):int(d['end1'])])
        word2.append(d['sentence2'][int(d['start2']):int(d['end2'])])
        pos.append(d['pos'])
        lemma.append(d['lemma'])
        target.append(y['tag'])
        lang.append(d['id'].split('.')[1])

    df = pd.DataFrame({'lang':lang,
                        'word1': word1,
                        'sentence1': text1,
                        'word2': word2,
                        'sentence2': text2,
                        'lemma': lemma,
                        'pos': pos,
                        'target': target})

    return df


files = os.listdir('data')

dfs = []

for f in files:
    if 'gold' not in f and 'trial' not in f:
        data = json.load(open(os.path.join('data', f)))
        gf = f.replace('data', 'gold')
        y = json.load(open(os.path.join('data', gf)))

        dfs.append(agg(data, y))


df = pd.concat(dfs, axis=0)
print(df.shape)
df = df.drop_duplicates()
print(df.shape)
df.to_csv('./csvs/data.csv', index=False)
