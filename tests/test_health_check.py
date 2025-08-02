import allure
import pytest
import requests


@allure.feature('Test Ping')
@allure.story('Test connection')
def test_ping(api_client):
    status_code = api_client.ping()
    assert status_code == 201, f"Expected status 201 but got {status_code}"


@allure.feature('Test Ping')
@allure.story('Test server unavailability')
def test_ping_server_unavailable(api_client, mocker):
    mocker.patch.object(api_client.session, 'get', side_effect=Exception("Server unavailable"))
    with pytest.raises(Exception, match="Server unavailable"):
        api_client.ping()


@allure.feature('Test Ping')
@allure.story('Test wrong HTTP method')
def test_ping_wrong_method(api_client, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 405
    mocker.patch.object(api_client.session, 'get', return_value=mock_response)
    with pytest.raises(AssertionError, match="Expected status 201 but got 405"):
        api_client.ping()


@allure.feature('Test Ping')
@allure.story('Test server error')
def test_ping_internal_server_error(api_client, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 500
    mocker.patch.object(api_client.session, 'get', return_value=mock_response)
    with pytest.raises(AssertionError, match="Expected status 201 but got 500"):
        api_client.ping()


@allure.feature('Test Ping')
@allure.story('Test wrong URL')
def test_ping_not_found(api_client, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 404
    mocker.patch.object(api_client.session, 'get', return_value=mock_response)
    with pytest.raises(AssertionError, match="Expected status 201 but got 404"):
        api_client.ping()


@allure.feature('Test Ping')
@allure.story('Test connection with different success code')
def test_ping_success_different_code(api_client, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mocker.patch.object(api_client.session, 'get', return_value=mock_response)
    with pytest.raises(AssertionError, match="Expected status 201 but got 200"):
        api_client.ping()


@allure.feature('Test Ping')
@allure.story('Test timeout')
def test_ping_timeout(api_client, mocker):
    mocker.patch.object(api_client.session, 'get', side_effect=requests.Timeout)
    with pytest.raises(requests.Timeout):
        api_client.ping()

@allure.feature('Test Ping')
@allure.story('Test Create Booking')
def test_ping_create_booking_success(api_client, mocker, generate_random_booking_data):
    booking_data = generate_random_booking_data
    response = mocker.Mock()
    response.status_code = 201
    response.json.return_value = {
            "booking": booking_data
        }
    mocker.patch.object(api_client.session, 'post', return_value=response)
    result = api_client.create_booking(booking_data)
    assert result['booking'] == booking_data
