# DIY High-throughput drought phenotyping

This repository includes information and examples to recreate both the hardware and software I used to perform high-throughput drought phenotyping in *Improving rice drought tolerance through host-mediated microbiome selection* (https://doi.org/10.1101/2024.02.03.578672).

In brief, traditional drought phenotyping methods are either low-throughput and/or difficult to perform on individual plants without destructive sampling. Spectroscopy can help to overcome these inefficiencies, e.g. using patterns of light transmission/reflectance to determine chlorophyll content, derive vegetation indices, etc., but agricultural applications are typically either individual leaf clip measurements (e.g. SPAD meters, Photosynq multispeQ) or field-level remote sensing with few examples at scales in between. While leaf clip measurements and be economical and quick to make, they only capture information from subsections of individual leaves and become difficult, if not impossible to make, once leaves have started to curl from water stress. On the other hand, remote sensing protocols could easily be scaled down for individual plants, but, the multi/hyper-spectral cameras required can be quite expensive. 

To address these issues, I built my own high-throughput phenotyping platform using inexpensive, readily available parts to approximate a multispectral imaging system and derive vegetation indices that track plant performance during drouhght. The platform consists of three parts: 1) a pair of DSLR cameras to perform the "multispectral" imaging, 2) a lightbox to control lighting for each image, and 3) a set of scripts to, per plant, pair data from the two cameras, segment plants from background, then use these data to derive quantitative indices to describe a plant's drought status.

### The cameras
The sensors of typical digital cameras are sensitive to light across both the visible (400-700nm) and near-infrared (700-1300) spectra, though IR exclusion filters overlaying the sensor typically restrict the detection of light to just the visible spectrum. Light passing this filter must additionally pass through a Bayer filter--a mosaic of red, green, and blue filters--that further restricts the wavelengths of light reaching the sensor and determines the RGB values for a given pixel in an image. As such, the R or Red channel for a pixel typically represents the intensity of red, visible light (~550-650nm) reflecting off the surface of the object being photographed. However, by removing the IR exclusion filter and replacing it with a dual-pass filter that transmits light between 400-600nm as well as between 700-800nm, the Blue and Green channels can be left relatively unaffected while shifting the red channel to detect longer wavelengths of light, including near-infrared. 

Our cameras, then, included one standard DSLR and one modified with the dual-pass filter described above; in short, by pairing the two cameras, we essentially created a multispectral camera with four channels, Red, Green, Blue, and IR. 
