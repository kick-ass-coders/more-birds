#USAGE
#Have the list of categories you want to import in a CSV file (see category_names_example.csv)
#Then call this function and pass in that filename along with the number of images you want to scrape per category
#e.g., in a python command line:
# from bulk_image_download import *
# download_images("category_names_example.csv",20)
# it will then create new folders to contain all the photos
def download_images(category_list_file,num_images_per_category):
    import csv
    import os

    with open(category_list_file, 'r') as f:
        reader = csv.reader(f)
        category_list = list(reader)

        categories=[]

    for category in category_list:
        categories.append(category[0])

    for category in categories:
        os.system(f'python google_images_download.py -k "{category}" -l {num_images_per_category}')