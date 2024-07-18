# DIY High-throughput drought phenotyping

This repository includes information to recreate both the hardware and software used to perform high-throughput drought phenotyping in *Improving rice drought tolerance through host-mediated microbiome selection* (https://doi.org/10.7554/eLife.97015.1).

The README covers a lot of the background and motivation for this project, but if you're more interested in the mechanics of the image segmentation and data extraction check out the [tutorial.ipynb](tutorial.ipynb) and use the binder link to follow along.
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/km4htc/diy-htp-drought-phenotyping/main?labpath=https%3A%2F%2Fgithub.com%2Fkm4htc%2Fdiy-htp-drought-phenotyping%2Fblob%2Fmain%2Ftutorial.ipynb)


Traditional drought phenotyping methods are either low-throughput and/or difficult to perform on individual plants without destructive sampling. Spectroscopy can help to overcome these inefficiencies, e.g. by using patterns of light transmission/reflectance to determine chlorophyll content or to derive vegetation indices, allowing samples to be quickly and non-destrucvtively measured. A number of tools already exist to make such measurements, though none that met the particular needs or budget for our project. For example, handheld tools such as a SPAD meter or Photosynq Multispeq are reasonably priced and are quick data collecters, but only capture data from a small portion of individual leaves and cannot be easily used on droughted plants with leaf curling symptoms. Other tools are meant for remote sensing, and employ drones or other vehicles to carry multi/hyperspectral cameras to scan entire fields; while this approach could  easily be scaled down to measure individual plants, the cameras themselves can be prohibitively expensive. 

With the goal of non-destructively phenotyping severely droughted plants in high throughput, I built my own platform using inexpensive and readily available parts. The platform consists of three parts: 1) a pair of DSLR cameras to perform the "multispectral" imaging, 2) a lightbox to control lighting for each image, and 3) a set of scripts to pair data from the two cameras, segment plants from background, then derive vegetation indices to describe a plant's drought status.

### The cameras
The sensors of typical digital cameras are sensitive to light across both the visible (400-700nm) and near-infrared (700-1300) spectra, though IR exclusion filters overlaying the sensor typically restrict the detection of light to just the visible spectrum. Light passing this filter must additionally pass through a Bayer filter--a mosaic of red, green, and blue filters--that further restrict which wavelengths of light reach the sensor and determine the RGB values for a given pixel in an image. As such, the R or Red value for a pixel represents the intensity of red visible light (~550-650nm) reflecting off the surface of the object being photographed; the Green and Blue values indicate the intensity of visible light within ~500-625nm and ~425-525nm, respectively (though there is overlap in the ranges of the red, green, and blue channels, sensitivity typically peaks in the middle of the range).

However, by removing the IR exclusion filter and replacing it with a dual-pass filter that transmits light between 400-600nm as well as between 700-800nm, the  the Red channel can be shifted to detect longer wavelengths of light, including near-infrared, while Blue and Green channels can be left relatively unaffected. Our cameras, then, included one standard DSLR and one modified with the dual-pass filter described above; by pairing the two cameras, we essentially created a multispectral camera with four channels, Red, Green, Blue, and IR. Both standard and modified cameras were Canon DSLRs, models t7 and t1, respectively, and IR exclusion filter removal and replacement was performed by Life Pixel Infrared. Both cameras were set to: shutter speed = 1/40; F-stop = 4.5; ISO = 100; Effect = Neutral; White balance = 7000K; Auto lighting optimizer = OFF.
<p align="middle">
  <img src="https://github.com/km4htc/diy-htp-drought-phenotyping/assets/27516057/0310b1bd-c8ea-45a0-8657-3c5319dcaceb" width="75%" >
</p>
<sup><sub>(A) A simplified lightbox showing full spectrum (white) and 730nm (red) LED light strips surrounding the standard and modified DSLR cameras. (B) A schematic of the portions of visible and near-infrared light that each camera's red, green, and blue channels are sensitive to. Below, black bars indicate the wavelengths of light that the full spectrum and 730nm LED strips emit; Chl FLO and Chl ABS are also included to indicate the fluorescence and absorption spectra of chlorophyll A and B. (C) Regressions of red, green, and blue channel values for images taken with the standard and modified cameras. As indicated in B, the green and blue channels of both cameras are highly correlated, whereas the red channel is not.</sub></sup>
<br/><br/>
The inclusion of IR values allowed us to derive the Normalized Difference Vegetation Index (NDVI), which is a useful measure of overall plant health and stress status. Simply put, NDVI is a measure of the difference of visible light vs infrared light reflected off a plant's surface. While healthy plants strongly absorb (red and blue) visible light via chlorophyll, more of this light will be reflected as plants become stressed and chlorophyll is lost. IR, on the other hand, tends to be strongly reflected regardless of plant stress status. As such, we quantified NDVI as the sum of the median red values from the standard (STD) and modified (MOD) cameras, i.e. visible red and IR, divided by their difference:

