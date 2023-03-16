#Based on https://github.com/ibaiGorordo/OpenImages-Yolo-converter/blob/master/OIDtoYOLOconverter.py

import csv
import os
import os.path

#Path to the predictions.csv file
predictions_file = '/home/andre/fiftyone/open-images-v7/train/labels/detections.csv'

#Path to the directory containing the images
image_directory = '/home/andre/fiftyone/open-images-v7/train/data'

labels_directory = '/home/andre/fiftyone/open-images-v7/train/labels/'

#Path to the directory containing the classes
classes_file = '/home/andre/fiftyone/open-images-v7/train/metadata/classes.csv'

#Path to the output file
output_file = 'dataset.csv'

target_classes = ['Person', 'Vehicle registration plate']

#List to store the rows that match the image names
matching_rows = []

target_classes_id = []


def SaveBoundingBoxToFile(image_id,label,x_min,x_max,y_min,y_max):
	
    if os.path.isfile(labels_directory + image_id + ".txt"):
        with open(labels_directory + image_id + ".txt", 'a') as f:
            f.write(' '.join([str(target_classes_id.index(label)),
                        str(round((x_max+x_min)/2,6)),
                        str(round((y_max+y_min)/2,6)),
                        str(round(x_max-x_min,6)),
                        str(round(y_max-y_min,6))])+'\n')

    else:
            with open(labels_directory + image_id + ".txt", 'w') as f:
                f.write(' '.join([str(target_classes_id.index(label)),
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
    column_names = next(reader_annotations)
    
    # Add the column names to the matching_rows list
    matching_rows.append(column_names)
    
    # Loop through each row
    for row in reader_annotations:
        
        # Get the image name from the first column
        image_name = row[0] + '.jpg'

        # Check if the image exists in the directory
        if os.path.exists(os.path.join(image_directory, image_name)):
            
            #Check if the annotation class is the one we are looking for
            for class_id in target_classes_id:
                if class_id == row[2]:
                    # Add the row to the matching_rows list
                    matching_rows.append(row)
                    SaveBoundingBoxToFile(row[0], row[2], float(row[4]), float(row[5]), float(row[6]), float(row[7]))
            

# Write the matching rows to the output file
with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(matching_rows)

print("Finished converting the annotations!")