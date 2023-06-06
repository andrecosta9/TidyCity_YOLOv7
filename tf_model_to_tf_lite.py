#Convert from pytorch to onnx
import os

""" path1 = '../Results/yolov7/yolov7-e6e_TidyCity_8classes_LabelStudio_OpenImages_Amesterdam_corrected/train/exp/weights/best.pt'

os.system(f'python3 export.py --weights {path1} --grid --end2end --simplify \
--topk-all 100 --iou-thres 0.65 --conf-thres 0.35 --img-size 1280 1280 --max-wh 1280') """

#Convert from onnx to tensorflow

path0 = '../Results/yolov7/yolov7-e6e_TidyCity_8classes_LabelStudio_OpenImages_Amesterdam_corrected/train/exp/weights/'
path2 = path0 + 'best.onnx'
os.system(f'onnx-tf convert -i {path2} -o {path0}')

#pip install onnx_tf
""" import onnx
from onnx_tf.backend import prepare
 
onnx_model = onnx.load(path2)
tf_rep = prepare(onnx_model)
tf_rep.export_graph(path0 + "best.pb") """

""" #Convert from tensorflow to tensorflow lite
import tensorflow as tf

converter = tf.lite.TFLiteConverter.from_saved_model('runs/train/exp11/weights/')
tflite_model = converter.convert()

with open('runs/train/exp11/weights/yolov7_tiny.tflite', 'wb') as f:
	f.write(tflite_model) """