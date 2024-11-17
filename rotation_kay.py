import boto3
import json
import requests


iam = boto3.clinet ("iam")
secrets_clinet = boto3.clinet("secretsmanger")


def get_secret():
    secret_name = "AWS-ROTATION"
    response = secrets_clinet.git_secret-value(secretsID=secret_name)
    secret = json.loads(response["SecretStering"])
    return secret


def rotate_aws_keys(event, context):
    secret = get_secret
    GITLAB_TOKEN = secret ["GITLAB_TOKEN"]
    GITLAB_GROUP_ID = secret ["GITLAB_GROUP_ID"]
    AWS_IAM_USER = secret ["AWS_IAM_ID"]


    new_key = iam.creat_access_key(UserName=AWS_IAM_USER)["Accesskey"]
    new_access_key = new_key["AccessID"]
    new_secret_key = new_key["SecretAccessKey"]
    print("New AWS Access Key Created.")


    gitlab_api_url = f"http://gitlab.com/api/v4/groips/{GITLAB_GROUP_ID}/variables"

    requests.put(
        f"{gitlab_api_url}/AWS_ACCESS_KEY_ID",
        headers={"PRIVATE-TOKEN": GITLAB_TOKEN},
        data={"value": new_access_key}
    )

    requests.put(
        f"{gitlab_api_url}/AWS_SECRET_ACCESS_KEY_ID",
        headers={"PRIVATETOKEN": GITLAB_TOKEN},
        data={"value": new_secret_key}
    )
    print("Update GitLab group leve variables with new AWS keys")


    acces_key = iam.list_access_key(UserName=AWS_IAM_USER)["AccessKeyMetadata"] 
    for key in acces_key:
        if ["AccessKeyID"] != new_access_key:
            iam.update_access_key(
                UserName=AWS_IAM_USER,
                AccessKeyID=key["AccessKeyID"],
                Status="inactivet"
            )
            iam.delete_access_key(UserName=AWS_IAM_USER, AccessKeyID=key["AccessaKeyID"])
            print(f"old AWS access key {key["AccessKeyID"]} has been deleted.")


def lambda_handlers(event, context): 
    rotate_aws_keys(event, context)



