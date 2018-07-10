from django.test import TestCase
from bowling.models import Game


class GameTests(TestCase):

    def test_total_frames(self):
        """
        total_frames() returns total number of frames in a game.
        """

        self.assertEqual(Game.total_frames(), 10)

    def test_frame_chances(self):
        """
        frame_chances() returns total number of chances for a given frame.
        """

        self.assertEqual(Game.frame_chances(1), 2)
        self.assertEqual(Game.frame_chances(3), 2)
        self.assertEqual(Game.frame_chances(10), 3)

    def test_chance_points(self):
        """
        chance_points() returns integer value for mark received (string).
        """

        self.assertEqual(Game.chance_points('1'), 1)
        self.assertEqual(Game.chance_points('6'), 6)
        self.assertEqual(Game.chance_points('/'), 10)
        self.assertEqual(Game.chance_points('x'), 10)

    def test_calculate_score(self):
        """
        calculate_score() returns correct score for given list
        of marks.
        """

        random_marks = ['5', '3', '6', '/', '3', '/', '6', '0', 'x', '6', '/', '0', '/', '6']
        all_strikes = ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x']
        all_spares = ['9', '/', '9', '/', '9', '/', '9', '/', '9', '/', '9', '/', '9', '/', '9', '/', '9', '/', '9', '/', '9']
        all_strikes_but_one = ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x']

        self.assertEqual(Game.calculate_score(all_strikes), 300)
        self.assertEqual(Game.calculate_score(all_spares), 190)
        self.assertEqual(Game.calculate_score(random_marks), 89)
        self.assertEqual(Game.calculate_score(all_strikes_but_one), 270)
