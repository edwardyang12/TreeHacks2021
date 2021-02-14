import tensorflow as tf
from tensorflow import keras
#!pip install stanza
import stanza
from stanza import *

word_representation_length = 14  # Must be at least log2(number_of_lemmas)
arr_length = 50  # Must be at least 45

model = keras.Sequential([])

def loss(model_output, one_hot_label): 
  return CrossEntropy(model_output, one_hot_label)

def pr(obj=""):
    if False:
      print(obj)

index_dictionary = {"sub":[0, range(1, 8), range(8, 15)], 0:[0, range(1, 8), range(8, 15)], 
                    "verb":[15, range(16, 23), range(23, 30)], 1:[15, range(16, 23), range(23, 30)],
                    "obj":[30, range(31, 38), range(38, 45)], 2:[30, range(31, 38), range(38, 45)],
                    "misc":range(45, arr_length), 3:range(45, arr_length)}
representation_dictionary = {}
rep_counter = 0

def binary_array(num):
  arr = [0]*word_representation_length
  for i in range(len(arr)):
    if num % 2 == 1:
      arr[i] = 1
    num = num//2
  return arr

def one_hot_array(num):
  arr = [0]*word_representation_length
  arr[num] = 1
  return arr

# Takes a word or lemma as a string and converts it to an array representation
def represent(str, binary_mode=True):
  #return str
  rep = representation_dictionary.get(str, None)
  if rep is None:
    global rep_counter
    rep_counter += 10127
    if binary_mode:
      rep = binary_array(rep_counter)
      representation_dictionary[str] = rep
      return rep
    else:
      rep = one_hot_array(rep_counter)
      representation_dictionary[str] = rep
      return rep
  else:
    return rep
      

# Takes a parsed sentence and transforms it to an array for network input
def parse_to_array(parse):
  arr = [[0]*word_representation_length]*arr_length

  # Identify the subject, verb, and object
  subject = None
  verb = None
  obj = None
  for word in parse.words:
    #pr(word.deprel)
    #pr(word.upos)
    if word.deprel == "root":
      if word.upos == "VERB":
        verb = word
      elif word.upos == "NOUN" or word.upos == "ADJ" or word.upos == "PRON":
        obj = word
    elif word.deprel == "nsubj":
      subject = word
    elif word.deprel == "cop":
      verb = word
    elif word.deprel == "obj":
      obj = word
  #pr()
  if subject is not None:
    pr(subject.text)
    arr[index_dictionary["sub"][0]] = represent(subject.lemma)
  if verb is not None:
    pr(verb.text)
    arr[index_dictionary["verb"][0]] = represent(verb.lemma)
  if obj is not None:
    pr(obj.text)
    arr[index_dictionary["obj"][0]] = represent(obj.lemma) 

  #counters = {"sub":(0,1), "verb":(15,1), "obj":(30,1), "misc":(45,0)}  # Bookkeeping for the index dictionary
  
  tree = [[subject], [verb], [obj], []]
  ids = [[], [], []]

  for i in range(4):
    pr(parse.words[i])

  # Populate direct dependents
  for word in parse.words:
    if not(word == subject or word == verb or word == obj):
      parent_index = word.head - 1
      if parent_index != -1:
        parent = parse.words[parent_index]
        if parent == subject:
          tree[0].append([word])
          ids[0].append(word.id)
        elif parent == verb:
          tree[1].append([word])
          ids[1].append(word.id) 
        elif parent == obj:
          tree[2].append([word])
          ids[2].append(word.id)

  # Populate the rest
  for word in parse.words:
    pr()
    pr(word.text)
    if not(word == subject or word == verb or word == obj):
      parent_old = word
      pr("parent_old" + ", " + parent_old.text)
      parent_index = word.head - 1
      pr("parent_index" + ", " + str(parent_index))
      if parent_index != -1:
        parent = parse.words[parent_index]
        pr("parent" + ", " + parent.text)
        if not(parent == subject or parent == verb or parent == obj):
          #pr(tree)
          for limit_counter in range(100):  # Instead of "while True:"
            pr("parent" + ", " + parent.text)
            parent_index = parent.head - 1
            if parent_index == -1:
              pr("aaa")
              tree[3].append(word)
              break
            else:
              parent_old = parent
              parent = parse.words[parent_index]
              pr("bbb")
              #pr(str(parent_old.text) + ", " + str(parent.text))
              if parent == subject:
                pr("ccc")
                for i in range(len(ids[0])):
                  if ids[0][i] == parent_old.id:
                    pr("!!!!" + word.text)
                    tree[0][i].append(word)
                break
              elif parent == verb:
                pr("ddd")
                for i in range(len(ids[1])):
                  if ids[1][i] == parent_old.id:
                    tree[1][i].append(word)
                break
              elif parent == obj:
                pr("eee")
                for i in range(len(ids[2])):
                  pr(ids[2])
                  if ids[2][i] == parent_old.id:
                    pr("fff")
                    pr(tree[2])
                    pr(tree[2][i])
                    pr(i)
                    pr(parent_old.text)
                    tree[2][i+1].append(word)
                break

  pr()
  pr(tree[0][1:])
  pr()
  pr(tree[1][1:])
  pr()
  pr(tree[2][1:])
  pr()
  pr(tree[3])
  pr()

  for n in range(3):    
    for i in range(1, len(tree[n])):
      if i >= 3:
        tree[3].append(word)  # Overflow to miscellaneous
      else:
        indices = index_dictionary[n][i]
        for j in range(len(tree[n][i])):
          word = tree[n][i][j]
          if j >= len(indices):
            tree[3].append(word)  # Overflow to miscellaneous
          else:
            arr[indices[j]] = represent(word.lemma)
  
  for i in range(min(5, len(tree[3]))):
    pr(index_dictionary[3])
    arr[index_dictionary[3][i]] = represent(tree[3][i].lemma)
                    
  pr()
  pr(tree[0][1:])
  pr()
  pr(tree[1][1:])
  pr()
  pr(tree[2][1:])
  pr()
  pr(tree[3])
  pr()

  pr()
  return arr

# This section based at least partially on https://stanfordnlp.github.io/stanza/#getting-started and https://stanfordnlp.github.io/stanza/depparse.html
stanza.download("en")
nlp = stanza.Pipeline("en", processors='depparse, lemma, pos, tokenize')

def convert_to_array(text):
  parse = nlp(text).sentences[0]
  return parse_to_array(parse)

#text = "Some happy people quickly create sentences like this one in the cold cold cold cold cold cold cold cold cold cold cold cold cold cold cold cold snowy explosive miscellaneous morning"
# text = "This sentence has an object with a clause"
#parse = nlp(text).sentences[0]
#pr(parse)
#parse_to_array(parse)
# End section

