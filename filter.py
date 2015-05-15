#!/usr/bin/env python2
from __future__ import division, print_function, unicode_literals
import sys, json
from itertools import groupby
from contractions import contractions as contractions_

from pprint import pprint
from collections import Counter

from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tag import pos_tag
lemmatizer = WordNetLemmatizer()
lemmatize = lemmatizer.lemmatize


def calculate_keyword_wers(wer_lines):
    # print('-'*60)
    groups = []
    keyfunc = lambda l: lemmatize(l[1].lower())
    data = sorted(wer_lines, key=keyfunc)
    keyword_to_wer_map = {}
    overall_count = 0
    overall_recognized = 0
    for k, g in groupby(data, keyfunc):
        group = list(g)
        count_for_word = len(group)
        overall_count += count_for_word

        count_recognized_correctly = len([l for l in group if l[0] == 'OK'])
        overall_recognized += count_recognized_correctly
        wcr = count_recognized_correctly / count_for_word
        keyword_to_wer_map[k] = {
                'count': count_for_word, 
                'recognized': count_recognized_correctly, 
                'wcr': wcr
                }
        # groups.append(group)      # Store group iterator as a list

        # keyword_to_wer_map[k] = {
    # print(json.dumps(keyword_to_wer_map, indent=4))
    # print('-'*60)
    sorted_ = sorted(keyword_to_wer_map.items(), key=lambda kw: kw[1]['count'], reverse=True)
    for keyword, values in sorted_:
        print('{} ({}/{})'.format(keyword, values['recognized'], values['count']))
    print('{}/{} keywords recognized => {}% WER.'.format(
        overall_recognized, overall_count, 100-(100*overall_recognized/overall_count)))
    # pprint(wer_lines)

# # def intersection_with_keywords(f):
keywords_file = 'keywords.txt'
keywords = set([w.lower() for w in open(keywords_file).read().split()])
#     print(keywords)
top5000words = open('top5000.txt').read().split('\n')[:-1]

def keyword_wer(frequent_keywords):
    wer_lines = unicode(open('wer.txt').read(), 'utf-8').split('\n')[1:-6]
    wer_data = [line.split('\t') for line in wer_lines]
    wer_data_keyword_filtered = \
        [(op, ref, hyp) for op, ref, hyp in wer_data if lemmatize(ref.lower()) in frequent_keywords]

    return wer_data_keyword_filtered


def frequent_keywords(f):
    """
    words that are in psychology keywords and not in 
    top1000 most frequent words
    """
    hyp = [w.lower() for w in open(f).read().split()]
    hyp = [unicode(w, 'utf-8') for w in hyp]

    hyp_tags = pos_tag(hyp)
    hyp_nouns = [w for w,pos in pos_tag(hyp) if pos in ['NNP', 'NN', '-NONE-', 'NNS']]
    lemmatized_nouns = map(lemmatize, hyp_nouns)
    counter = Counter(lemmatized_nouns)
    counts = counter.most_common()

    frequent_keywords = []
    for w,n in [(w.lower(), n) for w,n in counts]:
        if w in keywords and w not in top5000words[:1000]:
            frequent_keywords.append(w)
            # print('{} ({})'.format(w, n))

    
    return frequent_keywords


def unfrequent_nouns(f):

    top5000words_with_variants = set(top5000words)
    # print(len(top5000words))

    for w in top5000words:
        if len(w) >= 3:
            top5000words_with_variants |= {w + 's'}
            top5000words_with_variants |= {w + 'ing'}
            top5000words_with_variants |= {w + 'ting'}
            top5000words_with_variants |= {w + 'ed'}
            top5000words_with_variants |= {w + 'ped'}
            top5000words_with_variants |= {w + 'd'}
            top5000words_with_variants |= {w + '\'s'}
            top5000words_with_variants |= {w + '\'ll'}

    contractions = set(contractions_.keys())
    top5000words_with_variants |= contractions

    hyp = set([w.lower() for w in open(f).read().split()])
    hyp = hyp - top5000words_with_variants
    hyp = [unicode(w, 'utf-8') for w in hyp]

    hyp_tags = pos_tag(hyp)
    # pprint(sorted(hyp_tags))

    hyp_nouns = set(w for w,pos in pos_tag(hyp) if pos in ['NNP', 'NN', '-NONE-', 'NNS'])

    print(len(hyp_nouns))
    hyp_smaller = hyp_nouns.copy()
    for h in hyp:
        lemmatized = lemmatize(h)
        if lemmatized in top5000words_with_variants or \
          len(h) <= 3:
            hyp_smaller -= {h}

    return hyp_smaller


def main():
    args = sys.argv[1:]
    f = args[0]


    frequent_keywords_ = frequent_keywords(f)
    wer_lines = keyword_wer(frequent_keywords_)
    calculate_keyword_wers(wer_lines)
    # frequent_nouns(f)
    # intersection_with_keywords(f)

main()
