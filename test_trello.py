"""Tests for the trello module."""
from unittest import TestCase, skip
from unittest.mock import patch

from trello import get_probabilities, print_card


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


class TestPrintCard(TestCase):
    """Test printing out a card."""

    def setUp(self):
        """Set self.card to some dummy data"""
        self.card = {
            "name": "Name!",
            "desc": "Desc!",
            "attachments": [{"url": "https://something.com"}],
            "shortUrl": "https://somethingelse.com",
        }

    def get_output(self):
        """Return the outputted string."""
        with patch("builtins.print") as print_mock:
            print_card(self.card)

        return "\n".join("".join(args) for args, kwargs in print_mock.call_args_list)

    def test_name(self):
        """Should print name in the output."""

        output = self.get_output()

        self.assertIn(self.card["name"], output)

    def test_desc(self):
        """Should print desc in the output."""

        output = self.get_output()

        self.assertIn(self.card["desc"], output)

    def test_attachment_url(self):
        """Should print attachment url in the output."""

        output = self.get_output()

        self.assertIn(self.card["attachments"][0]["url"], output)

    def test_short_url(self):
        """Should print shortUrl in the output."""

        output = self.get_output()

        self.assertIn(self.card["shortUrl"], output)

    @skip("no ready yet")
    def test_no_bandcamp_footer(self):
        """Test that we don't get the bandcamp unsubscribe footer."""

        card
