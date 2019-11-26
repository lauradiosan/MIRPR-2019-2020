from absl import app, flags
from absl.flags import FLAGS

from yolov3_tf2.models import (
    YoloV3, YoloV3Tiny, yolo_anchors, yolo_anchor_masks,
    yolo_tiny_anchors, yolo_tiny_anchor_masks
)

flags.DEFINE_boolean('tiny', False, 'yolov3 or yolov3-tiny')
flags.DEFINE_string('weights', './checkpoints/yolov3.tf',
                    'path to weights file')
flags.DEFINE_string('darknet_weights', './data/yolov3-tiny.weights', 'darknet_weights_to_pass')
flags.DEFINE_string('classes', './data/person.names', 'path to classes file')
flags.DEFINE_enum('mode', 'fit', ['fit', 'eager_fit', 'eager_tf'],
                  'fit: model.fit, '
                  'eager_fit: model.fit(run_eagerly=True), '
                  'eager_tf: custom GradientTape')
flags.DEFINE_enum('transfer', 'none',
                  ['none', 'darknet', 'no_output', 'frozen', 'fine_tune'],
                  'none: Training from scratch, '
                  'darknet: Transfer darknet, '
                  'no_output: Transfer all but output, '
                  'frozen: Transfer and freeze all, '
                  'fine_tune: Transfer all and freeze darknet only')
flags.DEFINE_integer('size', 416, 'image size')
flags.DEFINE_integer('epochs', 2, 'number of epochs')
flags.DEFINE_integer('batch_size', 8, 'batch size')
flags.DEFINE_float('learning_rate', 1e-3, 'learning rate')
flags.DEFINE_integer('num_classes', 80, 'number of classes in the model')


flags.DEFINE_integer('initial_num_classes', 80, 'number of classes in the initial model')
flags.DEFINE_integer('custom_num_classes', 1, 'number of classes for the custom model to create')
flags.DEFINE_string('weights_path_original', './initial_weights/yolov3.tf',
                    'the path for the weights of the initial model (pre-trained)')
flags.DEFINE_string('weights_path_original_tiny', './initial_weights/yolov3-tiny.tf',
                    'the path for the weights of the initial model tiny (pre-trained)')
flags.DEFINE_string('weights_custom_path', './custom_initial_weights/yolov3.tf',
                    'the path to save the custom model with darknet weights')
flags.DEFINE_string('weights_custom_path_tiny', './custom_initial_weights/yolov3-tiny.tf',
                    'the path to save the custom model tiny with darknet weights')


def load_weights_original(model):
    if FLAGS.tiny:
        model.load_weights(FLAGS.weights_path_original_tiny)
    else:
        model.load_weights(FLAGS.weights_path_original)


def copy_darknet_weights_to_custom_model(original_model, custom_model, sub_model_layer_name='yolo_darknet'):
    sub_model = original_model.get_layer(sub_model_layer_name)
    custom_model.get_layer(sub_model_layer_name).set_weights(sub_model.get_weights())


def save_custom_model_weights(custom_model):
    if FLAGS.tiny:
        custom_model.save_weights(FLAGS.weights_custom_path_tiny)
    else:
        custom_model.save_weights(FLAGS.weights_custom_path)


def main(_argv):

    if FLAGS.tiny:
        initial_model = YoloV3Tiny(FLAGS.size,
                                   #training=True,
                                   classes=FLAGS.initial_num_classes)
        anchors = yolo_tiny_anchors
        anchor_masks = yolo_tiny_anchor_masks
        new_custom_model = YoloV3Tiny(FLAGS.size,
                                      #training=True,
                                      classes=FLAGS.custom_num_classes)
    else:
        initial_model = YoloV3(FLAGS.size,
                               #training=True,
                               classes=FLAGS.initial_num_classes)
        anchors = yolo_anchors
        anchor_masks = yolo_anchor_masks
        new_custom_model = YoloV3(FLAGS.size,
                                  #training=True,
                                  classes=FLAGS.custom_num_classes)

    load_weights_original(initial_model)
    copy_darknet_weights_to_custom_model(initial_model, new_custom_model)
    save_custom_model_weights(new_custom_model)


if __name__ == '__main__':
    try:
        app.run(main)
    except SystemExit:
        pass
