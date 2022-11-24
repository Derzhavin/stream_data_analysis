from BERT import SentimentEstimator
from pathlib import Path
import random
import time
import statistics
import pandas as pd
import numpy as np
import torch

NUMBER_TESTS = 3
PAUSE_AFTER_TEST_SEC = 0.05
MAX_SENTENCES_NUM = 32


torch.set_num_threads(6)


def read_sentences(n, sentences_dir_path):
    txt_files = list(Path(sentences_dir_path).glob('*.txt'))
    random.shuffle(txt_files)
    sentences = []
    for txt_file in txt_files[:n]:
        with open(txt_file, 'r') as f:
            data = f.read()
            sentences.append(data)

    return sentences


ns = [i for i in range(1, MAX_SENTENCES_NUM, 1)]

sentences = read_sentences(MAX_SENTENCES_NUM, '/home/denis/stream_data_analysis/src/neural_networks/sentiment_estimation/.data/imdb/aclImdb/test/neg')

p = SentimentEstimator(model_path='./sentiment_estimation_BERT.pt', target_device='cpu')
p.predict(sentences[:1])

ts_cpu = []
for n in ns:
    t_list = []
    for i in range(NUMBER_TESTS):
        t_begin = time.time()
        p.predict(sentences[:n])
        t_diff = (time.time() - t_begin) * 1000
        t_list += [t_diff]
        time.sleep(PAUSE_AFTER_TEST_SEC)
    ts_cpu += [int(statistics.mean(t_list))]
    print(f'Testing CPU: {n}/{MAX_SENTENCES_NUM}, {n * 100 / MAX_SENTENCES_NUM}%')

del p

p = SentimentEstimator(model_path='./sentiment_estimation_BERT.pt', target_device='cuda')
p.predict(sentences[:1])

ts_cuda = []
for n in ns:
    t_list = []
    for i in range(NUMBER_TESTS):
        t_begin = time.time()
        p.predict(sentences[:n])
        t_diff = (time.time() - t_begin) * 1000
        t_list += [t_diff]
        time.sleep(PAUSE_AFTER_TEST_SEC)
    ts_cuda += [int(statistics.mean(t_list))]
    print(f'Testing CUDA: {n}/{MAX_SENTENCES_NUM}, {n * 100 / MAX_SENTENCES_NUM}%')

ns_column = np.array(ns)
ts_cuda_column = np.array(ts_cuda)
ts_cpu_column = np.array(ts_cpu)

df = pd.DataFrame({"n" : ns, "t" : ts_cuda_column})
df.to_csv("test_BERT_performance_cuda.csv", index=False)

df = pd.DataFrame({"n" : ns, "t" : ts_cpu_column})
df.to_csv("test_BERT_performance_cpu.csv", index=False)