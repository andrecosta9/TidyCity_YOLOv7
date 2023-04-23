"""
Este código serve para fazer download do dataset, que inclui o TACO e um dataset de graffitis (https://zenodo.org/record/3238357#.ZAcVCXbP23D)

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
import fiftyone.utils.random as four

#dataset = foz.load_zoo_dataset("quickstart")
fo.config.dataset_zoo_dir = "/mnt/c/Users/ccvcauser2/Desktop/Datasets"

""" dataset = foz.load_zoo_dataset(
              "coco-2017",
              split="train",
              label_types=["detections"],
              classes=["person"],
              max_samples=1000,
          ) """


""" dataset = foz.load_zoo_dataset(
              "open-images-v7",
              split="train",
              label_types=["detections"],
              classes=["Plastic bag", "Waste container", "Billboard", "Traffic sign", "Stop sign",
                        "Sofa bed", "Couch", "Studio couch", "Bed", "Infant bed", "Television",
                        "Refrigerator", "Washing machine", "Home appliance", "Kitchen appliance", 
                        "Shelf", "Cabinetry", "Bathroom cabinet", "Filing cabinet", "Chest of drawers",
                        "Drawer", "Nightstand", "Table", "Coffee table", "Kitchen & dining room table", "Cupboard"],
              max_samples=10000,
          ) """

""" dataset = foz.load_zoo_dataset(
              "open-images-v7",
              split="train",
              label_types=["detections"],
              classes=["Vehicle registration plate"],
              max_samples=2000,
          ) """

dataset = foz.load_zoo_dataset(
              "open-images-v7",
              split="train",
              label_types=["detections"],
              classes=["Box"],
              only_matching=True,
              max_samples=1000,
          )

""" 
# The directory containing the dataset to import
dataset_dir = "/path/to/dataset"

# The type of the dataset being imported
dataset_type = fo.types.COCODetectionDataset  # for example

# Import the dataset
dataset = fo.Dataset.from_dir(
    dataset_dir=dataset_dir,
    dataset_type=dataset_type,
) """

# Export dataset in YOLOv5 format (which is the same as YOLOv7 format)
# https://docs.voxel51.com/user_guide/dataset_creation/datasets.html#yolodataset
dataset.export(
    export_dir="/mnt/c/Users/ccvcauser2/Desktop/Datasets/tidycity_1k_cardboardbox",
    dataset_type=fo.types.YOLOv5Dataset,
    #label_field="segmentations",  # this can be omitted bc dataset only contains one `Detections` field
)

""" # A name for the dataset
name = "my-dataset"

# The directory containing the dataset to import
dataset_dir = "/mnt/c/Users/ccvcauser2/Desktop/Datasets/people_dataset_1k_uncorrected"

# The type of the dataset being imported
dataset_type = fo.types.YOLOv5Dataset  # for example

dataset = fo.Dataset.from_dir(
    dataset_dir=dataset_dir,
    dataset_type=dataset_type,
    name=name,
)

session = fo.launch_app(dataset)

session.wait() """

