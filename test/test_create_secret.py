from moto import mock_aws
from unittest.mock import patch
from src.create_secret import create_secret
import pytest
import boto3
import json


@pytest.mark.describe("create_secret")
@pytest.mark.it("test user secret is stored")
@mock_aws
def test_user_secret_is_stored():
    """
    Given:
    A valid Secrets Manager client, secret name, user id and password

    Returns:
    Correct user id and password are stored in Secrets Manager
    """
    secrets = boto3.client('secretsmanager')
    secret_name = 'Missile_Launch_Codes'
    user_id = 'bidenj'
    password = 'Pa55word'
    create_secret(secrets, secret_name, user_id, password)
    response = secrets.get_secret_value(
        SecretId='Missile_Launch_Codes',
    )
    secret_string = json.loads(response['SecretString'])

    assert secret_string['UserId'] == 'bidenj'
    assert secret_string['Password'] == 'Pa55word'


@pytest.mark.describe("create_secret")
@pytest.mark.it("test secret name does not already exist")
@patch("builtins.print")
@mock_aws
def test_user_does_not_already_have_secret_with_this_name(mock_print):
    """
    Given:
    A valid Secrets Manager client, secret name that already exists,
    user id and password

    Returns:
    Correct print message to inform user that a secret with that name
    already exists
    """
    secrets = boto3.client('secretsmanager')
    secret_name = 'Missile_Launch_Codes'
    user_id = 'bidenj'
    password = 'Pa55word'
    create_secret(secrets, secret_name, user_id, password)

    create_secret(secrets, secret_name, user_id, password)
    mock_print.assert_called_with(
        "A secret with this name already exists, start again!")


'''
These last two tests have highlighted that mock_aws does not behave
in the same way as AWS in all cases:

AWS Secrets Manager will inform the user that a secret cannot be created
if a secret with that name is scheduled for deletion, but mock_aws
would show the message that a secret with that name already exists.

Also AWS Secrets Manager will not let the user create a secret with
invalid characters (valid characters are alphanumeric characters, or
any of the following: -/_+=.@!) but mock_aws will allow this.
'''


@pytest.mark.describe("create_secret")
@pytest.mark.it("test secret name has not just been deleted")
@patch("builtins.print")
@mock_aws
def test_user_does_not_already_have_secret_staged_for_deletion(mock_print):
    """
    Given:
    A valid Secrets Manager client, a secret name that has just been deleted,
    user id and password

    Returns:
    Correct print message to inform user that a secret with that name
    is already scheduled for deletion
    """
    secrets = boto3.client('secretsmanager')
    secret_name = 'Missile_Launch_Codes'
    user_id = 'bidenj'
    password = 'Pa55word'
    create_secret(secrets, secret_name, user_id, password)
    secrets.delete_secret(
        SecretId='Missile_Launch_Codes'
    )
    create_secret(secrets, secret_name, user_id, password)
    mock_print.assert_called_with(
        "You can't create this secret because a secret with this name is "
        "already scheduled for deletion, start again!")


@pytest.mark.describe("create_secret")
@pytest.mark.it("test try to create secret with invalid name")
@patch("builtins.print")
@mock_aws
def test_invalid_name(mock_print):
    """
    Given:
    A valid Secrets Manager client, a secret name containing invalid
    characters, user id and password

    Returns:
    Correct print message to inform user that the secret name is invalid
    """
    secrets = boto3.client('secretsmanager')
    secret_name = '!$*&(){£$%£}'
    user_id = 'bidenj'
    password = 'Pa55word'
    create_secret(secrets, secret_name, user_id, password)
    mock_print.assert_called_with(
        'Invalid name. Must be a valid name containing alphanumeric characters'
        ', or any of the following: -/_+=.@!, start again!')
