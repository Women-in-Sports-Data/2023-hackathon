# TODO: Set path to receive downloads on your local machine
working_directory <- "YOUR-WORKING-DIRECTORY-HERE"
setwd(working_directory)

# Load necessary libraries
library(aws.s3)
library(jsonlite)

# TODO: Set environment variables for bucket access
Sys.setenv(
  "AWS_ACCESS_KEY_ID" = "",
  "AWS_SECRET_ACCESS_KEY" = "",
  "AWS_DEFAULT_REGION" = "us-east-1"
)

# Set additional variables for use
bucket.name <- "sportradar-wisd-data"

# Create a dataframe with filenames and other relevant information
files.df <- get_bucket_df(bucket.name)

# Create a vector of filenames to be downloaded
filenames <- files.df$Key

# Iterate through the files and download them to your local working directory
for(filename in filenames){
  save_object(object = filename,
              bucket = bucket.name)
}

# To load a single downloaded file into R memory, you can use the following line
# To load all the downloaded files into R memory, you can loop through them again
sample.df <- stream_in(file(basename(filename)))
