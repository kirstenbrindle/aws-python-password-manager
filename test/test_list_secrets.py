from moto import mock_aws
from unittest.mock import patch
from src.list_secrets import list_secrets
import pytest
import boto3
import json


@pytest.mark.describe("list_secrets")
@pytest.mark.it("tests that it prints correct secret when only one secret")
@mock_aws
@patch('builtins.print')
def test_one_secret(mock_print):
    secrets = boto3.client('secretsmanager')
    secret_string = {
        "UserId": "bidenj",
        "Password": "Pa55word"
    }

    secrets.create_secret(
        Name='Missile_Launch_Codes',
        SecretString=json.dumps(secret_string)
    )
    list_secrets(secrets)
    mock_print.assert_called_with(
        "1 secret(s) available \nMissile_Launch_Codes")


@pytest.mark.describe("list_secrets")
@pytest.mark.it("tests that it prints correct secrets when mutiple secret")
@mock_aws
@patch('builtins.print')
def test_mutiple_secrets(mock_print):
    secrets = boto3.client('secretsmanager')
    secret_string = {
        "UserId": "bidenj",
        "Password": "Pa55word"
    }

    secrets.create_secret(
        Name='Missile_Launch_Codes',
        SecretString=json.dumps(secret_string)
    )
    secret_string = {
        "UserId": "trumpd",
        "Password": "password123"
    }

    secrets.create_secret(
        Name='NEW_Missile_Launch_Codes',
        SecretString=json.dumps(secret_string)
    )
    list_secrets(secrets)
    mock_print.assert_called_with(
        "2 secret(s) available \nMissile_Launch_Codes, "
        "NEW_Missile_Launch_Codes")


@pytest.mark.describe("list_secrets")
@pytest.mark.it("tests that it prints correct secrets when no secrets")
@mock_aws
@patch('builtins.print')
def test_no_secrets(mock_print):
    secrets = boto3.client('secretsmanager')
    list_secrets(secrets)
    mock_print.assert_called_with("0 secret(s) available")
