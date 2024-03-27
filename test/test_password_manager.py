from moto import mock_aws
from unittest.mock import patch, call
from src.password_manager import password_manager
import pytest


@pytest.mark.describe("password_manager")
@pytest.mark.it("tests that it prints correct opening statement")
@patch('builtins.input', return_value='x')
@mock_aws
def tests_correct_starting_user_prompt(mock_input):
    """
    Given:
    Function is first invoked

    Returns:
    Correct initial input prompt is printed
    """
    password_manager()
    mock_input.assert_called_with(
        "Please specify [e]ntry, [r]etrieval, [d]eletion, [l]isting or "
        "e[x]it: ")


@pytest.mark.describe("password_manager")
@pytest.mark.it("tests that it prints exit statement when x inputted")
@patch('builtins.input', return_value='x')
@patch('builtins.print')
@mock_aws
def tests_exit(mock_print, mock_input):
    """
    Given:
    Function is first invoked and user inputs x

    Returns:
    Correct exit message is printed
    """
    password_manager()
    mock_print.assert_called_with("Thank you, goodbye.")


@pytest.mark.describe("password_manager")
@pytest.mark.it("tests that it prints correct message for invalid input "
                "and confirm that it recalls the function")
@patch('builtins.input', side_effect=['i', 'x'])
@patch('builtins.print')
@mock_aws
def tests_invalid_input_message(mock_print, mock_input):
    """
    Given:
    Function is first invoked and user inputs invalid character

    Returns:
    Correct invalid input message is printed
    """
    password_manager()
    mock_input.assert_called_with(
        "Please specify [e]ntry, [r]etrieval, [d]eletion, [l]isting or "
        "e[x]it: ")
    mock_print.assert_has_calls(
        [call("Invalid input."), call("Thank you, goodbye.")])


@pytest.mark.describe("password_manager")
@pytest.mark.it("if input = e, correct prompts show")
@patch('builtins.input', side_effect=['e', "Missile_launch_codes",
                                      "bidenj", "Pa55word", 'x'])
@mock_aws
def tests_input_prompt_e(mock_input):
    """
    Given:
    Function is invoked and user inputs e

    Returns:
    Correct messages are printed
    """
    password_manager()
    mock_input.assert_has_calls(
        [call(
            "Please specify [e]ntry, [r]etrieval, [d]eletion, "
            "[l]isting or e[x]it: "),
         call("Secret identifier: "), call("UserId: "), call("Password: "),
         call("Please specify [e]ntry, [r]etrieval, [d]eletion, "
              "[l]isting or e[x]it: ")])


@pytest.mark.describe("password_manager")
@pytest.mark.it("if input = r, correct prompts show")
@patch('builtins.input', side_effect=['r', 'Missile_launch_codes', 'x'])
@patch('builtins.print')
@patch("src.password_manager.get_secret")
@mock_aws
def tests_input_prompt_r(mock_get_secret, mock_print, mock_input):
    """
    Given:
    Function is invoked and user inputs r

    Returns:
    Correct messages are printed
    """
    password_manager()
    mock_input.assert_has_calls(
        [call("Please specify [e]ntry, [r]etrieval, [d]eletion, "
              "[l]isting or e[x]it: "),
         call("Specify secret to retrieve: "),
         call("Please specify [e]ntry, [r]etrieval, [d]eletion, "
              "[l]isting or e[x]it: ")])


@pytest.mark.describe("password_manager")
@pytest.mark.it("if input = d, correct prompts show")
@patch('builtins.input', side_effect=['d', "Missile_launch_codes", "x"])
@patch('builtins.print')
@patch("src.password_manager.delete_secret")
@mock_aws
def tests_input_prompt_d(mock_delete_secret, mock_print, mock_input):
    """
    Given:
    Function is invoked and user inputs d

    Returns:
    Correct messages are printed
    """
    password_manager()
    mock_input.assert_has_calls(
        [call("Please specify [e]ntry, [r]etrieval, [d]eletion, "
              "[l]isting or e[x]it: "),
         call("Specify secret to delete: "),
         call("Please specify [e]ntry, [r]etrieval, [d]eletion, "
              "[l]isting or e[x]it: ")])


@pytest.mark.describe("password_manager")
@pytest.mark.it("if input = l, list secrets function is called")
@patch('builtins.input', side_effect=['l', 'x'])
@patch("src.password_manager.list_secrets")
@mock_aws
def tests_input_prompt_l_functionality(mock_list_secrets, mock_input):
    """
    Given:
    Function is invoked and user inputs l

    Returns:
    List secret is invoked
    """
    password_manager()
    assert mock_list_secrets.call_count == 1


@pytest.mark.describe("password_manager")
@pytest.mark.it("if input = e, create secrets function is called")
@patch('builtins.input', side_effect=['e', "Missile_launch_codes",
                                      "bidenj", "Pa55word", 'x'])
@patch("src.password_manager.create_secret")
@mock_aws
def tests_input_prompt_e_functionality(mock_create_secret, mock_input):
    password_manager()
    assert mock_create_secret.call_count == 1


@pytest.mark.describe("password_manager")
@pytest.mark.it("if input = r, get secrets function is called")
@patch('builtins.input', side_effect=['r', 'Missile_launch_codes', 'x'])
@patch("src.password_manager.get_secret")
@mock_aws
def tests_input_prompt_r_functionality(mock_get_secret, mock_input):
    """
    Given:
    Function is invoked and user inputs r

    Returns:
    Get secret is invoked
    """
    password_manager()
    assert mock_get_secret.call_count == 1


@pytest.mark.describe("password_manager")
@pytest.mark.it("if input = d, delete secret function is called")
@patch('builtins.input', side_effect=['d', "Missile_launch_codes", "x"])
@patch("src.password_manager.delete_secret")
@mock_aws
def tests_input_prompt_d_functionality(mock_delete_secret, mock_input):
    """
    Given:
    Function is invoked and user inputs d

    Returns:
    Delete secret is invoked
    """
    password_manager()
    assert mock_delete_secret.call_count == 1
