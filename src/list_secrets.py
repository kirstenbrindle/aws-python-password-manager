def list_secrets(secrets):
    """
    This function takes a boto3 Secrets Manager client and lists how many
    secrets are stored and the names of the stored secrets.

    Args:
        `secrets`: Secrets Manager boto3 client
    ---------------------------

    Returns:
        No return value.
    """
    response = secrets.list_secrets()
    num_of_secrets = len(response["SecretList"])
    if num_of_secrets == 0:
        print("0 secret(s) available")
    else:
        names = [secret["Name"] for secret in response["SecretList"]]
        print(f"{num_of_secrets} secret(s) available \n{', '.join(names)}")
