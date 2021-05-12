import pytest

from django.core.exceptions import ValidationError

from article.validators import BoardOptionValidator


class TestBoardOptionValidator:
    EXTERNAL_OPTIONS = {
        "differentDesigns": {
            "choices": [1, 2, 3]
        },
        "dimensionX": {
            "range": {
                "min": 10,
                "max": 100
            }
        }
    }

    @pytest.mark.parametrize("choices, range_min, range_max", [
        ([1, 2, 3], 10, 100),
        ([1], 10, 100),
        ([1, 2], 30, 80),
        ([1, 2, 3], 50, 50)
    ])
    def test_valid_options_do_not_raise_exception(self, choices, range_min, range_max):
        """GIVEN a BoardOptionValidator instantiated with a set of
        external board options

        WHEN the validate method is called with a set of internally
        offered, valid board options

        THEN no exception is thrown.
        """
        validator = BoardOptionValidator(self.EXTERNAL_OPTIONS)

        offered_options = {
            "differentDesigns": {
                "choices": choices
            },
            "dimensionX": {
                "range": {
                    "min": range_min,
                    "max": range_max
                }
            }
        }

        try:
            validator.validate(offered_options)
        except ValidationError:
            pytest.fail("Valid internal options raised ValidationError")

    @pytest.mark.parametrize("choices, range_min, range_max", [
        pytest.param([], 10, 100, id="empty choice list"),
        pytest.param([1, 2, 4], 10, 100, id="choice list contains unavailable value"),
        pytest.param([1, 2, 3], 9, 100, id="range minimum too low"),
        pytest.param([1, 2, 3], 10, 101, id="range maximum too high"),
        pytest.param([1, 2, 3], 50, 40, id="minimum is larger than maximum"),
        pytest.param(1, 10, 100, id="choices not given as list"),
        pytest.param([1, 2, 3], [10, 11], [99, 100], id="range bounds not given as ints")
    ])
    def test_invalid_option_values_raise_validation_error(self, choices, range_min, range_max):
        """GIVEN a BoardOptionValidator instantiated with a set of
        external board options

        WHEN the validate method is called with a set of internally
        offered, invalid board options

        THEN a ValidationError is thrown.
        """
        validator = BoardOptionValidator(self.EXTERNAL_OPTIONS)

        offered_options = {
            "differentDesigns": {
                "choices": choices
            },
            "dimensionX": {
                "range": {
                    "min": range_min,
                    "max": range_max
                }
            }
        }

        with pytest.raises(ValidationError):
            validator.validate(offered_options)


class TestAttributeValidator:
    pass
