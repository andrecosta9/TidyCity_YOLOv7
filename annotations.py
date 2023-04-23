#Based on https://github.com/ibaiGorordo/OpenImages-Yolo-converter/blob/master/OIDtoYOLOconverter.py

import csv
import os
import os.path

#Path to the predictions.csv file
predictions_file = '/mnt/c/Users/ccvcauser2/Desktop/open-images-v7/train/labels/detections.csv'
#predictions_file = '/mnt/c/Users/ccvcauser2/Desktop/faceslicenses_dataset_10000/validation/labels/detections.csv'

#Path to the directory containing the images
images_directory = '/mnt/c/Users/ccvcauser2/Desktop/open-images-v7/train/images'
#images_directory = '/mnt/c/Users/ccvcauser2/Desktop/faceslicenses_dataset_10000/validation/data'

labels_directory = '/mnt/c/Users/ccvcauser2/Desktop/open-images-v7/train/labels/'
#labels_directory = '/mnt/c/Users/ccvcauser2/Desktop/faceslicenses_dataset_10000/validation/labels/'

#Path to the directory containing the classes
classes_file = '/mnt/c/Users/ccvcauser2/Desktop/open-images-v7/train/metadata/classes.csv'
#classes_file = '/mnt/c/Users/ccvcauser2/Desktop/faceslicenses_dataset_10000/validation/metadata/classes.csv'

#Path to the output file
#output_file = 'dataset.csv'

""" target_classes = ["Person", "Vehicle registration plate"] """

target_classes = ["Plastic bag", "Waste container", "Billboard", "Traffic sign", "Stop sign"]

""" target_classes = ["Plastic bag", "Waste container", "Billboard", "Traffic sign", "Stop sign",
                        "Sofa bed", "Couch", "Studio couch", "Bed", "Infant bed", "Television",
                        "Refrigerator", "Washing machine", "Home appliance", "Kitchen appliance", 
                        "Shelf", "Cabinetry", "Bathroom cabinet", "Filing cabinet", "Chest of drawers",
                        "Drawer", "Nightstand", "Table", "Coffee table", "Kitchen & dining room table", "Cupboard"] """

#List to store the rows that match the image names
matching_rows = []

target_classes_id = []
annotations_count = [0]*len(target_classes)


def SaveBoundingBoxToFile(image_id,label,x_min,x_max,y_min,y_max):
	
    if os.path.isfile(labels_directory + image_id + ".txt"):
        with open(labels_directory + image_id + ".txt", 'a') as f:
            f.write(' '.join([str(target_classes_id.index(label)),
            #f.write(' '.join([str(1),
                        str(round((x_max+x_min)/2,6)),
                        str(round((y_max+y_min)/2,6)),
                        str(round(x_max-x_min,6)),
                        str(round(y_max-y_min,6))])+'\n')

    else:
            with open(labels_directory + image_id + ".txt", 'w') as f:
                f.write(' '.join([str(target_classes_id.index(label)),
                #f.write(' '.join([str(1),
                            str(round((x_max+x_min)/2,6)),
                            str(round((y_max+y_min)/2,6)),
                            str(round(x_max-x_min,6)),
                            str(round(y_max-y_min,6))])+'\n')        
        


with open(classes_file, 'r') as csvfile:
    reader_classes = csv.reader(csvfile)

    for row_classes in reader_classes:
        
        for class_name in target_classes:

            #print(class_name)
            if row_classes[1] == class_name:  
                target_classes_id.append(row_classes[0])

print("Classes:", target_classes, " ids:", target_classes_id)
            

#Open the predictions.csv file
with open(predictions_file, 'r') as csvfile:
    reader_annotations = csv.reader(csvfile)
    
    # Get the column names from the first row
    #column_names = next(reader_annotations)
    
    # Add the column names to the matching_rows list
    #matching_rows.append(column_names)
    
    # Loop through each row
    for row in reader_annotations:
        
        # Get the image name from the first column
        image_name = row[0] + '.jpg'

        # Check if the image exists in the directory
        if os.path.exists(os.path.join(images_directory, image_name)):
            
            #Check if the annotation class is the one we are looking for
            for class_id in target_classes_id:

                if row[2] == class_id:
                    
                    annotations_count[target_classes_id.index(class_id)] += 1
                    # Add the row to the matching_rows list
                    #matching_rows.append(row)
                    SaveBoundingBoxToFile(row[0], row[2], float(row[4]), float(row[5]), float(row[6]), float(row[7]))
                    
                    break

"""            
                else:

                    if (row[2] == "/m/03bt1vf") or (row[2] == "/m/04yx4") or (row[2] == "/m/0dzct"):    #If it is "Man", "Woman" or "Human face" -> change it to "Person"
   
                        annotations_count[target_classes_id.index(class_id)] += 1
                        # Add the row to the matching_rows list
                        #matching_rows.append(row)
                        SaveBoundingBoxToFile(row[0], "/m/01g317", float(row[4]), float(row[5]), float(row[6]), float(row[7]))
                        break
"""                        

"""
# Write the matching rows to the output file
with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(matching_rows)
"""

#Split dataset in train, validation and test subsets
from utils.datasets import * 

autosplit(images_directory, [0.7, 0.3, 0.0], annotated_only=False)


print("Finished converting the annotations!")

for i in range(len(target_classes)):
    print("Class: ", target_classes[i], "   N. annotations: ", annotations_count[i])


import os

#os.system("python3 train.py --weights ../Models/yolov7-e6e.pt --data data/faceslicenses.yaml --workers 2 --epochs 50 --batch-size 32 --img 640 --cfg cfg/training/yolov7-e6e_faceslicenses.yaml --project ../Results/yolov7-e6e_5k_tidycity/train")
os.system("python3 train_aux.py --weights ../Models/yolov7-e6.pt --data data/faceslicenses.yaml --workers 1 --epochs 50 --batch-size 8 --img 1280 --cfg cfg/training/yolov7-e6_faceslicenses.yaml --project ../Results/yolov7-e6_5k_peoplelicenses/train")
