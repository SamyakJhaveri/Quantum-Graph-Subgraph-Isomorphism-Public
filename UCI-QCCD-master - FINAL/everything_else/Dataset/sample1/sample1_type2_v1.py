import re, sys, collections
stop = set(open('../stop_words.txt').read().split(','))
words = re.findall('[a-z]{2,}', open(sys.argv[1]).read().lower())
count = collections.Counter(w for w in words if w not in stop)
for (w, c) in count.most_common(25):
    print(w, '-', c)
