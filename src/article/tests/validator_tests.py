import pytest

from django.core.exceptions import ValidationError

from article.validators import BoardOptionValidator, AttributeValidator


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
    OFFERED_OPTIONS = {
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

    @pytest.mark.parametrize("differentDesigns, dimensionX", [
        (1, 10),
        (3, 100),
        (2, 42),
    ])
    def test_valid_attributes_do_not_raise_exception(self, differentDesigns, dimensionX):
        """GIVEN an AttributeValidator instantiated with a set of
        currently offered board options

        WHEN the validate method is called with a set of valid board attributes

        THEN no exception is thrown.
        """
        validator = AttributeValidator(self.OFFERED_OPTIONS)

        board_attributes = {
            "differentDesigns": differentDesigns,
            "dimensionX": dimensionX
        }

        try:
            validator.validate(board_attributes)
        except ValidationError:
            pytest.fail("Valid board attributes raised ValidationError")

    @pytest.mark.parametrize("differentDesigns, dimensionX", [
        pytest.param(0, 42, id="choice not offered"),
        pytest.param(1, 9, id="value out of range (low)"),
        pytest.param(1, 101, id="value out of range (high)"),
        pytest.param(1.0, 42, id="choice has wrong type (float)"),
        pytest.param([1], 42, id="choice has wrong type (list)"),
        pytest.param("1", 42, id="choice has wrong type (str)"),
        pytest.param(3, "42", id="value has wrong type (str)"),
        pytest.param(3, [42], id="value has wrong type (list)")
    ])
    def test_invalid_attributes_raise_exception(self, differentDesigns, dimensionX):
        """GIVEN an AttributeValidator instantiated with a set of
        currently offered board options

        WHEN the validate method is called with a set of invalid board
        attributes

        THEN a ValidationError is thrown.
        """
        validator = AttributeValidator(self.OFFERED_OPTIONS)

        board_attributes = {
            "differentDesigns": differentDesigns,
            "dimensionX": dimensionX
        }

        with pytest.raises(ValidationError):
            validator.validate(board_attributes)
