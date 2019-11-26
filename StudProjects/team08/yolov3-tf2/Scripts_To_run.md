#Commands To Run



### Convert pre-trained Darknet weights
```bash
# yolov3
python convert.py --weights ./data/yolov3.weights --output ./initial_weights/yolov3.tf

# yolov3-tiny
python convert.py --weights ./data/yolov3-tiny.weights --output ./initial_weights/yolov3-tiny.tf --tiny
```


###Create custom  model by copying only extractor layers

```bash
# yolov3
python load_official_weights_create_custom_model.py

# yolov3-tiny
python load_official_weights_create_custom_model.py --tiny
```

###Create custom model by copying extractor layers + pre-output layers

```bash
# yolov3
python load_all_official_weights_create_custom_model.py

# yolov3-tiny
python load_all_official_weights_create_custom_model.py --tiny
```



###Train model only from darknet config (first load)

```bash
#yolov3 
python train_custom.py --batch_size 8 --epochs 30 --first_load --transfer fine_tune


#yolov3-tiny
python train_custom.py --batch_size 8 --epochs 200 --first_load --transfer fine_tune --tiny --dataset ./images/train --val_dataset ./images/test --dataset_labels ./images/train_labels.csv --val_dataset_labels ./images/test_labels.csv
```

###Train model from latest checkpoint

```bash
#yolov3 
python train_custom.py --batch_size 8 --epochs 30 --load_from_checkpoint --transfer fine_tune

#yolov3-tiny
python train_custom.py --batch_size 8 --epochs 200 --load_from_checkpoint --transfer fine_tune --tiny --dataset ./images/train --val_dataset ./images/test --dataset_labels ./images/train_labels.csv --val_dataset_labels ./images/test_labels.csv
```

###Train original model with our dataset (first loading with pretrained weights)
python train_original_custom.py --batch_size 8 --epochs 200 --first_load --transfer fine_tune --tiny --dataset ./images/train --val_dataset ./images/test --dataset_labels ./images/train_labels.csv --val_dataset_labels ./images/test_labels.csv

###Detect image based on latest-checkpoint

```bash
#yolov3-tiny
python detect_custom.py --tiny --image ./data/street.jpg

#compare with classic command with 80 classes:
python detect.py --weights ./initial_weights/yolov3-tiny.tf --tiny --image ./data/street.jpg
```