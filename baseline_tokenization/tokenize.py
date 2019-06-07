#!/usr/bin/python

import javalang
import sys
import re
import remove_comments
import argparse


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
    pat2 = re.compile('\/\/(.*)')
    
    pat3 = re.compile('\n')
    data = open(f, 'r', encoding='utf-8').read()
    # replace comments with empty space (pat1,pat2)
    # replace newline with special unicode character; this is because the tokenizer is weird, and we could only hijack it with single characters -- turns out most keyboard characters can appear in programs.
    return (pat3.sub(' \u2023 ', pat2.sub("",pat1.sub("",data))))


def split_subtokens(str):
    return [str]#[subtok for subtok in RE_WORDS.findall(str) if not subtok == '_']

def tokenizeFile(file_path):
  lines = 0
  with open(file_path + 'method_tokens_content.txt', 'w') as method_contents_file:
    cfree_file = clean_code(file_path)
    cfree_file = cfree_file.split('\n')
    for line in cfree_file:
      lines += 1
      line = line.rstrip()
      #parts = line.split('|', 1)
      method_content = line
      try:
        tokens = list(javalang.tokenizer.tokenize(method_content))
      except:
        print('ERROR in tokenizing: ' + method_content)
        #tokens = method_content.split(' ')
      #if len(tokens) > 0:
      method_contents_file.write(' '.join([' '.join(split_subtokens(i.value)) for i in tokens]) + '\n')
      #else:
      #  print('ERROR in len of: ' + method_name + ', tokens: ' + str(tokens))
  print(str(lines))


if __name__ == '__main__':
      
  # initiate the parser
  parser = argparse.ArgumentParser()  
  parser.add_argument("-f", "--file", help="file to tokenize")
  parser.add_argument("-d", "--directory", help="directory to tokenize")
  args, leftovers = parser.parse_known_args()

  if args.file is not None:
    print ("Tokenizing ", args.file)

    file = str(args.file)
    tokenizeFile(file)


