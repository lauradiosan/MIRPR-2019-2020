import os, cv2
rootdir = '.'

for subdir, _, files in os.walk(rootdir):
    new_dir_name = subdir + "_inference"
    try:
        subdir.index("video") 
        v = 0
        try:
            subdir.index("inference")
        except Exception as ex:
            v = 1
        if not v:
            raise Exception()
        os.mkdir(new_dir_name)
    except Exception as e:
        print(new_dir_name + " already exists or does not contain images")
        continue
    for file in files:
        image_path = os.path.join(subdir, file)
        img = cv2.imread(image_path) # image as numpy array
        #inference
        inference_image_path = os.path.join(new_dir_name, file)
        cv2.imwrite(inference_image_path, img)
