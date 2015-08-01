#!/usr/bin/env python3
import sys
from pprint import pprint

SHOW_CORRECT_LINES = False


FILTER_BY_CORPUS = True
if FILTER_BY_CORPUS:
    X = 50
else: 
    X = 800

top5000words = open('/home/jwerner/uni/bachelor/bin/top5000.txt').read().split('\n')[:-1]
topXwords=top5000words[:X]


def percent(a,b):
    return '{:.0%}'.format(a/b)
    # return '{}/{}'.format(a, b)

def format_word(word, corpus):
    if FILTER_BY_CORPUS:
        return '<span class="topword">{}</span>'.format(word) if word not in corpus else word
    else:
        return '<span class="topword">{}</span>'.format(word) if word in topXwords else word

def filter_out_INS(result):
    return [l for l in result
        if '|' in l and l.split(' | ')[0] != 'INS']

def compare(wer_result1, wer_result2, name1, name2, template, corpus):
    # print ('HYP1: {}'.format(fname1))
    # print ('HYP2: {}'.format(fname2))

    summary1 = wer_result1[-1]
    summary2 = wer_result2[-1]
    wer_result1 = filter_out_INS(wer_result1)[1:]
    wer_result2 = filter_out_INS(wer_result2)[1:]

    out = []

    out.append('<table>')
    out.append('<tr>')
    out.append('<th>' + '</th><th>'.join(['Reference', name1, name2]) + '</th>')
    out.append('</tr>')

    worsened = 0
    worsened_words = []
    improved = 0
    improved_words = []

    for line1, line2 in zip(wer_result1, wer_result2):
        try:
            op, ref, hyp1 = line1.split(' | ');
            _, _, hyp2 = line2.split(' | ');
            hyp1 = hyp1.replace('*', '.')
            hyp2 = hyp2.replace('*', '.')
            hyp1_class = 'correct' if hyp1 == ref else 'false'
            hyp2_class = 'correct' if hyp2 == ref else 'false'

            # leave out lines where both results are correct if
            # the flag is set
            if not SHOW_CORRECT_LINES and hyp1_class == 'correct' and hyp2_class == 'correct': continue

            tr_class = 'interesting' if hyp1_class != hyp2_class else ''
            if hyp1_class == 'correct' and hyp2_class == 'false':
                tr_class += ' worsened'
                worsened += 1
                worsened_words.append(hyp1)
            elif hyp1_class == 'false' and hyp2_class == 'correct':
                tr_class += ' improved'
                improved += 1
                improved_words.append(hyp2)
            ref = ref.replace('*', '.')
            prefix = '# ' if hyp1 != hyp2 else '  '
            out.append('<tr class="{}">'.format(tr_class))
            out.append('<td class={}>{}</td>'.format('', ref))
            out.append('<td class={}>{}</td>'.format(hyp1_class, hyp1))
            out.append('<td class={}>{}</td>'.format(hyp2_class, hyp2))
            out.append('</tr>')
        except ValueError: # last line
            pass

    out.append('</table>')
    # this has nothing to do with good code
    # anyway. :)


    if FILTER_BY_CORPUS:
        worsened_words_top = [w for w in worsened_words 
                if not w in corpus]
        worsened_words_not_top = [w for w in worsened_words 
                if w in corpus]
        improved_words_top = [w for w in improved_words 
                if not w in corpus]
        improved_words_not_top = [w for w in improved_words 
                if w in corpus]
    else:
        worsened_words_top = [w for w in worsened_words 
            if w in topXwords]
        worsened_words_not_top = [w for w in worsened_words 
                if w not in topXwords]
        improved_words_top = [w for w in improved_words 
                if w in topXwords]
        improved_words_not_top = [w for w in improved_words 
                if w not in topXwords]

    worsened_words_sorted = \
        worsened_words_top + worsened_words_not_top
    improved_words_sorted = \
        improved_words_top + improved_words_not_top

    formatted_worsened_words = ' '.join(format_word(w, corpus) for w in worsened_words_sorted)

    formatted_improved_words = ' '.join(format_word(w, corpus) for w in improved_words_sorted)

    explanation = 'Interesting words: not in topX of the most common words. X = {}'.format(X) if not FILTER_BY_CORPUS else 'Interesting words: in corpus'
    out.append('<br/><p>{}</p>'.format(explanation))
    out.append('<br/><p><b>Worsened Words</b> ({}, {} interesting):</p><p> {}</p><p> <br/> <b>Improved Words</b> ({}, {} interesting): </p><p> {}</p>'.format(
        len(worsened_words),
        percent(len(worsened_words_not_top), len(worsened_words)),
        formatted_worsened_words,

        len(improved_words),
        percent(len(improved_words_not_top), len(improved_words)),
        formatted_improved_words
        )
    )

    out.append('<p>Worsened: {} ; Improved: {}</p>'.format(
        worsened, improved))
    out.append('<p>{}: {}</p>'.format(name1, summary1))
    out.append('<p>{}: {}</p>'.format(name2, summary2))
    print(template.format('\n'.join(out)))

def main():
    args = sys.argv[1:]
    wer_result1 = open(args[0]).read().split('\n')[:-1]
    wer_result2 = open(args[1]).read().split('\n')[:-1]
    name1 = args[2] # for table headers
    name2 = args[3] # ...
    corpus = open(args[4]).read().split()[:-1]
    corpus_without_top_words = \
        [w for w in corpus if w not in topXwords]
    template = open('/home/jwerner/uni/bachelor/bin/compare-wer/template.html').read()
    compare(wer_result1, wer_result2, name1, name2, template, corpus_without_top_words)

main()