```math
NDVI = {MOD_{red} + STD_{red} \over MOD_{red} - STD_{red}} 
```

### The lightbox
A simple lightbox, a 2'x2'x2' cube constructed from MDF, served to control lighting conditions for each image. We painted the interior with "Black 3.0", an ultra light-absorbing black paint from Culture Hustle USA, to minimize reflectance off the surfaces of the box and used a blackout cloth to prevent light leaking through the box door and holes cut to accomodate camera lenses. We affixed alternating strips of full spectrum and 730nm LED lights the entire length of the wall opposite where plants were to be positioned; importantly, while the modified camera could detect the 730nm red light, the standard camera could not. For ease of loading plants, we added a small track made from drawer slides and a corresponding "drawer" that could be loaded with up to 5 five plants at a time (for this project we also built plywood racks to hold five plants with individual pots and water reservoirs; this could then be loaded directly onto the track). Additionally, because downstream object detection of individual plants within images was most easily accomplished if plants did not overlap one another, we built a simple divider, also painted with Black 3.0, to create a boundary between plants.
<p align="middle">
  <img src="https://github.com/km4htc/diy-htp-drought-phenotyping/assets/27516057/0e6f6777-4a3a-4250-b1fc-818044594863" width="49%" />
  <img src="https://github.com/km4htc/diy-htp-drought-phenotyping/assets/27516057/e4319410-659c-4fb2-a682-41ce47b36e68" width="49%" />
</p>
<sup><sub>Interior and exterior views of the lightbox. The interior (left) demonstrates how full spectrum and 730nm LED strips were positioned around the cameras while the exterior (right) shows how cameras were attached to the outside of the box.</sub></sup>
<br/><br/>

<p align="middle">
  <img src="https://github.com/km4htc/diy-htp-drought-phenotyping/assets/27516057/03f5a249-2abf-46c2-9c0d-1cd96df7ed1e" width=75% >
</p>
<sup><sub>Images taken with both standard (left column) and modified (right column) cameras. When red 730nm LEDs are off (top row) images from both cameras are similar; when red 730nm LEDs are on (bottom row) only the modified camera detects the additional light. Like data shown above, this demonstrates that only the red channel is significantly different between the two cameras.</sub></sup>

### The scripts
Lastly, we wrote a series of custom scripts to combine image data for individual plants across standard and modified camera images. These scripts—which relied heavily on many tools from PlantCV—can be found elsewhere in the repository, so here I'll just provide a descriptive overview. First, each image was given a unique name that included multiple fields of sample metadata; paired images from the two cameras shared the same name with the exception of a final field noting the camera origin. Within each image, plants were individually segmented from the backround via object detection, then cropped and saved as individual image files (carrying forward metadata from the original filename as well as a unique plant identifier based on its left-right position in the original image). Using masks made during object detection, median RGB values were then extracted from individual plants, and, by matching filenames, data extracted from standard and modified camera images were then paired and used to calculate NDVI using the equation given above.

# Proof of principle
We then performed several experiments to demonstrate that NDVI values derived from our high-throughput phenotyping platform are highly predictive of plant chlorophyll and water content, and can be used to track plant drought stress through time. All experiments were performed in a walk-in growth chamber with "Super Dwarf" rice as the plants of interest. 

### Experiment 1 - predicting SPAD values
In this experiment we simply asked how well our image data matched SPAD values--a measure of chlorophyll content--taken with a SPAD meter. In total we measured 119 plants after 30 days of well-watered growth, and took the average of three SPAD measurements (one each from the center of the largest leaves on the largest tillers). We were unable to perform SPAD measurements on droughted plants because it quickly became impossible to clip the SPAD meter on water stressed, curled leaves; consequently, the range of SPAD values assessed was far more narrow than we had hoped for. Interestingly, though NDVI showed a significant linear correlation with SPAD values, several other traits derived from our image data were better predictors of SPAD. These traits, including hue circular mean derived from both cameras individually or median blue-yellow values from the standard camera, more explicitly track the "greenness" of a plant. Whether these traits would remain the top predictors of SPAD across varying levels of drought is unclear, but might be answered using a different plant species whose leaves are larger or more easily manipulated while water stressed.
<p align="middle">
  <img src="https://github.com/km4htc/diy-htp-drought-phenotyping/assets/27516057/525cea9f-11bc-48a8-b958-377796c5f22f" width="50%" />
