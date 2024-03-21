import boto3
import json


def create_secret(secrets, secret_name, user_id, password):
    try:
        secret_string = {
            "UserId": user_id,
            "Password": password}

        secrets.create_secret(
            Name=secret_name,
            SecretString=json.dumps(secret_string)
        )
        print('Secret saved.')

    except Exception as error:
        if error.response['Error']['Message'] == 'A resource with the ID you requested already exists.':
            print(
                "A secret with this name already exists, start again!")
        elif error.response['Error']['Message'] == 'Invalid name. Must be a valid name containing alphanumeric characters, or any of the following: -/_+=.@!':
            print(error.response['Error']['Message'] + ', start again!')
        elif error.response['Error']['Message'] == "You can't create this secret because a secret with this name is already scheduled for deletion.":
            print(error.response['Error']['Message'][:-1] + ', start again!')
