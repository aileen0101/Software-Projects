Assignment 2: N-Grams
---------------------

### N-gram library

The main part of this assignment consists of various functions to implement an n-gram model generator. These comprise a library that can be found in the file `lib/ngrams.ml`.

### Stand-alone app

In addition, there is a stand-alone app that uses the functions in the ngram library to build an n-gram model from a training corpus and perform various tasks with it. The code can be found in `bin/main.ml`. You will not need to modify this file. 

### Testing

You will need to have good unit test coverage on your library code. The tests go in `test/main.ml`. You do not need to make any acceptance tests for the executable, but you should test any auxiliary library functions that are amenable to unit testing.

### File structure

The release code is available on CMS. Like assignments A0 and A1, we are giving you a skeleton to fill in. Your library code will go in the files `lib/bag.ml`, `lib/model.ml`, `lib/ngrams.ml`, along with any new helper functions needed. OUnit tests should go in `test/main.ml`.

### Submission and Grading
Fill out your hours worked in `lib/author.ml` and your collaborators (if any) in `lib/author.mli`. As usual, run a final `make clean; make finalcheck` and upload your zip file to CMS.
