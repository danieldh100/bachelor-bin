# bachelor-bin

#### `html-to-corpus`
- takes a HTML-File from the resources and transform it to a uppercased, punctuation removed blob of words.
- pass this corpus to filter.py to get the reference word timings

#### `filter.py corpus.txt`:
- take a corpus text, collect all nouns and filter out the top x most common words. (plus variants of those like plurals) (x = 500 right now).
- remove short words (<3 chars) and words with "'" in them
- export those words and their counts into json (stdout)

input: result.txt

#### `sort-word-counts.py <filter.py-output.json>`
print them words sorted

#### `wordpositions <filter.py-output <sphinx4run_times.txt>`
Take a reference words file (output by `filter.py` for a given transcript) and a timing file for a recognition run (from Sphinx) and create a JSON array with words sorted by most often used in reference with found positions.
`wordpositions ~/bachelor-results/2/interesting-words.json ~/bachelor-results/2/psy2_times.txt`

In contrast to evaluating the general WER performance (possible with `wer.py` / `compare-wer.py`) this gives a WER analysis of the performance with respect to potentially more 'interesting' words, as we are only evaluating what the WER of words is that fall below the threshold of the most-common-words filter.

  (NOTE: this tool doesn't actually do this evaluation, but only supplies the necessary data for this task. see `measure-kwer-perf`)


input: `interesting-words.json` and `psy2_times.txt`
output: `positions-frequent-words-500.json`

#### `measure-kwer-performance <output-from-wordpositions>`
shows overall keyword error rate

#### `cluster`
create clusters for each word (from the output of wordpositions)

#### `wer.py reference.txt hyp.txt`
#### `compare-wer.py wer-baseline.txt wer-better.txt name-baseline name-better`

#### `pdf-to-corpus class03.pdf`

---------------- from others -------------------------
# from raw text to language model

1. `tocorpus.pl`
set of regexes to remove punctuation and excess space, producing output like

  ANARCHISM IS A POLITICAL PHILOSOPHY WHICH CONSIDERS THE STATE UNDESIRABLE UNNECESSARY AND HARMFUL AND INSTEAD PROMOTES A STATELESS SOCIETY OR ANARCHY
  THE CONCISE OXFORD DICTIONARY OF POLITICS
  IT SEEKS TO DIMINISH OR EVEN ABOLISH AUTHORITY IN THE CONDUCT OF HUMAN RELATIONS

use: `cat raw.txt | tocorpus.pl > corpus.txt`

1b. remove numbers:
`sed 's/[0-9]*//g' input.txt` (mutates)

1c. keep only alphanumeric stuff:
`sed -i.bak 's/[^a-zA-Z]/ /g' input.txt`

2. `estimate-ngram -text {corpus.txt -write-lm model.lm


