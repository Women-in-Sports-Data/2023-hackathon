# Retrieve Hackathon Data

## Download tracking and event data files locally 
Sportradar has provided 18 games worth of NBA tracking data via an AWS S3 bucket. Each game has two files: `{game_id}_tracking.jsonl` and `{game_id}_events.jsonl`. To download all of the files from the S3 bucket to your local computer, you can use the `download_data.py` or `download_data.R` script to do so. Now it's up to you to handle and analyze!

### Using Python
Prior to running the Python script, please install the package(s) listed below.

Dependencies / Please Install (`pip install {package_name}`):
- `boto3`

To Run:
- `python3 retrieve_data/download_data.py`

### Using R
Prior to running the R script, please install the package(s) listed below. Also, you will need to update the `download_data.R` file to define the location of the downloaded files on your local computer (define the `working_directory` variable at the top of the script) and provide the AWS credentials.

Dependencies / Please Install (`install.packages("{package_name}")`):
- `aws.s3`
- `jsonlite`

To Run:
- Update the `working_directory` variable and AWS credentials at the top of the `download_data.R` file
- From the terminal run `Rscript retrieve_data/download_data.R` or execute the code in RStudio


## Map Sportradar Events Data to Publicly Available Play-By-Play Data
If you would like to enrich the events data provided by Sportradar, feel free to supplement any publicly available NBA data to do so. To help with this, we've provided a script that retrieves the events data from Sportradar and maps the data to play-by-play data from the public Python package, `py_ball` (https://github.com/basketballrelativity/py_ball).

The `map_pbp.py` script will print out json files containing the mapped events data mapped to the play-by-play data from `py_ball`

Dependencies / Please Install (`pip install {package_name}`):
- `pandas`
- `py_ball`
- `requests`

To Run:
- `python3 retrieve_data/map_pbp.py`


The `event_to_pbp.py` script is another example of accessing our data and linking with py_ball, more of a focus on accessing the data through pandas + dataframes. 
Note, this example expects data to be downloaded locally prior to running. 

Dependencies / Please Install (`pip install {package_name}`):
- `pandas`
- `py_ball`
- `requests`

To run: 
- `python3 retieve_data/event_to_pbp.py`
