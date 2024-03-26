def delete_secret(secrets, secret_name):
    """
    This function takes a boto3 Secrets Manager client and name of a
    secret. The function deletes the specified secret from Secrets
    Manager.

    Args:
        `secrets`: Secrets Manager boto3 client
        `secret_name`: string of secret name
    ---------------------------

    Returns:
        No return value.
    """
    try:
        secrets.delete_secret(
            SecretId=secret_name
        )
        print("Deleted.")
    except Exception:
        print("A secret with that name does not exist, start again.")