</p>
<sup><sub>The best predictors of SPAD measurements of chlorophyll content. Though NDVI was significantly correlated with SPAD values, it was outperformed by these other metrics that were also able to be derived from image data. Notably these metrics did not require both cameras; rather they could be derived from data captured by either the standard (STD) or modified (MOD) camera alone. Had we been able to make SPAD measurements across a wide range of rice drought stress, it's possible that NDVI would have outperformed the traits shown here.</sub></sup>

### Experiment 2 - predicting percent water content
To determine whether NDVI--or other traits derived from image data--could accurately predict plant water content. To do so, we grew rice in well-watered conditions for 30 days, then reduced water reservoirs to 25% original volume for two days before completely emptying reservoirs and withholding water. We  harvested 10 plants each day for 10 days, such that plants harvested later were more drought stressed than those harvested sooner. By measuring the difference between fresh and dry weights (i.e. weight at harvest and weight after a week in a drying oven), we were able to determine plant percent water content at harvest. In contrast to Experiment 1, NDVI was a top predictor of percent water content (PWC) and able to account for up to 96% of variation in PWC data. Several other traits performed similarly well, including red and green chromatic coordinate values from the modified and standard cameras, respectively.
<p align="middle">
  <img src="https://github.com/km4htc/diy-htp-drought-phenotyping/assets/27516057/0f0c4126-2fb9-4641-bdc5-49fc71412b70" width="50%" />
</p>
<sup><sub>Here, we see that multiple traits derived from image data were highly correlated with rice percent water content. As above in Experiment 1, two traits (A & B) could be derived with data from a single camera alone; however, they are slightly outperformed by NDVI (C). Another vegetation index, the Chlorophyll Index (CIG) is shown in (D). A multiple regression built on a combination of vegetation indices (VARI and TGI, Visible Atmospherically Resistant Index and Triangular Greenness Index) and single-camera traits (blue chromatic coordinate derived from the modified camera) proved to be the best predictor of rice percent water content (E).</sub></sup>

### Experiment 3 - tracking drought in time series
Lastly, we sought to demonstrate how NDVI values for individual plants change throughout drought. As in Experiment 2, rice plants were grown in well-watered conditions for 30 days before withholding then eliminating water completely; however, rather than harvesting a subset of plants each day thereafter, we imaged plants (N=30) daily for 10 days. Not only were we able to show that NDVI declines as drought becomes increasingly severe, but we also found that changes in NDVI were sensitive to--and therefore predictive of--the onset of leaf curling. To demonstrate the latter, we simply fit a smoothed spline to the curve created by an individual plant's NDVI values along 10 days of drought and calculated the point at which the slope was most negative, representing a sharp decrease in NDVI; by cross-referencing these inflection points with the image history of individual plants, we found strong correspondence with which day leaf curling was first visible.
<p align="middle">
  <img src="https://github.com/km4htc/diy-htp-drought-phenotyping/assets/27516057/9daba8a9-34a6-4e51-8846-067ff9e7d99d" width="50%" />
</p>
<sup><sub>NDVI (y-axis) decreases as drought becomes more severe (x-axis); each point represents an individual plant measured at a given time point. For each plant, we used NDVI values to predict the onset of leaf curling by finding the point at which the slope of a curve fitted to NDVI values over time was most negative. In 32/43 cases, the prediction exactly matched the day on which leaf curling was first visible; the remaining 11 cases were all within +/-1 day accuracy. To represent this in a simple manner, the above plot shows the average predicted onset of leaf curling in red and the actual onset in blue. Overall, these data show that NDVI values derived from our DIY high-throughput phenotyping were highly sensitive to changes in plant physiology in response to drought stress.</sub></sup>

# Conclusions
Here, we demonstrate that a simple, inexpensive phenotyping platform can generate data capable of tracking plant stress status through time. Importantly, 1) data can be captured for multiple plants simultaneously, 2) leaf curling and other drought stress symptoms do not preclude accurate measurements, and 3) data can be collected non-destructively. Despite only being able to calculate a single NDVI value per plant (rather than per pixel), the data were sensitive enough to detect variation in plant response, even among individuals grown in the same environment. The ability to detect subtle variation among plants was a key precursor for a large-scale selection experiment we performed in which we iteratively selected rice root microbiomes from plants with superior drought tolerance (https://doi.org/10.7554/eLife.97015.1).
