import pytest
from pydantic import ValidationError
from app.models import ObservationIn
from app.trestle import observation_path

def test_observation_strips_required_fields():
    item=ObservationIn(title="  River gums  ",location=" North bank ")
    assert item.title == "River gums" and item.location == "North bank"

def test_observation_bounds_temperature_and_ids():
    with pytest.raises(ValidationError): ObservationIn(title="x",location="y",temperature=100)
    with pytest.raises(ValueError): observation_path("../admin")
