from moto import mock_aws
from unittest.mock import patch
from src.get_secret import get_secret
import pytest
import boto3
import json
import os


@pytest.mark.describe("get_secret")
@pytest.mark.it("makes file with correct name")
@mock_aws
def test_file_with_correct_name_has_been_created():
    """
    Given:
    A valid Secrets Manager client and valid secret name

    Returns:
    Correct secrets file has been created
    """
    secrets = boto3.client('secretsmanager')
    secret_string = {
        "UserId": "bidenj",
        "Password": "Pa55word"
    }

    secrets.create_secret(
        Name='Missile_Launch_Codes',
        SecretString=json.dumps(secret_string)
    )
    get_secret(secrets, 'Missile_Launch_Codes')

    assert os.path.isfile('./Top_secret/secrets.txt')


@pytest.mark.describe("get_secret")
@pytest.mark.it("secrets file contains correct secret data")
@mock_aws
def test_file_with_correct_secret_data_has_been_created():
    """
    Given:
    A valid Secrets Manager client and valid secret name

    Returns:
    Correct secret data is stored in secrets.txt file
    """
    secrets = boto3.client('secretsmanager')
    secret_string = {
        "UserId": "bidenj",
        "Password": "Pa55word"
    }

    secrets.create_secret(
        Name='Missile_Launch_Codes',
        SecretString=json.dumps(secret_string)
    )
    get_secret(secrets, 'Missile_Launch_Codes')

    with open('./Top_secret/secrets.txt', 'r', encoding='utf-8') as f:
        data = f.read()

    assert data == 'UserId: bidenj \nPassword: Pa55word'


@pytest.mark.describe("get_secret")
@pytest.mark.it("function overwrites secret in file when new one retrieved")
@mock_aws
def test_overwrites_previous():
    """
    Given:
    A valid Secrets Manager client and valid secret name

    Returns:
    Correct secret data has overwritten previous secret data in secrets.txt
    """
    secrets = boto3.client('secretsmanager')
    secret_string = {
        "UserId": "bidenj",
        "Password": "Pa55word"
    }

    secrets.create_secret(
        Name='Missile_Launch_Codes',
        SecretString=json.dumps(secret_string)
    )
    get_secret(secrets, 'Missile_Launch_Codes')

    with open('./Top_secret/secrets.txt', 'r', encoding='utf-8') as f:
        data = f.read()

    assert data == 'UserId: bidenj \nPassword: Pa55word'

    secret_string = {
        "UserId": "trumpd",
        "Password": "password123"
    }

    secrets.create_secret(
        Name='NEW_Missile_Launch_Codes',
        SecretString=json.dumps(secret_string)
    )
    get_secret(secrets, 'NEW_Missile_Launch_Codes')

    with open('./Top_secret/secrets.txt', 'r', encoding='utf-8') as f:
        data = f.read()

    assert data == 'UserId: trumpd \nPassword: password123'


@pytest.mark.describe("get_secret")
@pytest.mark.it("prints correct message if input secret does not exist")
@patch("builtins.print")
@mock_aws
def test_secret_does_not_exist(mock_print):
    """
    Given:
    A valid Secrets Manager client and secret name that does not exist

    Returns:
    Correct print message to inform user that secret does not exist
    """
    secrets = boto3.client('secretsmanager')
    get_secret(secrets, 'NEW_Missile_Launch_Codes')
    mock_print.assert_called_with(
        "A secret with this name does not exist, start again.")


@pytest.mark.describe("get_secret")
@pytest.mark.it("test secret name has just been deleted")
@patch("builtins.print")
@mock_aws
def test_user_has_deleted_this_secret(mock_print):
    """
    Given:
    A valid Secrets Manager client and secret name that has just been deleted

    Returns:
    Correct print message to inform user that secret does not exist
    """
    secrets = boto3.client('secretsmanager')
    secret_string = {
        "UserId": "bidenj",
        "Password": "Pa55word"
    }

    secrets.create_secret(
        Name='Missile_Launch_Codes',
        SecretString=json.dumps(secret_string)
    )
    secrets.delete_secret(
        SecretId='Missile_Launch_Codes'
    )
    get_secret(secrets, 'Missile_launch_codes')
    mock_print.assert_called_with(
        "A secret with this name does not exist, start again.")


@pytest.mark.describe("get_secret")
@pytest.mark.it("try to get secret with invalid name prints correct message")
@patch("builtins.print")
@mock_aws
def test_invalid_name(mock_print):
    """
    Given:
    A valid Secrets Manager client and invalid secret name

    Returns:
    Correct print message to inform user that secret does not exist
    """
    secrets = boto3.client('secretsmanager')
    get_secret(secrets, '!$*&(){£$%£}')
    mock_print.assert_called_with(
        "A secret with this name does not exist, start again.")
