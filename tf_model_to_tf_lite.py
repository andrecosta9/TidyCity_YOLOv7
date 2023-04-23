import tensorflow as tf

converter = tf.lite.TFLiteConverter.from_saved_model('runs/train/exp11/weights/')
tflite_model = converter.convert()

with open('runs/train/exp11/weights/yolov7_tiny.tflite', 'wb') as f:
	f.write(tflite_model)