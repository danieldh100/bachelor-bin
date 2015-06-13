# bachelor-bin

### `filter.py` (unfrequent words):
- take a recognition result (raw text), collect all nouns and filter out the top x most common words. (plus variants of those like plurals) (x = 500 right now).
- remove short words (<3 chars) and words with "'" in them
- export those words and their counts into json (stdout)

input: result.txt

### `wordpositions` 
Take a reference words timings file (output by `filter.py`) and a timing file for a recognition run (from Sphinx) and create a JSON array with words sorted by most often used in reference with found positions.
`wordpositions ~/bachelor-results/2/interesting-words.json ~/bachelor-results/2/psy2_times.txt`

input: `interesting-words.json` and `psy2_times.txt`
output: `positions-frequent-words-500.json`

### `cluster` 
create clusters for each word (from the output of wordpositions)
