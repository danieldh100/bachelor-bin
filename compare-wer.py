#!/usr/bin/env python3
import sys
from pprint import pprint

SHOW_CORRECT_LINES = False

def filter_out_INS(result):
    return [l for l in result
        if '|' in l and l.split(' | ')[0] != 'INS']

def compare(wer_result1, wer_result2, name1, name2, template):
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
    improved = 0

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
            elif hyp1_class == 'false' and hyp2_class == 'correct':
                tr_class += ' improved'
                improved += 1
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
    out.append('<p>Worsened: {}; Improved: {}</p>'.format(worsened, improved))
    out.append('<p>{}: {}</p>'.format(name1, summary1))
    out.append('<p>{}: {}</p>'.format(name2, summary2))
    print(template.format('\n'.join(out)))

def main():
    args = sys.argv[1:]
    wer_result1 = open(args[0]).read().split('\n')[:-1]
    wer_result2 = open(args[1]).read().split('\n')[:-1]
    name1 = args[2] # for table headers
    name2 = args[3] # ...
    template = open('/home/jwerner/bachelor-bin/compare-wer/template.html').read()
    compare(wer_result1, wer_result2, name1, name2, template)

main()
