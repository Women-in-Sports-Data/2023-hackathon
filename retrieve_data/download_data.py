import boto3


def main():
    """
    Simple script to download wisd sportsradar data to local directory
    """
    s3_client = boto3.client('s3')
    bucket = "sportradar-wisd-data"
    prefix = "games"

    print("Connecting to Sportradar S3 bucket...")
    response = s3_client.list_objects_v2(Bucket=bucket, Prefix=prefix)
    files = response.get("Contents")
    print(f"Success! \nDownloading {len(files)} files... \n")
    for file_num, file in enumerate(files):
        current_file = file['Key']
        split_path = current_file.split("/")
        file_to_copy = split_path[2]
        print(
            f"Downloading file: {file_to_copy} [{file_num + 1}/{len(files)}]"
        )
        s3_client.download_file(bucket, current_file, file_to_copy)
        print(f"Successfully downloaded {file_to_copy} \n")


if __name__ == "__main__":
    main()
