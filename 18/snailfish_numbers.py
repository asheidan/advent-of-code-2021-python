
import math
import unittest
from typing import Tuple, Union

Number = Union[int, Tuple["Number", "Number"]]


def number_from_string(string: str) -> Number:
    return eval(string.strip().replace("[", "(").replace("]", ")"))


def magnitude(number: Number):
    match number:
        case (left, right):
            return magnitude(left) * 3 + magnitude(right) * 2

        case element:
            return element


def add(first: Number, second: Number) -> Number:
    return (first, second)

def add_right(number: Number, value: int) -> Number:
    match number:
        case (left, right):
            return (left, add_right(right, value))

        case element:
            return element + value


def add_left(number: Number, value: int) -> Number:
    match number:
        case (left, right):
            return (add_left(left, value), right)

        case element:
            return element + value


def reduce(number: Number) -> Number:

    while True:
        (_, number, _), did_explode = explode(number)
        if did_explode:
            continue

        number, did_split = split(number)
        if did_split:
            continue

        return number


def split(number: Number) -> Tuple[Number, bool]:
    """Split the left-most number > 9.
    
    Return the number and a bool which is true if any number was split.
    """
    match number:
        case (left, right):
            left, was_split = split(left)

            if was_split:

                return (left, right), True

            right, was_split = split(right)

            return (left, right), was_split

        case element if element > 9:
            #print("fjiupp")
            return (math.floor(element / 2), math.ceil(element / 2)), True

        case element:
            return element, False


def explode(number: Number, level: int = 1) -> Tuple[Tuple[int, Number, int], bool]:
    match [number, level]:
        case [(left, right), l] if l >= 5:
            #print("BOOM!")
            return (left, 0, right), True

        case ((left, right), _):
            result, did_explode = explode(left, level + 1)
            left_splinter, left, right_splinter = result

            if did_explode:
                if right_splinter:
                    right = add_left(right, right_splinter)

                return (left_splinter, (left, right), 0), True

            result, did_explode = explode(right, level + 1)
            left_splinter, right, right_splinter = result

            if did_explode:
                if left_splinter:
                    left = add_right(left, left_splinter)

                return (0, (left, right), right_splinter), True

            return (left_splinter, (left, right), right_splinter), False

        case [foo, _]:
            return (0, foo, 0), False


class TestSplit(unittest.TestCase):

    def test_single_low_element_should_be_unaffected(self):
        # Given
        number = 9

        # When
        result = split(number)

        # Then
        self.assertEqual((9, False), result)

    def test_single_high_element_should_return_split_number(self):
        # Given
        number = 11

        # When
        result = split(number)

        # Then
        self.assertEqual(((5, 6), True), result)

    def test_nested_high_element_should_return_split_number(self):
        # Given
        number = (1, (15, 5))

        # When
        result = split(number)

        # Then
        expected = (1, ((7, 8), 5))
        self.assertEqual((expected, True), result)

    def test_nested_low_elements_should_not_split_numbers(self):
        # Given
        number = (1, ((9, 8), 5))

        # When
        result = split(number)

        # Then
        expected = (1, ((9, 8), 5))
        self.assertEqual((expected, False), result)

    def test_multiple_high_number_should_split_leftmost(self):
        # Given
        number = (11, 15)

        # When
        result = split(number)

        # Then
        expected = ((5, 6), 15)
        self.assertEqual((expected, True), result)

class TestExplode(unittest.TestCase):
    def test_flat_tuple_should_not_change(self):
        # Given
        number = (1, 5)

        # When
        (_left, result, _right), _did_explode = explode(number)

        # Then
        self.assertEqual((1, 5), result)

    def test_example_explode_left(self):
        # Given
        number = (((((9, 8), 1), 2), 3), 4)

        # Then
        (left, result, _right), _did_explode = explode(number)

        # Then
        expected = ((((0, 9), 2), 3), 4)
        self.assertEqual(expected, result)
        self.assertEqual(9, left)

    def test_example_explode_right(self):
        # Given
        number = (7, (6, (5, (4, (3, 2)))))

        # Then
        (_left, result, right), _did_explode = explode(number)

        # Then
        expected = (7, (6, (5, (7, 0))))
        self.assertEqual(expected, result)
        self.assertEqual(2, right)

    def test_example_explode_only_leftmost(self):
        # Given
        number = ((3, (2, (1, (7, 3)))), (6, (5, (4, (3, 2)))))

        # Then
        (left, result, right), did_explode = explode(number)

        # Then
        expected = ((3, (2, (8, 0))), (9, (5, (4, (3, 2)))))
        self.assertEqual(expected, result)
        self.assertEqual(0, left)
        self.assertEqual(0, right)
        self.assertTrue(did_explode)