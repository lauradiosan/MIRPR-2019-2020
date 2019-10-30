import cv2

def get_processed_image(option):
    processed_image = 'photos/'+ option + 'Processed.jpg'

    processed_img = cv2.imread(processed_image)
    cv2.imshow('processed image', processed_img)
    print('Press any button to close the image')
    cv2.waitKey()
    cv2.destroyAllWindows()

def main():
    print("Which image would you like to process?")
    print("1, 2 or 3?")
    for x in range(1, 4):
        image = 'photos/' + str(x) + '.jpg'
        img = cv2.imread(image)
        cv2.imshow('image' + str(x), img)
    cv2.waitKey()
    cv2.destroyAllWindows()
    option = str(input())
    get_processed_image(option)

if __name__ == "__main__":
    main()