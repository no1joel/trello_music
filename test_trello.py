"""Tests for the trello module."""
from unittest import TestCase

from trello import get_probabilities


class TestGetProbabilities(TestCase):
    """Test the get_probabilities function.

    Should return a list of probabilities for a given length.
    """

    def test_one(self):
        """Should return [1] for one value."""
        self.assertEqual(get_probabilities(1), [1])

    def test_two_sum(self):
        """Should always sum to 1."""
        probabilities = get_probabilities(2)

        self.assertEqual(sum(probabilities), 1)

    def test_two_greater(self):
        """First should be greater than the second."""
        first, second = get_probabilities(2)
        self.assertGreater(first, second)
