import allure
import pytest
import requests
from pydantic import ValidationError
from core.models.booking import BookingResponse

from conftest import booking_dates
from conftest import generate_random_booking_data
from requests.exceptions import HTTPError


@allure.feature('Test creating booking')
@allure.story('Test Success Create Booking')
def test_create_booking_success(api_client, generate_random_booking_data):
    booking_data = generate_random_booking_data
    response = api_client.create_booking(booking_data)
    assert isinstance(response, dict), "Ответ не является словарем"
    assert "bookingid" in response, "Ответ не содержит bookingid"
    assert "booking" in response, "Ответ не содержит booking"


@allure.feature('Test creating booking')
@allure.story('Create booking with empty body')
def test_create_booking_empty_body(api_client):
    with pytest.raises(HTTPError):
        api_client.create_booking({})


@allure.feature('Test creating booking')
@allure.story('Create booking with invalid field')
def test_create_booking_invalid_field(api_client, booking_dates):
    invalid_data = {
        "lastname": "Doe",
        "totalprice": "invalid_price",
        "depositpaid": True,
        "bookingdates": booking_dates,
        "additionalneeds": "Breakfast"
    }
    with pytest.raises(HTTPError):
        api_client.create_booking(invalid_data)


@allure.feature('Test creating booking')
@allure.story('Positive: creating booking with custom data')
def test_create_booking_with_custom_data(api_client):
    booking_data = {
        "firstname": "Ivan",
        "lastname": "Ivanovich",
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2026-06-01",
            "checkout": "2026-06-10"
        },
        "additionalneeds": "Dinner"
    }

    response = api_client.create_booking(booking_data)
    try:
        BookingResponse(**response)
    except ValidationError as e:
        raise ValidationError(f"Response validation failed: {e}")

        assert response['booking']['firstname'] == booking_data['firstname']
        assert response['booking']['lastname'] == booking_data['lastname']
        assert response['booking']['totalprice'] == booking_data['totalprice']
        assert response['booking']['depositpaid'] == booking_data['depositpaid']
        assert response['booking']['bookingdates']['checkin'] == booking_data['bookingdates']['checkin']
        assert response['booking']['bookingdates']['checkout'] == booking_data['bookingdates']['checkout']
        assert response['booking']['additionalneeds'] == booking_data['additionalneeds']
