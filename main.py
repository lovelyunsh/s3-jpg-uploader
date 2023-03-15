import os
import argparse
from s3_uploader import S3Uploader

def main(local_folder, bucket_folder, bucket_name):
    # Create an instance of S3Uploader
    uploader = S3Uploader(bucket_name=bucket_name)

    # Upload files
    success = uploader.upload_files(local_folder=local_folder, bucket_folder=bucket_folder)
    if success:
        print("All files uploaded successfully.")
    else:
        print("Failed to upload files.")

if __name__ == '__main__':
    bucket_name = 'default bucket'
    local_folder = 'local_folder/'
    bucket_folder = 'bucket_folder/'
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Upload files to S3')
    parser.add_argument('-l', '--local_folder', type=str, default=local_folder, help='Local folder path')
    parser.add_argument('-b', '--bucket_folder', type=str, default=bucket_folder, help='S3 bucket folder path')
    parser.add_argument('-bn', '--bucket_name', type=str, default=bucket_name, help='S3 bucket name')
    args = parser.parse_args()

    # Call the main function
    main(args.local_folder, args.bucket_folder, args.bucket_name)
