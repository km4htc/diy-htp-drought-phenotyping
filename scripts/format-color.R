# This script iterates over results output from analyze color and summarizes it
# Summary data can then be used to calculate NDVI (after data from both standard and modified cameras are merged)
# NOTE! Line 119 and later will need to be modified to work with your filenames

#!/usr/bin/env Rscript
library(reshape2, warn.conflicts = F, quietly = T)
library(dplyr, warn.conflicts = F, quietly = T)
options(dplyr.summarise.inform = FALSE)
library(e1071)

# Custom functions to be used
# Get the mode
mode <- function(nums) {
    which.max(tabulate(nums))
}

# Retrieve single-value traits
svt <- function(x) {
    hcm <- which(x$trait == 'hue_circular_mean')
    hcm <- x$value[hcm]
    hcs <- which(x$trait == 'hue_circular_std')
    hcs <- x$value[hcs]
    hmed <- which(x$trait == 'hue_median')
    hmed <- x$value[hmed]
    l <- as.data.frame(c(hcm, hcs, hmed))
    rownames(l) <- c("hue_circular_mean", "hue_circular_stdev", "hue_median")
    colnames(l) <- "V1"
    return(l)
}

# Retrieve multi-value trait descriptive stats
mvt <- function(x, ...) {
    # Subset to a particular multi-value trait
    subs <- deparse(substitute(...))
    df <- subset(x, eval(parse(text = subs)))
    # Tabulate the label column by the number of pixels w that label (i.e. value)
    # Makes a column of values that represents the frequency distribution
    # Get summary stats
    df$label <- as.numeric(df$label)
    freqs <- as.data.frame(rep(df$label, df$value*100000))
    colnames(freqs) <- "freqs"
    freqs$freqs <- as.numeric(freqs$freqs)
    summary <- freqs %>% 
        summarize_at(.vars = "freqs", 
                     .funs=c(mean=mean, median=median, kurt=kurtosis, sd=sd, mode=mode))
    return(summary)
}

mvt_format <- function(x, lab) {
    x <- t(x)
    rownames(x) <- paste0(lab,rownames(x))
    return(as.data.frame(x))
}

# A summary stat function to iterate over each file
summ_fun <- function(x) {
    
    # Get all the multi-value traits
    b <- mvt(x, trait=='blue_frequencies')
    b <- mvt_format(b, lab='b.')
    g <- mvt(x, trait=='green_frequencies')
    g <- mvt_format(g, lab='g.')
    r <- mvt(x, trait=='red_frequencies')
    r <- mvt_format(r, lab='r.')
    l <- mvt(x, trait=='lightness_frequencies')
    l <- mvt_format(l, lab='l.')
    gm <- mvt(x, trait=='green-magenta_frequencies')
    gm <- mvt_format(gm, lab='gm.')
    by <- mvt(x, trait=='blue-yellow_frequencies')
    by <- mvt_format(by, lab='by.')
    h <- mvt(x, trait=='hue_frequencies')
    h <- mvt_format(h, lab='h.')
    s <- mvt(x, trait=='saturation_frequencies')
    s <- mvt_format(s, lab='s.')
    v <- mvt(x, trait=='value_frequencies')
    v <- mvt_format(v, lab='v.')

    # Get the single-value traits
    singles <- svt(x)
    
    # Bind all rows and return
    out <- bind_rows(list(b, g, r, l, gm, by, h, s, v, singles))
    return(out)
}

# Get a list of all files
files <- list.files(path="results", 
                    pattern="*.csv", 
                    full.names=TRUE, 
                    recursive=FALSE)

# Check if any files are empty...
info = file.info(files)
empty = rownames(info[info$size == 0, ])
if (length(empty) != 0){
    cat("The following files are empty:", sprintf("%s\n", empty))
    stop("Re-analyze color for the above file(s).", call. = TRUE, domain = NULL)
    geterrmessage()
} else {
    remove(info)
    remove(empty)
}

# Make an empty df to append results to
# (runs summ.fun on first file then deletes data but keeps colnames)
out <- summ_fun(read.csv(files[1]))
out <- as.data.frame(t(out))
rownames(out) <- "plant"
out <- out[FALSE,]

# MAIN: iterate over files and generate summary stats
i = 1
while (i <= length(files)) {
    
    # Get stats for ith file
    color <- summ_fun(read.csv(files[i]))
    
    # Get the plant ID
    plant <- (strsplit(files[i], "/")[[1]][2] %>% strsplit(split="-"))[[1]][1]
    
    # Append results to summary
    color <- as.data.frame(t(color))
    rownames(color) <- plant
    out <- rbind(out, color)
    
    # Next
    i = i + 1
}

# Add chromatic coordinates
out$BCC <- out$b.mean / (out$b.mean + out$g.mean + out$r.mean)
out$GCC <- out$g.mean / (out$b.mean + out$g.mean + out$r.mean)
out$RCC <- out$r.mean / (out$b.mean + out$g.mean + out$r.mean)

write.csv(out, file = "color.csv", row.names = FALSE)
