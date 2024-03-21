from moto import mock_aws
from unittest.mock import patch
from src.delete_secret import delete_secret
import pytest
import boto3
import json


@pytest.mark.describe("delete secret")
@pytest.mark.it("tests it deletes given secret when only one secret stored")
@mock_aws
def test_deletes_secret():
    secrets = boto3.client('secretsmanager')
    secret_string = {
        "UserId": "bidenj",
        "Password": "Pa55word"
    }

    secrets.create_secret(
        Name='Missile_Launch_Codes',
        SecretString=json.dumps(secret_string)
    )
    response = secrets.list_secrets()

    assert len(response["SecretList"]) == 1
    assert response["SecretList"][0]["Name"] == 'Missile_Launch_Codes'

    delete_secret(secrets, 'Missile_Launch_Codes')

    with pytest.raises(Exception):
        secrets.get_secret_value(
            SecretId='Missile_Launch_Codes'
        )


@pytest.mark.describe("delete secret")
@pytest.mark.it("tests it deletes given secret when mutiple secrets stored")
@mock_aws
def test_deletes_secret_when_mutiple():
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
    response = secrets.list_secrets()

    assert len(response["SecretList"]) == 2
    assert response["SecretList"][0]["Name"] == 'Missile_Launch_Codes'
    assert response["SecretList"][1]["Name"] == 'NEW_Missile_Launch_Codes'

    delete_secret(secrets, 'Missile_Launch_Codes')
    response = secrets.list_secrets()
    for secret in response["SecretList"]:
        if secret["Name"] == 'Missile_Launch_Codes':
            assert "DeletedDate" in secret


@pytest.mark.describe("delete_secret")
@pytest.mark.it("test prints correct message if secret name does not exist")
@patch("builtins.print")
@mock_aws
def test_user_does_not_have_secret_with_this_name(mock_print):
    secrets = boto3.client('secretsmanager')
    delete_secret(secrets, 'NEW_Missile_Launch_Codes')
    mock_print.assert_called_with(
        "A secret with that name does not exist, start again.")


@pytest.mark.describe("delete_secret")
@pytest.mark.it("test try to delete secret with invalid name")
@patch("builtins.print")
@mock_aws
def test_invalid_name(mock_print):
    secrets = boto3.client('secretsmanager')
    delete_secret(secrets, '!$*&(){£$%£}')
    mock_print.assert_called_with(
        "A secret with that name does not exist, start again.")
