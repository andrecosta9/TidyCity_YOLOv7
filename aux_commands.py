import os


#os.system("python3 annotations.py")

#os.system("python3 train_aux.py --weights ../Models/yolov7-e6.pt --data data/faceslicenses.yaml --workers 1 --epochs 50 --batch-size 8 --img 1280 --cfg cfg/training/yolov7-e6_faceslicenses.yaml --project ../Results/yolov7-e6_5k_peoplelicenses/train")

""" os.system("python3 train_aux.py --weights ../Results/yolov7-e6e_TidyCity_7classes_LabelStudio/train/exp/weights/best.pt  --data data/tidycity.yaml --workers 2 --epochs 50 --batch-size 4 --img 1280 --cfg cfg/training/yolov7-e6e_tidycity.yaml --project ../Results/yolov7-e6e_TidyCity_7classes_LabelStudio_bagwasteOpenImages/train")
os.system("python3 test.py --weights ../Results/yolov7-e6e_TidyCity_7classes_LabelStudio_bagwasteOpenImages/train/exp/weights/best.pt --conf 0.25 --img-size 1280 --data data/tidycity.yaml --project ../Results/yolov7-e6e_TidyCity_7classes_LabelStudio_bagwasteOpenImages/test --batch-size 1")
 """
#####################
""" #Path to the directory containing the images
images_directory = '/mnt/c/Users/ccvcauser2/Desktop/Andre_FEUP/Datasets/TidyCity_8classes_LabelStudio_OpenImages_Amesterdam/train/images'

#Split dataset in train, validation and test subsets
from utils.datasets import * 

autosplit(images_directory, [0.7, 0.3, 0.0], annotated_only=False)

os.system("python3 train_aux.py --weights ../Models/yolov7-e6e.pt --data data/tidycity.yaml --workers 2 --epochs 50 --batch-size 4 --img 1280 --cfg cfg/training/yolov7-e6e_tidycity.yaml --project ../Results/yolov7-e6e_TidyCity_8classes_onlyWithPretrainedCOCO/train")

 """
 ######################
""" import csv

#Path to the files containing the labels
train_labels = '/mnt/c/Users/ccvcauser2/Desktop/Datasets/graffiti_dataset/Bounding_boxes/train_labels.csv'
test_labels = '/mnt/c/Users/ccvcauser2/Desktop/Datasets/graffiti_dataset/Bounding_boxes/test_labels.csv'
labels = '/mnt/c/Users/ccvcauser2/Desktop/Datasets/graffiti_dataset/Bounding_boxes/labels.csv'

#Create a function that reads all labels in test_labels, merge them with the labels in train_labels and save the result in labels
def MergeTrainTestLabels(train_labels, test_labels, labels):
    #Open the files
    with open(train_labels, 'r') as train_labels_file:
        with open(test_labels, 'r') as test_labels_file:
            with open(labels, 'w') as labels_file:
                #Read the files
                train_labels_reader = csv.reader(train_labels_file, delimiter=',')
                test_labels_reader = csv.reader(test_labels_file, delimiter=',')
                labels_writer = csv.writer(labels_file, delimiter=',')
                
                #Write the column names
                labels_writer.writerow(["image_name", "class_id", "xmin", "ymin", "xmax", "ymax"])
                
                #Read the train labels
                for row in train_labels_reader:
                    labels_writer.writerow(row)
                
                #Read the test labels
                for row in test_labels_reader:
                    labels_writer.writerow(row)


MergeTrainTestLabels(train_labels, test_labels, labels) """


#os.system('fiftyone convert --input-dir /mnt/c/Users/ccvcauser2/Desktop/coco-2017/train --input-type fiftyone.types.COCODetectionDataset --output-dir /mnt/c/Users/ccvcauser2/Desktop/coco-2017/ --output-type fiftyone.types.YOLOv5Dataset')

images_dir = '/mnt/c/Users/ccvcauser2/Desktop/Datasets/label_studio/batch1_2_3_corrected/images'
labels_dir = '/mnt/c/Users/ccvcauser2/Desktop/Datasets/label_studio/batch1_2_3_corrected/labels'

#Read all image names in the images directory and change it to the first 12 characters plus ".jpg"

import os
import glob

def RenameImages(images_dir):
    #Get all image names in the images directory
    images = glob.glob(images_dir + "/*.jpg")
    for image in images:
        #Get the image name
        image_name = os.path.basename(image)
        #Change the image name to the first 12? characters plus ".jpg"
        os.rename(image, os.path.join(images_dir, image_name[:36] + ".jpg"))


def RenameLabels(labels_dir):
    #Get all label names in the labels directory
    labels = glob.glob(labels_dir + "/*.txt")
    for label in labels:
        #Get the label name
        label_name = os.path.basename(label)
        #Change the label name to the first 12? characters plus ".txt"
        os.rename(label, os.path.join(labels_dir, label_name[:36] + ".txt"))

RenameImages(images_dir)
RenameLabels(labels_dir)