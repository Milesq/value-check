import pytest

from src import ValCheck, ValReq, Checkable


@pytest.fixture(name="data")
def fixture_data():
    return {
        "tab_name": "landing page",
        "col": 1,
        "row": "3",
        "metadata": {
            "lang": "en",
        },
    }


def test_match_primitive_values(data):
    schema = ValCheck({
        "tab_name": "landing page",
        "col": 1,
        "metadata": {
            "lang": "en",
        },
    })

    assert schema.check(data)


def test_returns_false_on_primitive_differences(data):
    schemas = [
        {
            "col": 2,
        },
        {
            "col": "1",
        },
        {
            "tab_name": "library page",
        },
    ]

    for invalid_schema in schemas:
        schema = ValCheck(invalid_schema)

        assert schema.check(data) is False


def test_match_checkable_value(data):
    schema = ValCheck({
        "col": ValReq(le=1, gt=0),
        "row": ValReq(lt=10, cast=int),
    })

    assert schema.check(data)

    data['col'] -= 1
    assert not schema.check(data)
    data['col'] += 1

    data['row'] = 11
    assert not schema.check(data)


def test_custom_checkable():
    class CustomCheckable(Checkable):
        def check(self, value):
            return value in ['Anakin Skywalker', 'Darth Vader']

    schema = ValCheck({
        "person": CustomCheckable(),
    })

    assert schema.check({"person": "Anakin Skywalker"})

    assert not schema.check({"person": "Obi-Wan Kenobi"})


def test_cover_none_value():
    schema = ValReq(eq=None)

    assert schema.check(None) is True
    assert schema.check(1) is False


    schema = ValReq(ne=None)

    assert schema.check(None) is False
    assert schema.check(2) is True
