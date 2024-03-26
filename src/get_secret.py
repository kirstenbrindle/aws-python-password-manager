import json


def get_secret(secrets, secret_name):
    """
    This function takes a boto3 Secrets Manager client and name of a
    secret. The function retrieves the specified secret from Secrets
    Manager and saves the contents to a local text file.

    Args:
        `secrets`: Secrets Manager boto3 client
        `secret_name`: string of secret name
    ---------------------------

    Returns:
        No return value.
    """
    try:
        response = secrets.get_secret_value(
            SecretId=secret_name,
        )
        secret_string = json.loads(response['SecretString'])

        data = (f'UserId: {secret_string["UserId"]} \n'
                f'Password: {secret_string["Password"]}')

        with open('./Top_secret/secrets.txt', 'w', encoding='utf-8') as f:
            f.write(data)

        print('Secrets stored in local file secrets.txt')

    except Exception:
        print("A secret with this name does not exist, start again.")
