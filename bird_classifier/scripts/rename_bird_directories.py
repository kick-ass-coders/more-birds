import os, sys

#Set working directory to where the birds live
os.chdir('tf_files/bird_images_full')

names=os.listdir(os.getcwd())[1:]
print(names)

for name in names:
    renamed_text=name.split(".")[1]
    renamed_text=renamed_text.replace("_", " ")
    os.rename(name,renamed_text)

print "WE DID IT Y'ALL"