import boto3
from src.create_secret import create_secret
from src.get_secret import get_secret
from src.list_secrets import list_secrets
from src.delete_secret import delete_secret


def password_manager():
    secrets = boto3.client('secretsmanager')

    initial_input = input(
        'Please specify [e]ntry, [r]etrieval, [d]eletion, [l]isting or e[x]it: ')
    if initial_input == 'e' or initial_input == "entry" or initial_input == "E" or initial_input == "Entry":
        secret_name = input('Secret identifier: ')
        user_id = input('UserId: ')
        password = input("Password: ")
        create_secret(secrets, secret_name, user_id, password)
        password_manager()

    elif initial_input == 'r' or initial_input == "R" or initial_input == "retrieval" or initial_input == "Retrieval":
        secret_name = input('Specify secret to retrieve: ')
        get_secret(secrets, secret_name)
        password_manager()

    elif initial_input == 'd' or initial_input == "D" or initial_input == "deletion" or initial_input == "Deletion":
        secret_name = input('Specify secret to delete: ')
        delete_secret(secrets, secret_name)
        password_manager()
    elif initial_input == 'l' or initial_input == "L" or initial_input == "listing" or initial_input == "Listing":
        list_secrets(secrets)
        password_manager()
    elif initial_input == 'x' or initial_input == 'X' or initial_input == 'exit' or initial_input == "Exit":
        print("Thank you, goodbye.")
        exit
    else:
        print("Invalid input.")
        password_manager()
