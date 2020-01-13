from pathlib import Path

import face_recognition


def trueCount(array):
    return sum([1 for x in array if x == True])


def recognise(filename):
    tolerance = 0.55
    step = 0.0075
    iters = 0

    filenames = [path.stem for path in Path('./static/known/adults').iterdir()]
    known_images = [face_recognition.load_image_file(path) for path in Path('./static/known/adults').iterdir()]
    __known_encodings = [face_recognition.face_encodings(known_images[i]) for i in range(len(known_images))]
    known_encodings = [__known_encodings[i][0] for i in range(len(__known_encodings))] #encodings of people we know

    unknown_image = face_recognition.load_image_file(filename)
    __unknown_encoding = face_recognition.face_encodings(unknown_image) #encoding of person we want to authenticate

    if len(__unknown_encoding) == 0:
        return 'no_face'
    elif len(__unknown_encoding) > 1:
        return 'multiple_faces'
    else:
        unknown_encoding = __unknown_encoding[0]

    result = face_recognition.compare_faces(known_encodings, unknown_encoding, tolerance=tolerance)
    while trueCount(result) != 1 and 0.5 <= tolerance <= 0.7 and iters < 50:
        if trueCount(result) > 1:
            step *= -1
        tolerance += 0.0075 #modify tolerance hoping to find a (single) match
        result = face_recognition.compare_faces(known_encodings, unknown_encoding, tolerance=tolerance)
        iters += 1

    index = None
    for i in range(len(result)):
        if result[i]:
            index = i
            break

    if index is None:
        return "unknown_person"

    return filenames[index]