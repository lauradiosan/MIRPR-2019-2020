def extract_positive_reviews(reviews):
    try:
        return [R['pros'] for R in reviews if R['pros']]
    except Exception as e:
        print(e)
        return 


def extract_negative_reviews(reviews):
    try:
        return [R['cons'] for R in reviews if R['cons']]
    except Exception as e:
        print(e)
        return []

