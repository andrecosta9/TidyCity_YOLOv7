#Este código serve para fazer download do dataset, que inclui o TACO e um dataset de graffitis (https://zenodo.org/record/3238357#.ZAcVCXbP23D)

#Ao correr, usando python3 test_andre.py, uma pasta chamada TACO_Graffiti-2 vai ser criada
#e é aí que vai ser guardado o dataset (que está no formato YOLOv7 pytorch).

import os

os.system("pip install roboflow")


from roboflow import Roboflow

rf = Roboflow(api_key="0zi6trxO4J2tlDhqx04T")
project = rf.workspace("feup-ohds6").project("taco_graffiti")
dataset = project.version(2).download("yolov7")


