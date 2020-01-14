import json
from ibm_watson import VisualRecognitionV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


def getFeatFromPicture(url):
    authenticator = IAMAuthenticator('kuo4VcndKjTh-piE0JWLTF3vRmEKimmutQ7M-SrZsTRo')
    visual_recognition = VisualRecognitionV3(
        version='2018-03-19',
        authenticator=authenticator
    )

    visual_recognition.set_service_url('https://gateway.watsonplatform.net/visual-recognition/api')

    with open(url, 'rb') as images_file:
        classes = visual_recognition.classify(
            images_file=images_file,
            classifier_ids=["default"]).get_result()
        res = json.dumps(classes, indent=2)
        print(res)

    result = classes['images'][0]['classifiers'][0]['classes']

    list_result = []
    filtered_out_words = ['hotel', 'sky', 'color', 'building', 'slope', 'road']
    for r in result:
        print(r['class'])
        list_result.append([r['class'], r['score']])

    return filter(list_result, filtered_out_words)


def filter(results, filtered_words):
    new_results = []
    for result in results:
        ok = 1
        for word in filtered_words:
            if word in result[0].lower():
                ok = 0
        if ok == 1:
            new_results.append(result)
    return new_results


# l = getFeatFromPicture('tokyo2.jpg')
# print()
# print()
# print("Features:")
# print(l)
