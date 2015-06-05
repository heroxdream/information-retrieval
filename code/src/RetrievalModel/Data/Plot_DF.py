__author__ = 'Xuan Han'

import matplotlib.pyplot as plt
import pickle


f = open('docs_freq.pkl', 'r')

docs_freq = pickle.load(f)

assert isinstance(docs_freq, dict)

vs = sorted(docs_freq.values(), reverse=True)

vs2 = []
for v in vs:
    vs2.append(v / 100)

d = dict()

for v in vs2:
    if not d.has_key(v):
        d[v] = 1
    d[v] += 1

print len(d)

d.pop(0)
d.pop(1)
d.pop(2)

x = []
y = []
for e in d:
    x.append(e)
    y.append(d[e])
    print(e, d[e])

plt.plot(x, y)
plt.show()


