"""
Este código serve para fazer download do dataset, que inclui o TACO e um dataset de graffitis (https://zenodo.org/record/3238357#.ZAcVCXbP23D)

Ao correr, usando python3 test_andre.py, uma pasta chamada TACO_Graffiti-2 vai ser criada
e é aí que vai ser guardado o dataset (que está no formato YOLOv7 pytorch).

"""


import os
"""
os.system("pip install roboflow")
os.system("cd /home/andre/Desktop") #Mudar para o desktop pq ao fazer o download para dentro desta pasta depois não consigo dar push para o github

from roboflow import Roboflow

rf = Roboflow(api_key="0zi6trxO4J2tlDhqx04T")
project = rf.workspace("feup-ohds6").project("taco_graffiti")
dataset = project.version(2).download("yolov7")

"""

#os.system("pip install fiftyone")

import fiftyone as fo
import fiftyone.zoo as foz

#dataset = foz.load_zoo_dataset("quickstart")

dataset = foz.load_zoo_dataset(
              "open-images-v7",
              split="train",
              label_types=["detections"],
              classes=["Person", "Vehicle registration plate"],
              max_samples=100,
          )

dataset = foz.load_zoo_dataset(
              "open-images-v7",
              split="validation",
              label_types=["detections"],
              classes=["Person", "Vehicle registration plate"],
              max_samples=100,
          )

dataset = foz.load_zoo_dataset(
              "open-images-v7",
              split="test",
              label_types=["detections"],
              classes=["Person", "Vehicle registration plate"],
              max_samples=100,
          )


#session = fo.launch_app(dataset)

#session.wait()

