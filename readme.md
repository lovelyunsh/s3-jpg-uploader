이 코드는 지정한 로컬 폴더와 그 하위 폴더에 있는 jpg 파일들을
AWS S3 버킷에 동일한 폴더 구조로 업로드하는 Python 코드입니다.

## 사용법

s3_uploader.py에 있는 access_key_id와 secret_access_key를
S3권한이 있는 사용자 계정으로 수정하여야 합니다.

이 코드를 실행하기 위해서는 다음과 같은 세 가지 인자를 입력해야 합니다.

- `--local_folder`: 로컬 폴더의 경로
- `--bucket_folder`: S3 버킷의 폴더 경로
- `--bucket_name`: S3 버킷의 이름

예를 들어, 다음과 같이 실행할 수 있습니다.

```shell
python s3_upload.py --local_folder /path/to/local/folder --bucket_folder /path/to/bucket/folder --bucket_name my-bucket
```
이 코드는 S3Uploader 클래스를 사용하여 로컬 폴더에 있는 jpg 파일들을 S3 버킷으로 업로드하고 로컬 파일은 삭제합니다.
업로드 중 발생하는 log파일 역시 동일한 버킷 /log 폴더에 업로드 합니다.

## 의존성

이 모듈은 boto3 패키지를 사용하며, boto3 패키지는 AWS SDK for Python입니다.
