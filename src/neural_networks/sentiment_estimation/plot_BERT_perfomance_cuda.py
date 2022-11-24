import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

cuda_df = pd.read_csv('test_BERT_performance_cuda.csv')

ns = cuda_df['n'].values.tolist()
ts_cuda = cuda_df['t'].values.tolist()

plt.figure(figsize=(10,8))
plt.grid()
plt.plot(ns, ts_cuda, color='blue', label='CUDA')
plt.xticks(np.arange(0, 33, 1))
plt.xlabel("n")
plt.yticks(np.arange(0, 2700, 100))
plt.ylabel("t, ms")
plt.legend(loc='upper left')
plt.savefig('plot_BERT_perfomance_cuda.png')