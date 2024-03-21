# aws-python-password-manager

This AWS-powered password manager is a command-line application to store and retrieve passwords. The passwords are stored in AWS Secrets Manager. 

Accessing your AWS account (with your Access Key ID and Secret Key) is considered sufficient authorisation to retrieve the passwords.

## Functionality

The application allows the user to:

- store a user id and password as a secret in secretsmanager
- list all the stored secrets
- retrieve a secret with the resulting user ID and password stored in a text file
- delete a secret

## Using the application

To run the application, type the following command in the terminal:

`python src/run_password_manager.py`

You will then be prompted to select a service with this message:

`Please specify [e]ntry, [r]etrieval, [d]eletion, [l]isting or e[x]it: `
