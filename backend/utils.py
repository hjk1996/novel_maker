import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

# AWS 세션 생성
session = boto3.Session(region_name="us-east-1")  # 필요한 경우 지역을 지정

# SSM 클라이언트 생성
ssm_client = session.client("ssm")


def get_parameter(parameter_name):
    try:
        response = ssm_client.get_parameter(
            Name=parameter_name, WithDecryption=True  # 값이 암호화된 경우 True로 설정
        )
        return response["Parameter"]["Value"]
    except ssm_client.exceptions.ParameterNotFound:
        print(f"Parameter {parameter_name} not found.")
        return None
    except NoCredentialsError:
        print("AWS credentials not found.")
        return None
    except PartialCredentialsError:
        print("Incomplete AWS credentials.")
        return None
