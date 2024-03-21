# aws-python-password-manager

This AWS-powered password manager is a command-line application written using Python to store and retrieve passwords. The passwords are stored in AWS Secrets Manager and connect using boto3.

Accessing your AWS account (with an Access Key ID and Secret Key) is considered sufficient authorisation to retrieve the passwords.

## Functionality

The application allows the user to:

- store a user id and password as a secret in secretsmanager
- list all the stored secrets
- retrieve a secret with the resulting user ID and password stored in a text file
- delete a secret

## Using the application

To run the application, the user needs to be logged it to an AWS account.

They can then type the following command in the terminal:

`python src/run_password_manager.py`

The user will then be prompted to select a service with this message:

`Please specify [e]ntry, [r]etrieval, [d]eletion, [l]isting or e[x]it: `

If [e] is selected, the user can create a new secret.

If [r] is selected, the user can retrieve a stored secret (it will be saved to a text file in the 'Top_secret' folder).

If [d] is selected, the user can delete a stored secret.

If [l] is selected, the user can list all stored secrets.

If [x] is selected, the application will exit the command line.

If any other character is selected, the user will be prompted to select a valid letter.

## Utility functions

The main function password_manager uses the following utility functions:

- create_secret
- delete_secret
- get_secret
- list_secrets
