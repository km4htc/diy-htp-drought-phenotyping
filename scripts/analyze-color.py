# Uses plantCV to extract color histograms from plants output from classify and split

#!/usr/bin/env python
# Import libraries
import os 
import argparse
import numpy as np
from plantcv import plantcv as pcv
from plantcv import parallel 

# Required inputs
# image is one of the cropped individual plant images output from classify and split
# mask is the corresponding mask to that image
# name to save the output data to
def options():
    parser = argparse.ArgumentParser(description="Imaging processing with opencv")
    parser.add_argument("-i", "--image", help="Input image file.", required=True)
    parser.add_argument("-m", "--mask", help="Mask file for input image.", required=True)
    parser.add_argument("-n", "--name", help="Simplified name for output files.", required=True)
    parser.add_argument("-D", "--debug", help="Turn on debug, prints intermediate images.", default=None)
    args = parser.parse_args()
    return args
    
def main():
	# Initialize options
	args = options()
	pcv.params.debug = args.debug

	# Read image and mask
	img, path, filename = pcv.readimage(filename = args.image)
	mask, path, filename = pcv.readimage(filename = args.mask)
	
	# Extract RGB, HSV, and LAB frequencies and plot histogram
	hist = pcv.analyze_color(rgb_img=img, mask=mask, hist_plot_type='all')
	pcv.print_image(hist, 'audit-color/{}_histogram.png'.format(args.name))

	# Save results to txt file
	pcv.print_results(filename='results/color/{}/unformatted-results.json'.format(args.name))
	
	# Format results for conversion to CSV
	parallel.process_results(job_dir='results/color/{}/'.format(args.name), json_file='results/color/{}/formatted-results.json'.format(args.name))

if __name__ == "__main__":
	main()
