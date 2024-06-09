import os 

from agents import NextStoryAgent, ChoicesAgent, DallEAgent
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

# AWS 세션 생성
session = boto3.Session(region_name=os.getenv("REGION", "ap-northeast-2"))  # 필요한 경우 지역을 지정

# SSM 클라이언트 생성
ssm_client = session.client("ssm")


def get_parameter(parameter_name):
    try:
        response = ssm_client.get_parameter(
            Name=parameter_name, WithDecryption=False  # 값이 암호화된 경우 True로 설정
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

openai_api_key = get_parameter("novel-maker-openai-api-key")


next_stroy_agent = NextStoryAgent(
    api_key=openai_api_key
)
choices_agent = ChoicesAgent(
    api_key=openai_api_key
)
dall_e_agent = DallEAgent(
    api_key=openai_api_key
)


def get_next_story_agent() -> NextStoryAgent:
    return next_stroy_agent


def get_choices_agent() -> ChoicesAgent:
    return choices_agent


def get_dall_e_agent() -> DallEAgent:
    return dall_e_agent
