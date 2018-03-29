# Google Image Scraper

This scraper was used to put together the dataset of non-bird animal images for the "bird-not bird" classifier.

`bulk_image_download.py` downloaded the set of images based on keywords specified in `animal_names.csv`.

These images are all saved in separate subdirectories (one per keyword), so `consolidate_images.py` consolidated them into a single folder containing all non-bird animal images, for use in retraining the image classification model.

The google image scraping script was originally downloaded from this Github repo: https://github.com/hardikvasa/google-images-download