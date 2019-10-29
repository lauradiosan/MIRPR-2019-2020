import nltk

import sys
import functools
import random
import traceback
import pprint

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

def fromVp(vpElems):
  propSets = vpElems[1]
  condType = None
  cond = None

  if len(vpElems) > 2:
    condType = vpElems[2][0][0]
    cond = propToRule(vpElems[2][1][:])

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
    traceback.print_exc(file=sys.stdout)
    return False

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

parser = nltk.parse.corenlp.CoreNLPParser()
rawInput = sys.argv[1]

# Keyword to synthesize the rules - cannot conflict with other types of output since those are
# wrapped in a Tree() sexp.
if rawInput == 'Done.':
  print('#')
  exit(0)

sentence = next(parser.raw_parse(rawInput))[0]

rules = propToRule(sentence)
pprint.pprint(rules)
