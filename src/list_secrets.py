import boto3


def list_secrets(secrets):
    response = secrets.list_secrets()
    num_of_secrets = len(response["SecretList"])
    if num_of_secrets == 0:
        print("0 secret(s) available")
    else:
        names = [secret["Name"] for secret in response["SecretList"]]
        print(f"{num_of_secrets} secret(s) available \n{', '.join(names)}")
