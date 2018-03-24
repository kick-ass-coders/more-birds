# import the necessary packages
from imutils import paths
import requests
import cv2
import os
import csv

def download_images(file, output_dir):
    
    
    # read in file with url list
    with open(file) as f:
        reader = csv.reader(f)
        url_list = list(reader)

    # flatten list of lists
    urls = [item for sublist in url_list for item in sublist]
    
    # set total to 0
    total = 0
    
    # loop the URLs
    for url in urls:
        try:
            # try to download the image
            r = requests.get(url, timeout=60)

            # save the image to disk
            p = os.path.sep.join([output_dir, "{}.jpg".format(
                str(total).zfill(8))])
            f = open(p, "wb")
            f.write(r.content)
            f.close()

            # update the counter
            print("[INFO] downloaded: {}".format(p))
            total += 1

        # handle if any exceptions are thrown during the download process
        except:
            print("[INFO] error downloading {}...skipping".format(p))
    
def qc_images(output_dir):
    # loop over the image paths we just downloaded
    for imagePath in paths.list_images(output_dir):
        # initialize if the image should be deleted or not
        delete = False

        # try to load the image
        try:
            image = cv2.imread(imagePath)

            # if the image is `None` then we could not properly load it
            # from disk, so delete it
            if image is None:
                delete = True

        # if OpenCV cannot load the image then the image is likely
        # corrupt so we should delete it
        except:
            print("Except")
            delete = True

        # check to see if the image should be deleted
        if delete:
            print("[INFO] deleting {}".format(imagePath))
            os.remove(imagePath)