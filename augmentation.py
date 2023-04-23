import albumentations as A
import cv2
import os


images_directory = "/mnt/c/Users/ccvcauser2/Desktop/open-images-v7_licenses/images/"
bboxes_directory = "/mnt/c/Users/ccvcauser2/Desktop/open-images-v7_licenses/labels/"

augmentedimages_directory = "/mnt/c/Users/ccvcauser2/Desktop/open-images-v7_licenses/images/augmented_images/"
augmentedlabels_directory = "/mnt/c/Users/ccvcauser2/Desktop/open-images-v7_licenses/labels/augmented_labels/"

class_labels = ["Vehicle registration plate"]



def calculate_newROI(image_file, image, id_aux):

    #Calculate the Bbox coordinates
    bbox_x_min = x_center - int(bbox_width/2)
    bbox_x_max = x_center + int(bbox_width/2)

    bbox_y_min = y_center - int(bbox_height/2)
    bbox_y_max = y_center + int(bbox_height/2)

    #Calculate a threshold to expand the ROI and avoid cropping the image too much
    threshold_x = bbox_x_max - bbox_x_min
    threshold_y = 2*(bbox_y_max - bbox_y_min)

    x_min_shift = 0
    x_max_shift = 0
    y_min_shift = 0
    y_max_shift = 0

    #Apply the threshold to the ROI
    x_min = bbox_x_min - threshold_x
    if x_min <= 0: 
        x_min_shift = x_min
        x_min = 0

    x_max = bbox_x_max + threshold_x
    if x_max >= width:
        x_max_shift = x_max - width
        x_max = width

    y_min = bbox_y_min - threshold_y
    if y_min <= 0: 
        y_min_shift = y_min
        y_min = 0

    y_max = bbox_y_max + threshold_y
    if y_max >= height: 
        y_max_shift = y_max - height
        y_max = height


    #print(x_min, x_max, y_min, y_max)

    #Select the ROI and save it in a new image
    roi = image[y_min:y_max, x_min:x_max]

    if id_aux == 0:
        cv2.imwrite(augmentedimages_directory + image_file, roi)
        #print("Saved image: " + augmentedimages_directory + image_file)
    else:
        cv2.imwrite(augmentedimages_directory + image_file.replace(".jpg", "_{}.jpg".format(id_aux)), roi)
        #new_image_file = image_file.replace(".jpg", "_{}.jpg".format(id_aux))
        #print("Saved image: " + augmentedimages_directory + new_image_file)
    
    calculate_newBbox(x_min, x_max, y_min, y_max, id_aux, x_min_shift, x_max_shift, y_min_shift, y_max_shift)


#Create function to calculate the new relative coordinates of the bounding box
def calculate_newBbox(x_min, x_max, y_min, y_max, id_aux, x_min_shift, x_max_shift, y_min_shift, y_max_shift):

    #Calculate the new relative coordinates of the bounding box considering the new ROI
    new_width = x_max - x_min
    new_height = y_max - y_min

    #Correct the new bounding box coordinates if the ROI was expanded
    if x_min_shift < 0 or x_max_shift > 0:
        new_center_x = (((x_max - x_min) + x_min_shift + x_max_shift)/2) / new_width
    else:
        new_center_x = ((x_max - x_min)/2)/new_width

    if y_min_shift < 0 or y_max_shift > 0:
        new_center_y = (((y_max - y_min) + y_min_shift + y_max_shift)/2) / new_height
    else:
        new_center_y = ((y_max - y_min)/2)/new_height
    
    new_width = bbox_width/new_width
    new_height = bbox_height/new_height

    #Save the new bounding box coordinates in a text file
    if id_aux == 0:
        with open(augmentedlabels_directory + image_file.replace(".jpg", ".txt"), 'w') as new_file:
            new_file.write("1 {:.6f} {:.6f} {:.6f} {:.6f}\n".format(new_center_x, new_center_y, new_width, new_height))
            #print("Saved label: " + augmentedlabels_directory + image_file.replace(".jpg", ".txt"))
    else:
        new_image_file = image_file.replace(".jpg", "_{}.txt".format(id_aux))

        with open(augmentedlabels_directory + new_image_file, 'w') as new_file:
            new_file.write("1 {:.6f} {:.6f} {:.6f} {:.6f}\n".format(new_center_x, new_center_y, new_width, new_height))
            #print("Saved label: " + augmentedlabels_directory + new_image_file)

####################
#   Main Program   #
####################

#Loop through every file in the folder bbox_directory
for file in os.listdir(bboxes_directory):
    
        #If the file is a text file
        if file.endswith(".txt"):
    
            #Get the image file name
            image_file = file.replace(".txt", ".jpg")
            #print(image_file)

            #Get the image
            image = cv2.imread(images_directory + image_file)
            height, width, channels = image.shape
    
            #Get the bounding boxes file name
            bboxes_file = bboxes_directory + file
            #print(bboxes_file)

            #Loop through every bounding box in the file
            with open(bboxes_file, 'r') as file:
                
                #count_aux = len(file.readlines())
                #print(file.readlines())
                id_aux = 0

                for line in file:
                    
                    #Split the line to get the bounding box coordinates
                    bboxes = line.split()
                    bboxes = [float(x) for x in bboxes]
                    bboxes = bboxes[1:]

                    #Convert the bounding box coordinates to absolute values
                    x_center = int(bboxes[0]*width)
                    y_center = int(bboxes[1]*height)
                    bbox_width = int(bboxes[2]*width)
                    bbox_height = int(bboxes[3]*height)
                    
                    #print(bboxes)

                    calculate_newROI(image_file, image, id_aux)       
                    
                    id_aux += 1  
                    #print(id_aux)    

            #break




""" 
#Loop through every bounding box in the file
with open(bboxes_file, 'r') as file:
    
    for line in file:

        #Split the line to get the bounding box coordinates
        bboxes = line.split()
        bboxes = [float(x) for x in bboxes]
        bboxes = bboxes[1:]

        #Convert the bounding box coordinates to absolute values
        bboxes[0] = int(bboxes[0]*width)
        bboxes[1] = int(bboxes[1]*height)
        bboxes[2] = int(bboxes[2]*width)
        bboxes[3] = int(bboxes[3]*height)
        
        print(bboxes)

        calculate_newROI(bboxes)
 """

""" transform = A.Compose([
    A.RandomCropNearBBox()
], bbox_params=A.BboxParams(format='yolo'))
 """


""" transformed = transform(image=image, bboxes=bboxes, cropping_bbox=random.choice(bboxes))
#transformed = transform(image=image)
transformed_image = transformed['image']
transformed_bboxes = transformed['bboxes']
#transformed_class_labels = transformed['class_labels']


image_name = "00a09b822d470896.jpg"
augmented_images = "/mnt/c/Users/ccvcauser2/Desktop/open-images-v7_licenses/images/augmented_images/"

cv2.imwrite(augmented_images + image_name, transformed_image)
#cv2.imshow('image', transformed_image) """



