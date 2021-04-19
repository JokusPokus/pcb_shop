import pytest

from article.validators import BoardOptionValidator


class TestPrivateMethods:
    def test_choice_attribute_true_positive(self, choice_attribute):
        assert BoardOptionValidator._contains_choices(choice_attribute)

    def test_choice_attribute_no_false_positive(self, range_attribute):
        assert not BoardOptionValidator._contains_choices(range_attribute)

    def test_range_attribute_true_positive(self, range_attribute):
        assert BoardOptionValidator._contains_range(range_attribute)

    def test_range_attribute_no_false_positive(self, choice_attribute):
        assert not BoardOptionValidator._contains_range(choice_attribute)


class TestValidationSuccess:
    pass


class TestValidationFailure:
    pass
