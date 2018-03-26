# Bird Image Classifier

Started with the model specified here: https://towardsdatascience.com/tensorflow-image-recognition-python-api-e35f7d412a70

Retrained it with the birds data (CUB-200, see below) according to steps outlined here: https://towardsdatascience.com/training-inception-with-tensorflow-on-custom-images-using-cpu-8ecd91595f26


# Usage

The bird classifier lives in a module, `bird_classifier.py`. The script contains instructions for how to implement it, but basically all you do is import all the functions from the module, specify the image, model, and labels file to use, and then when you call the classifying function it will output a dataframe containing all the category labels and associated probabilities the model predicted for the image that you passed into the function.

`bird_classifier.py` was created by adapting the original script in `scripts/label_image.py`, which specifies a bunch of arguments we don't really need... but if we need to "go back to the drawing board," well, that's kind of where the drawing board is I guess.

@TODO: Need to figure out how to put this into a Flask app....


### Caltech-UCSD Birds 200 (CUB-200) dataset

**Caltech-UCSD Birds 200 (CUB-200)** is an image dataset with photos of 200 bird species (mostly North American). For detailed information about the dataset, please see the technical report linked below.

**Number of categories:** 200

**Number of images:** 6,033

Annotations: Bounding Box, Rough Segmentation, Attributes

Citation:
Welinder P., Branson S., Mita T., Wah C., Schroff F., Belongie S., Perona, P. “Caltech-UCSD Birds 200”. California Institute of Technology. CNS-TR-2010-001. 2010.


# Readme.md for "tensorflow for poets 2"

This repo contains code for the "TensorFlow for poets 2" series of codelabs.

There are multiple versions of this codelab depending on which version 
of the tensorflow libraries you plan on using:

* For [TensorFlow Lite](https://www.tensorflow.org/mobile/tflite/) the new, ground up rewrite targeted at mobile devices
  use [this version of the codelab](https://codelabs.developers.google.com/codelabs/tensorflow-for-poets-2-tflite) 
* For the more mature [TensorFlow Mobile](https://www.tensorflow.org/mobile/mobile_intro) use 
  [this version of the codealab](https://codelabs.developers.google.com/codelabs/tensorflow-for-poets-2).


This repo contains simplified and trimmed down version of tensorflow's example image classification apps.

* The TensorFlow Lite version, in `android/tflite`, comes from [tensorflow/contrib/lite/](https://github.com/tensorflow/tensorflow/tree/master/tensorflow/contrib/lite).
* The Tensorflow Mobile version, in `android/tfmobile`, comes from [tensorflow/examples/android/](https://github.com/tensorflow/tensorflow/tree/master/tensorflow/examples/android).

The `scripts` directory contains helpers for the codelab. Some of these come from the main TensorFlow repository, and are included here so you can use them without also downloading the main TensorFlow repo (they are not part of the TensorFlow `pip` installation).

