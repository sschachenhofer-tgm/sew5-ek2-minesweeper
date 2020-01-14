import random
from unittest import TestCase

from ms_model import *


class TestField(TestCase):

    def setUp(self) -> None:
        self.field = Field()

    def test_default_state(self):
        """The Field should have a default state of COVERED at first"""
        self.assertEqual(self.field.state, Field.COVERED)

    def test_default_no_mine(self):
        """After instantiating, the Field should not contain a mine"""
        self.assertFalse(self.field.mine)

    def test_switch_tagging_to_tagged(self):
        """Switch to MINE_TAGGED (exclamation mark !)"""
        self.field.switch_tagging()
        self.assertEqual(self.field.state, Field.MINE_TAGGED)

    def test_switch_tagging_to_possible(self):
        """Switch to MINE_POSSIBLE (question mark ?)"""
        self.field.switch_tagging()
        self.field.switch_tagging()
        self.assertEqual(self.field.state, Field.MINE_POSSIBLE)

    def test_switch_tagging_untagged(self):
        """Switch back to untagged (COVERED)"""
        self.field.switch_tagging()
        self.field.switch_tagging()
        self.field.switch_tagging()
        self.assertEqual(self.field.state, Field.COVERED)

    def test_switch_tagging_when_uncovered(self):
        """Trying to switch the Field state on an UNCOVERED Field should raise an exception"""
        self.field.state = Field.UNCOVERED
        self.assertRaises(AlreadyUncoveredError, self.field.switch_tagging)

    def test_uncover(self):
        """Field state should switch to UNCOVERED"""
        self.field.uncover()
        self.assertEqual(self.field.state, Field.UNCOVERED)

    def test_uncover_already_uncovered(self):
        """A Field can only be uncovered once"""
        self.field.state = Field.UNCOVERED
        self.assertRaises(AlreadyUncoveredError, self.field.uncover)

    def test_uncover_tagged(self):
        self.field.state = Field.MINE_TAGGED
        self.assertRaises(FieldTaggedError, self.field.uncover)

    def test_uncover_mine(self):
        self.field.mine = True
        self.assertRaises(MineFound, self.field.uncover)


class TestModel(TestCase):

    def setUp(self) -> None:
        self.model = MinesweeperModel()

    def test_correct_dimensions(self):
        """The default game board should have a width and height of 9"""
        self.assertEqual(self.model.width, 9)
        self.assertEqual(self.model.height, 9)

    def test_correct_mines(self):
        """The default game board should have 10 randomly placed mines, each on their own Field"""
        correct_mines = list(filter(lambda m: 0 <= m[0] < 9 and 0 <= m[1] < 9, set(self.model.mines)))
        self.assertEqual(len(correct_mines), 10)

    def test_field_state(self):
        """Before uncovering a Field, all fields should have a state of COVERED"""
        self.assertEqual(self.model.field_state(random.randrange(0, 9), random.randrange(0, 9)), Field.COVERED)

    def test_field_state_tagged(self):
        """After tagging a Field, it should have a state of MINE_TAGGED"""
        x = random.randrange(0, 9)
        y = random.randrange(0, 9)
        self.model.switch_tagging(x, y)
        self.assertEqual(self.model.field_state(x, y), Field.MINE_TAGGED)

    def test_uncover_clean(self):
        """After uncovering an untagged, previously covered Field, the state should switch to UNCOVERED"""

        x = random.randrange(0, 9)
        y = random.randrange(0, 9)

        while (x, y) in self.model.mines:
            # Find coordinates that are not a mine
            x = random.randrange(0, 9)
            y = random.randrange(0, 9)

        self.model.uncover(x, y)
        self.assertEqual(self.model.field_state(x, y), Field.UNCOVERED)

    def test_uncover_tagged(self):
        x = random.randrange(0, 9)
        y = random.randrange(0, 9)

        self.model.switch_tagging(x, y)
        with self.assertRaises(FieldTaggedError):
            self.model.uncover(x, y)

    def test_uncover_already_uncovered(self):
        x = random.randrange(0, 9)
        y = random.randrange(0, 9)

        self.model.uncover(x, y)
        with self.assertRaises(AlreadyUncoveredError):
            self.model.uncover(x, y)

    def test_uncover_mine(self):
        x, y = self.model.mines[0]

        with self.assertRaises(MineFound):
            self.model.uncover(x, y)

    def test_won(self):
        for x in range(9):
            for y in range(9):
                if (x, y) in self.model.mines:
                    self.model.switch_tagging(x, y)
                else:
                    self.model.uncover(x, y)

        self.assertTrue(self.model.won())