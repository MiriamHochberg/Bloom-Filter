# Bloom Filter

## About Bloom Filters
A Bloom filter is a probabilistic data structure for fast, memory-efficient membership checks. 
Internally, it uses multiple hash functions to map elements into positions in a bit array 
rather than storing the elements themselves. This allows O(1) insertion and lookup while using 
very little space. Because different elements can map to the same bits, false positives are 
possible. However, a Bloom filter will never return a false negative.

## What This Does
Running `BloomFilter.py` builds a Bloom Filter from 100,000 words in `wordlist.txt`, then tests 
it by:
- Confirming all inserted words are found (zero false negatives)
- Checking how many never-inserted words are falsely matched
- Comparing the actual false positive rate to the theoretically projected rate

## Resources
- `wordlist.txt` from [Princeton CS Real-World Data Sets](https://introcs.cs.princeton.edu/java/data/)
- `BitHash.py` from Professor Alan J. Broder
- `BitVector.py` from Avinash Kak       
