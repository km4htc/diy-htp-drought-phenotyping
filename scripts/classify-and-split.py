# This script takes an input image with multiple plants and outputs an image and mask for each individual plant detected
#!/usr/bin/env python
from contextlib import contextmanager,redirect_stderr,redirect_stdout
from os import devnull
import argparse
import numpy as np
import cv2
from plantcv import plantcv as pcv
            
@contextmanager
def suppress_stdout_stderr():
    with open(devnull, 'w') as fnull:
        with redirect_stderr(fnull) as err, redirect_stdout(fnull) as out:
            yield (err, out)

# Required inputs
# image is the input image
# classifier is a pre-trained naive-bayes classifier
# size sets a minimum threshold of the number of pixels required to be considered an object; can be useful to exclude stray, incorrectly classified pixels
# outdir indicates which directory to save cropped plant images and masks to
def options():
    parser = argparse.ArgumentParser(description="Imaging processing with opencv.")
    parser.add_argument("-i", "--image", help="Input image file.", required=True)
    parser.add_argument("-c", "--classifier", help="Naive Bayes PDF file.", required=True)
    parser.add_argument("-s", "--size", help="Min object contour size to keep.", required=True)
    parser.add_argument("-o", "--outdir", help="Outdir for split imgs.", required=True)
    parser.add_argument("-D", "--debug", help="Turn on debug, prints intermediate images.", default=None)
    args = parser.parse_args()
    
def main():
	# Read image and segment plant pixels from background using a premade classifier
	img, path, filename = pcv.readimage(filename = args.image)
	classified = pcv.naive_bayes_classifier(rgb_img=img, pdf_file=args.classifier)
	mask = pcv.visualize.colorize_masks(masks=[classified['plant'], classified['background']], colors=['white', 'black'])
	mask = pcv.rgb2gray(mask)
	mask = pcv.median_blur(gray_img = mask, ksize = 8)
	# Use a mask of plant pixels to find all plant objects
	obj_contour, obj_hierarchy = pcv.find_objects(img=img, mask=mask)
	new_mask = np.zeros(np.shape(img)[:2], dtype=np.uint8)
	for c, cnt in enumerate(obj_contour):
			if len(obj_contour[c]) > int(args.size):
					cv2.fillPoly(new_mask, [np.vstack(obj_contour[c])], (255))
	
	# Save cluster audit image to file
	# This is a quick way to visualize whether two plants were detected as a single object
	cnts, hier = cv2.findContours(new_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2:]
	n = len(cnts)				
	clusters_i, contours, hierarchies = pcv.cluster_contours(img=img,
															 roi_objects=obj_contour,
															 roi_obj_hierarchy=obj_hierarchy,
															 nrow=1,
															 ncol=n)
	clustered_img = pcv.visualize.clustered_contours(cropped_img, clusters_i, contours, hierarchies, nrow=1, ncol=n)
	audit_name = 'audit-cluster/' + str.replace(filename, '.png', '_clustered.png')
	pcv.print_image(clustered_img, audit-name)

	# Iterate over kept contours, crop to plant, store to dict
	# Identifies the rectangular boundary of each plant
	cropped_images = {}
	cropped_masks = {}
	i = 0
	while i < n:
		x_coords = []
		y_coords = []
	
		m = len(cnts[i])
		j = 0
		while j < m:
			x_coords.append(cnts[i][j][0][0])
			y_coords.append(cnts[i][j][0][1])
			j = j + 1
	
		x = min(x_coords)
		w = max(x_coords) - min(x_coords)
		y = min(y_coords)
		h = max(y_coords) - min(y_coords)

		cropped_masks[x] = pcv.crop(new_mask, x, y, h, w)
		cropped_images[x] = pcv.crop(img, x, y, h, w)
  
		i = i + 1
	
	# Sort dict by min x (i.e. sort plants left to right)
	# Allows the addition of a unique plant identifier based on its left-right position
	keys = list(cropped_masks.keys())
	keys.sort()
	images = []
	masks = []
	for key in keys:
		images.append(cropped_images[key])
		masks.append(cropped_masks[key])
	
	# Save cropped images to file
	for plant in range(len(images)):
		new = '_%i_p%i.png' % (plant, plant)
		out = args.outdir + '/' + str.replace(filename, '.png', new)
		pcv.print_image(images[plant], out)
	
	for plant in range(len(masks)):
		new = '_%i_p%i_mask.png' % (plant, plant)
		out = args.outdir + '/' + str.replace(filename, '.png', new)
		pcv.print_image(masks[plant], out)
if __name__ == "__main__":
        main()
