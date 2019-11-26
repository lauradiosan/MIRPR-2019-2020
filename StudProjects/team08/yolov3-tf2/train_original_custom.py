from absl import app, flags, logging
from absl.flags import FLAGS
import tensorflow as tf
import numpy as np
import cv2
from tensorflow.keras.callbacks import (
    ReduceLROnPlateau,
    EarlyStopping,
    ModelCheckpoint,
    TensorBoard
)
from yolov3_tf2.models import (
    YoloV3, YoloV3Tiny, YoloLoss,
    yolo_anchors, yolo_anchor_masks,
    yolo_tiny_anchors, yolo_tiny_anchor_masks
)
from yolov3_tf2.utils import freeze_all
import yolov3_tf2.dataset as dataset


flags.DEFINE_string('dataset', './images/train', 'path to dataset')
flags.DEFINE_string('val_dataset', './images/train_labels.csv', 'path to validation dataset')
flags.DEFINE_string('dataset_labels', './images/test', 'labels path')
flags.DEFINE_string('val_dataset_labels', './images/test_labels.csv', 'labels path')

flags.DEFINE_boolean('tiny', False, 'yolov3 or yolov3-tiny')
flags.DEFINE_string('weights', './checkpoints/yolov3.tf',
                    'path to weights file')
flags.DEFINE_string('classes', './data/coco.names', 'path to classes file')
flags.DEFINE_enum('transfer', 'none',
                  ['none', 'fine_tune'],
                  'none: Training from scratch, '
                  'fine_tune: Transfer all and freeze darknet only')
flags.DEFINE_integer('size', 416, 'image size')
flags.DEFINE_integer('epochs', 2, 'number of epochs')
flags.DEFINE_integer('batch_size', 8, 'batch size')
flags.DEFINE_float('learning_rate', 1e-3, 'learning rate')
flags.DEFINE_integer('num_classes', 80, 'number of classes in the model')



flags.DEFINE_boolean('load_from_checkpoint', False, 'Tell whether we load from the latest checkpoint or not')
flags.DEFINE_boolean('first_load', False, 'Tell whether we load from the initial full model or not')
flags.DEFINE_string('weights_first_load', './initial_weights/yolov3.tf',
                    'the path for loading the initial weights from a full model tiny')
flags.DEFINE_string('weights_first_load_tiny', './initial_weights/yolov3-tiny.tf',
                    'the path for loading the initial weights from a full model tiny')

YOLOV3_LAYER_LIST = [
    'yolo_darknet',
    'yolo_conv_0',
    'yolo_output_0',
    'yolo_conv_1',
    'yolo_output_1',
    'yolo_conv_2',
    'yolo_output_2',
]

YOLOV3_TINY_LAYER_LIST = [
    'yolo_darknet',
    'yolo_conv_0',
    'yolo_output_0',
    'yolo_conv_1',
    'yolo_output_1',
]


def load_weights_first(full_model, training_model):
    if FLAGS.tiny:
        full_model.load_weights(FLAGS.weights_first_load_tiny)
        layers = YOLOV3_TINY_LAYER_LIST
    else:
        full_model.load_weights(FLAGS.weights_first_load)
        layers = YOLOV3_LAYER_LIST

    for layer in layers:
        training_model.get_layer(layer).set_weights(full_model.get_layer(layer).get_weights())
    return training_model
    
def load_model():
    if FLAGS.tiny:
        full_model = YoloV3Tiny(FLAGS.size,
                                # training=True,
                                classes=FLAGS.num_classes)
        training_model = YoloV3Tiny(FLAGS.size,
                                    training=True,
                                    classes=FLAGS.num_classes)
    else:
        full_model = YoloV3(FLAGS.size,
                            # training=True,
                            classes=FLAGS.num_classes)
        training_model = YoloV3(FLAGS.size,
                                training=True,
                                classes=FLAGS.num_classes)

    if FLAGS.first_load:
        training_model = load_weights_first(full_model, training_model)
        return training_model
    elif FLAGS.load_from_checkpoint:
        checkpoint_path = "initial_weights/yolov3.tf"
        checkpoint_dir = os.path.dirname(checkpoint_path)
        latest_train = tf.train.latest_checkpoint(checkpoint_dir)
        training_model.load_weights(latest_train)

    if FLAGS.transfer == 'fine_tune':
        # freeze darknet
        darknet = training_model.get_layer('yolo_darknet')
        freeze_all(darknet)

    return training_model
    
    
def main(_argv):
    physical_devices = tf.config.experimental.list_physical_devices('GPU')
    if len(physical_devices) > 0:
        tf.config.experimental.set_memory_growth(physical_devices[0], True)

    training_model = load_model()

    if FLAGS.tiny:
        anchors = yolo_tiny_anchors
        anchor_masks = yolo_tiny_anchor_masks
    else:
        anchors = yolo_anchors
        anchor_masks = yolo_anchor_masks

    train_dataset = dataset.load_dataset(FLAGS.dataset, FLAGS.dataset_labels)
    train_dataset = train_dataset.shuffle(buffer_size=1024)  # TODO: not 1024
    train_dataset = train_dataset.batch(FLAGS.batch_size)
    train_dataset = train_dataset.map(lambda x, y: (
        dataset.transform_images(x, FLAGS.size),
        dataset.transform_targets(y, anchors, anchor_masks, FLAGS.num_classes)))
    train_dataset = train_dataset.prefetch(
        buffer_size=tf.data.experimental.AUTOTUNE)

    val_dataset = dataset.load_dataset(FLAGS.val_dataset, FLAGS.val_dataset_labels)
    val_dataset = val_dataset.batch(FLAGS.batch_size)
    val_dataset = val_dataset.map(lambda x, y: (
        dataset.transform_images(x, FLAGS.size),
        dataset.transform_targets(y, anchors, anchor_masks, FLAGS.num_classes)))

    

    optimizer = tf.keras.optimizers.Adam(lr=FLAGS.learning_rate)
    loss = [YoloLoss(anchors[mask], classes=FLAGS.num_classes)
            for mask in anchor_masks]

    
    optimizer = tf.keras.optimizers.Adam(lr=FLAGS.learning_rate)
    loss = [YoloLoss(anchors[mask], classes=FLAGS.num_classes)
            for mask in anchor_masks]

    training_model.compile(
        optimizer=optimizer,
        loss=loss)

    callbacks = [
        # ReduceLROnPlateau(monitor='val_loss', factor=0.75, patience=5, verbose=1, min_lr=0.001),
        # EarlyStopping(monitor='val_loss', min_delta=0, patience=10, verbose=1),
        ModelCheckpoint('checkpoints/yolov3_train_{epoch}.tf',
                        verbose=1,
                        save_weights_only=True,
                        period=1),

        TensorBoard(log_dir='logs')
    ]

    history = training_model.fit(
        train_dataset,
        epochs=FLAGS.epochs,
        callbacks=callbacks,
        validation_data=val_dataset)


if __name__ == '__main__':
    try:
        app.run(main)
    except SystemExit:
        pass
