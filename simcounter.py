import time
import datetime
from tqdm import tqdm
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt
from card import *

timestamp = datetime.datetime.strftime(datetime.datetime.utcnow(), "%Y-%m-%dT%H%M%S")

N = 10000

start_time = time.perf_counter()

results = []

for i in tqdm(range(N)):
    deck = Deck()
    deck.shuffle()
    results.append(Hand(deck.take(5)).strength)
print(time.perf_counter() - start_time, "seconds")
#%% ------------

O_c = dict(Counter(results))
O_f = {k: v/N for k, v in O_c.items()}

observed = pd.DataFrame(
    {k: [v] for k, v in O_c.items()}
).T.reset_index().rename(columns={'index': 'Ident', 0: 'Observed'})

expected = pd.read_csv('pokerhands.csv')
df = expected.set_index('Ident').join(observed.set_index('Ident'))

df['Observed'] = df['Observed'].fillna(0)
df['Expected'] = df['Probability'] * N
df['p_obs'] = df['Observed'] / N

df.to_csv(f'shed/{timestamp}_simulation_results.csv',index=False)

#%% plot
with plt.style.context('fivethirtyeight'):
    df[['Probability', 'p_obs']].plot(kind='bar', log=True, edgecolor='k')
    plt.show()
