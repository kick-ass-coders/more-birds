#consolidate images in all directories within a parent directory to live in a new directory
def relocate_imgs(parent_directory, new_directory):
    import os

    # create list of images
    dir_list = os.listdir(parent_directory)

    for dir in dir_list[1:]:
        img_list = os.listdir(parent_directory+"/"+dir)
        
        for file in img_list:
            os.rename(parent_directory+"/"+dir+"/"+file, new_directory+"/"+file)