#!/usr/bin/python

import javalang
import sys
import re
import remove_comments
import argparse
import os
from pathlib import Path
from random import shuffle


modifiers = ['public', 'private', 'protected', 'static']

RE_WORDS = re.compile(r'''
    # Find words in a string. Order matters!
    [A-Z]+(?=[A-Z][a-z]) |  # All upper case before a capitalized word
    [A-Z]?[a-z]+ |  # Capitalized words / all lower case
    [A-Z]+ |  # All upper case
    \d+ | # Numbers
    .+
''', re.VERBOSE)

def clean_code(f):
    pat1 = re.compile('\/\*(.*?)\*\/',re.M|re.DOTALL)
    pat2 = re.compile('[^:\/]\/\/(.*)')
    
    pat3 = re.compile('\n')
    data = open(f, 'r', encoding='utf-8').read()
    # replace comments with empty space (pat1,pat2)
    # replace newline with special unicode character; this is because the tokenizer is weird, and we could only hijack it with single characters -- turns out most keyboard characters can appear in programs.
    return (pat3.sub(' \u2023 ', data))
    #return (pat3.sub(' \u2023 ', pat2.sub("",pat1.sub("",data))))


def split_subtokens(str):
    return [str]#[subtok for subtok in RE_WORDS.findall(str) if not subtok == '_']

def tokenizeFile(file_path):
  lines = 0
  #with open(file_path + 'method_tokens_content.txt', 'w') as method_contents_file:
  res = ""
  cfree_file = clean_code(file_path)
  cfree_file = cfree_file.split('\n')
  for line in cfree_file:
    lines += 1
    line = line.rstrip()
    #parts = line.split('|', 1)
    method_content = line
    try:
      tokens = list(javalang.tokenizer.tokenize(method_content))
      tokens = map(lambda x: "\n" if x.getValue() == '‣' else x.getValue(), tokens)
    except:
      print('ERROR in tokenizing: ' + method_content)

    res = res + ' '.join([' '.join(split_subtokens(i)) for i in tokens]) 
  
  return res

if __name__ == '__main__':
      
  # initiate the parser
  parser = argparse.ArgumentParser()  
  parser.add_argument("-f", "--file", help="file to tokenize")
  parser.add_argument("-d", "--directory", help="directory to tokenize")
  parser.add_argument("-o", "--output", help="file for output")

  args, leftovers = parser.parse_known_args()

  if args.file is not None:
    print ("Tokenizing ", args.file)

    file = str(args.file)
    s = tokenizeFile(file)
    with open(args.output, 'w') as output_file:
      output_file.write(s)
  
  if args.directory is not None:
    success = 0
    fail = 0
    print ("Tokenizing entire directory ", args.directory)
    pathlist = Path(str(args.directory)).glob('**/*.java')
    pathlist = [p for p in pathlist]
    res = ""
    
    shuffle(pathlist)
    with open(args.output, 'w') as output_file:

      for path in pathlist:
        # because path is object not string
        try:
          path_in_str = str(path)
          print("\tTokenizing ", path_in_str)
          s = tokenizeFile(path_in_str)
          output_file.write(s)
          success = success+1
        except:
          fail = fail+1
      
    print (success, " out of ",success+fail, " succeeded")

    print ("Splitting data")

    train_file = open(args.output + ".train", "w")
    test_file = open(args.output + ".test", "w")
    valid_file = open(args.output + ".valid", "w")

    original_file = open(args.output, 'r', encoding='utf-8').read()
    nlines = len(original_file)
    
    print ("Number of total lines: " , nlines)

    print ("Train lines: ", int(nlines*0.8))
    train_file.write(original_file[0:int(nlines*0.8)])

    print ("Test lines: ", abs(int(nlines*0.8) - int(nlines*0.9)))
    test_file.write(original_file[int(nlines*0.8): int(nlines*0.9)])

    print ("Validation lines: ", abs (int(nlines*0.9) - int(nlines)))
    valid_file.write(original_file[int(nlines*0.9):int(nlines)])

    train_file.close()
    test_file.close()
    valid_file.close()






