from monkeylearn import MonkeyLearn

import sys
import json

def get_intent():
    ml = MonkeyLearn('de48008ab4f3aa99ef9e7614ce7fe61270be7179')
    model_id = 'cl_Hy3wormR'
    result = ml.classifiers.classify(model_id, [sys.argv[1]])
    print(json.dumps((result.body[0])))
    return result

get_intent()
