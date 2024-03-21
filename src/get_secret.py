import json


def get_secret(secrets, secret_name):
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
