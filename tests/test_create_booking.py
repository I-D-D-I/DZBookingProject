import allure
import pytest
import requests

from conftest import booking_dates
from conftest import generate_random_booking_data
from requests.exceptions import HTTPError


@allure.feature('Create Booking')
@allure.story('Test Success Create Booking')
def test_create_booking_success(api_client, generate_random_booking_data):
    booking_data = generate_random_booking_data
    print("Sent JSON:", booking_data)
    # print("URL:", url)
    response = api_client.create_booking(booking_data)
    print("Response:", response.text)
    assert isinstance(response, dict), "Ответ не является словарем"
    assert "bookingid" in response, "Ответ не содержит bookingid"
    assert "booking" in response, "Ответ не содержит booking"


@allure.feature('Create Booking')
@allure.story('Create booking with empty body')
def test_create_booking_empty_body(api_client):
    with pytest.raises(HTTPError):
        api_client.create_booking({})


@allure.feature('Create Booking')
@allure.story('Create booking with invalid field')
def test_create_booking_invalid_field(api_client, booking_dates):
    invalid_data = {
        "firstname": "John",
        "lastname": "Doe",
        "totalprice": "invalid_price",
        "depositpaid": True,
        "bookingdates": booking_dates,
        "additionalneeds": "Breakfast"
    }
    with pytest.raises(HTTPError):
        api_client.create_booking(invalid_data)

