import os
import boto3
import logging
import datetime


class S3Uploader:
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.access_key_id = 'your access key'
        self.secret_access_key = 'your secreat access key'

        # Initialize S3 client
        self.s3 = boto3.client('s3',
                              aws_access_key_id=self.access_key_id,
                              aws_secret_access_key=self.secret_access_key)

        # Initialize logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        log_file_name = datetime.datetime.now().strftime("log/%Y-%m-%d_%H-%M-%S") + '.log'
        self.log_file_path = os.path.join(os.getcwd(), log_file_name)
        
        file_handler = logging.FileHandler(self.log_file_path)
        file_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def upload_files(self, local_folder, bucket_folder):
        success = True
        jpg_found = False  # Flag to check if jpg files are present in the folder
        
        for dirpath, dirnames, filenames in os.walk(local_folder):
            for file_name in filenames:
                local_path = os.path.join(dirpath, file_name)
                if not self.upload_file(local_path, local_folder, bucket_folder):
                    success = False
                elif file_name.endswith('.jpg'):
                    jpg_found = True
                
        # If no jpg files are found, log the message
        if not jpg_found:
            self.logger.warning(f"No jpg files found in the {local_folder}")

        self.upload_log_file(bucket_folder+'log/')
        return success

    def upload_file(self, local_path, local_folder, bucket_folder):
        file_name = os.path.basename(local_path)
        if not file_name.endswith('.jpg'):
            return True
        with open(local_path, "rb") as f:
            try:
                key = os.path.join(bucket_folder, local_path[len(local_folder):]).replace('\\','/')
                self.s3.upload_fileobj(f, self.bucket_name, key)
            except Exception as e:
                self.logger.error(f"Failed to upload {file_name}: {e}")
                print(f"Failed to upload {file_name}: {e}")
                return False
            else:
                self.logger.info(f"Uploaded {file_name} to S3 at {key}")
                print(f"Uploaded {file_name} to S3 at {key}")

            # Delete the file if upload was successful
            os.remove(local_path)
            self.logger.info(f"Deleted {file_name} from local folder")

        return True

    def upload_log_file(self, bucket_folder):
        
        log_file_name = os.path.basename(self.log_file_path)
        with open(self.log_file_path, "rb") as f:
            try:
                key = os.path.join(bucket_folder, log_file_name)
                self.s3.upload_fileobj(f, self.bucket_name, key)
            except Exception as e:
                self.logger.error(f"Failed to upload log file: {e}")
                print(f"Failed to upload log file: {e}")
            else:
                # Close the log file handler
                for handler in self.logger.handlers:
                    if isinstance(handler, logging.FileHandler):
                        handler.close()
                        self.logger.removeHandler(handler)
                os.remove(self.log_file_path)

        # Upload all log files in the log directory
        log_dir = "log/"
        for log_file in os.listdir(log_dir):
            log_path = os.path.join(log_dir, log_file)
            with open(log_path, "rb") as f:
                try:
                    key = os.path.join(bucket_folder, log_file)
                    self.s3.upload_fileobj(f, self.bucket_name, key)
                except Exception as e:
                    print(e)
                else:
                    os.remove(log_path)
                
