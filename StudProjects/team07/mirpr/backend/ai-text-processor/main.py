import nltk
from nltk.stem import WordNetLemmatizer 
from nltk.corpus import wordnet
from nltk.parse.corenlp import CoreNLPDependencyParser

import sys
import functools
import random
import traceback
import json

def isntPunct(tree):
  punctuationSymbols = ",.!?@#$%^&*()_+=-<>/\\|[]{}'\":;`~"
  return tree.label() not in punctuationSymbols

def fromModal(md):
  mdw = md[0]
  if mdw == 'should':
    return 0.6 + random.random() % 0.3
  if mdw == 'must':
    return 1.0
  if mdw == 'could':
    return 0.4 + random.random() % 0.2
  if mdw == 'may':
    return 0.2 + random.random() % 0.6
  if mdw == 'can':
    return 0.3 + random.random() % 0.3

  return random.random()

def flatten(l, acc = []):
  if type(l) is list:
    for elem in l:
      flatten(elem, acc)

    return acc
  else:
    acc.append(l)
    return acc

def flattenTree(tree):
  acc = []

  if type(tree) != str and len(tree) == 1 and type(tree[0]) == str and hasProperLabel(tree.label()[0]):
    acc.append((tree.label(), tree[0]))
  else:
    for item in tree:
      if len(item) == 0:
        continue

      if type(item) != str:
        if len(item) == 1 and type(item[0]) == str and hasProperLabel(item.label()[0]):
          acc.append((item.label(), item[0]))
        else:
          flattened = sum([flattenTree(i) for i in item], [])
          acc.extend(flattened)

  return acc

def hasProperLabel(item):
  first = item[0]

  return first == 'J' or first == 'N' or first == 'V' or first == 'R'

def lemmatizeSafe(tagType, text, lemmatizer):
  try:
    return lemmatizer.lemmatize(text, tagType)
  except:
    return lemmatizer.lemmatize(text)

def lemmatizeSafely(text, lemmatizer):
  minimal = text

  w = wordnet
  for tag in [w.ADJ, w.VERB, w.NOUN, w.ADV, None]:
    lemmatized = lemmatizeSafe(tag, text, lemmatizer)
    if len(lemmatized) < len(minimal):
      minimal = lemmatized

  return minimal

def fromVp(vpElems):
  lemmatizer = WordNetLemmatizer() 
  propSets = ' '.join(list(map(lambda node: lemmatizeSafely(node[1], lemmatizer), flattenTree(vpElems[1]))))
  condType = None
  cond = None

  # This would allow adding additional constraints to a constraint.
  # if len(vpElems) > 2:
  #   condType = vpElems[2][0][0]
  #   cond = propToRule(vpElems[2][1][:])

  return {'props': propSets, 'cond-type': condType, 'cond': cond}

def propToRule(leaves):
  prop = sentenceToRule(leaves)

  if prop:
    return prop

  try:
    npElems = list(filter(lambda x: x.label() != 'DT', leaves[0][:])) if leaves[0].label() == 'NP' else None
    np = ' '.join(functools.reduce(lambda x, y: x + y, list(map(lambda x: x.leaves(), npElems)), [])).lower()

    vpElems = leaves[1] if leaves[1].label() == 'VP' else None

    modal = fromModal(vpElems[0])

    optNeg = ''.join(vpElems[1].leaves()).lower()
    isOptNeg = optNeg == 'not' or optNeg == 'n\'t'

    propI = 2 if isOptNeg else 1
    prop = fromVp(vpElems[propI])

    chance = 1 - modal if isOptNeg else modal

    return {'np': np, 'chance': chance, 'prop': prop}
  except Exception as x:
    traceback.print_exc(file=sys.stderr)
    return {'np': 'it', 'chance': 1.0, 'prop': None}

def sentenceToRule(sentence):
  sentences = list(filter(isntPunct, sentence[:]))
  rule = []

  for s in sentences:
    if s.label() == 'CC':
      rule.append(s[0].lower())
    elif s.label() == 'S':
      rule.append(propToRule(list(filter(isntPunct, s[:]))))
    else:
      return False

  return rule

def traverseDepGraph(nodes, lemmatizer):
  weightedTags = []

  for index in nodes:
    node = nodes[index]

    weight = 1.0

    if node['word'] is not None and hasProperLabel(node['tag']):
      if 'neg' in node['deps']:
        weight = 0.0

      weightedTags.append({ 'word': lemmatizeSafely(node['word'], lemmatizer), 'weight': weight })

  return weightedTags

parser = nltk.parse.corenlp.CoreNLPParser()
rawInput = sys.argv[1]

sentence = next(parser.raw_parse(rawInput))[0]
rules = propToRule(sentence)

lemmatizer = WordNetLemmatizer() 
tags = list(set(map(lambda node: lemmatizeSafely(node[1], lemmatizer), flattenTree(sentence))))

dependency_parser = CoreNLPDependencyParser()

result = dependency_parser.raw_parse(rawInput)

depGraph = next(result)

depGraphResult = traverseDepGraph(depGraph.nodes, lemmatizer)

print(json.dumps({ 'modality': flatten(rules, []), 'depGraph': depGraphResult, 'flatTags': tags }))
