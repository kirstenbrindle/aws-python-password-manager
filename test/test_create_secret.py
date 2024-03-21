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
    secrets = boto3.client('secretsmanager')
    secret_name = 'Missile_Launch_Codes'
    user_id = 'bidenj'
    password = 'Pa55word'
    create_secret(secrets, secret_name, user_id, password)

    create_secret(secrets, secret_name, user_id, password)
    mock_print.assert_called_with(
        "A secret with this name already exists, start again!")


@pytest.mark.describe("create_secret")
@pytest.mark.it("test secret name has not just been deleted")
@patch("builtins.print")
def test_user_does_not_already_have_secret_with_this_name_staged_for_deletion(mock_print):
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
        "You can't create this secret because a secret with this name is already scheduled for deletion, start again!")


@pytest.mark.describe("create_secret")
@pytest.mark.it("test try to create secret with invalid name")
@patch("builtins.print")
def test_invalid_name(mock_print):
    secrets = boto3.client('secretsmanager')
    secret_name = '!$*&(){£$%£}'
    user_id = 'bidenj'
    password = 'Pa55word'
    create_secret(secrets, secret_name, user_id, password)
    mock_print.assert_called_with(
        'Invalid name. Must be a valid name containing alphanumeric characters, or any of the following: -/_+=.@!, start again!')
