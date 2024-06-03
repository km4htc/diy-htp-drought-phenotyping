# Scripts
This directory includes the scripts needed to run the object detection to identify individual plants, extract color data from those plants, then wrangle that data into a tidier format. Please note that these scripts may need to be modified depending on the filenames of inputs... I've done my best to make these scripts compatible with the example images provided, but have not as yet gone back through the entire pipeline start to finish; these were originally written to be paired with several intermediate bash scripts that ensured lots of metadata could be carried forward through filenames. 

The order with which the scripts should be used goes:
classify-and-split.py -> analyze-color.py -> format-color.R

The pre-trained classifiers (to discern plant from background pixels) are also included here and are required inputs for classify-and-split.py.

In particular, I relied on functions and examples from [PlantCV](https://plantcv.readthedocs.io/en/stable/).
