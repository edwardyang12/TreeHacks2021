import os
import sys
import time
import re
import json
import random

path = "C:/Users/Edward/Desktop/BiMPM/Quora/train.tsv"
out = "C:/Users/Edward/Desktop/BiMPM/Quora/newtrain.tsv"

def collect_vocab(path):
    all_labels = set()
    all_words = set()
    infile = open(path, 'rt', encoding="utf8")
    for line in infile:

        line = line.strip()
        if line.startswith('-'): continue
        items = re.split("\t", line)
        label = items[0]
        sentence1 = re.split("\\s+",items[1].lower())
        sentence2 = re.split("\\s+",items[2].lower())
        all_labels.add(label)
        all_words.update(sentence1)
        all_words.update(sentence2)
    infile.close()
    return all_words, all_labels

def generate(input, target):
    infile = open(input, 'rt',encoding="utf8")
    outfile = open(target, "w", encoding="utf8")
    temp = ""
    id = 500000
    for line in infile:
        line = line.strip()
        if line.startswith('-'): continue
        items = re.split("\t", line)
        if temp=="":
            outfile.write(line + "\n")
        else:
            outfile.write(line + "\n")
            update = "2" + "\t" + items[1] + "\t" + temp + "\t" + str(id) + "\n"
            outfile.write(update)
        temp = items[random.choice([1,2])]
        id+=1

generate(path, out)
