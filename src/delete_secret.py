import boto3


def delete_secret(secrets, secret_name):
    try:
        secrets.delete_secret(
            SecretId=secret_name
        )
        print("Deleted.")
    except Exception:
        print("A secret with that name does not exist, start again.")
