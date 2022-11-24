import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

cpu_df = pd.read_csv('test_BERT_performance_cpu.csv')

ns = cpu_df['n'].values.tolist()
ts_cpu = cpu_df['t'].values.tolist()

plt.figure(figsize=(10,8))
plt.grid()
plt.plot(ns, ts_cpu, color='red', label='CPU')
plt.xticks(np.arange(1, 32, 1))
plt.xlabel("n")
plt.yticks(np.arange(0, 31000, 1000))
plt.ylabel("t, ms")
plt.legend(loc='upper left')

plt.savefig('plot_BERT_perfomance_cpu.png')