import re, sys, collections
stopwords = set(open('../stop_words.txt').read().split(','))
with open(sys.argv[1], 'r') as f:
    words = re.findall('[a-z]{2,}', f.read().lower())
counts = collections.Counter(w for w in words if w not in stopwords)
for (w, c) in counts.most_common(25):
    print(w, '-', c)