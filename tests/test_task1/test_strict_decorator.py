from unittest import TestCase

from task1.solution import strict


class TestStrictDecorator(TestCase):
    def test_type_int(self):
        @strict
        def sum_two(a: int, b: int) -> int:
            return a + b

        self.assertEqual(sum_two(5, 5), 10)
        self.assertEqual(sum_two(3, b=7), 10)
        self.assertEqual(sum_two(a=6, b=4), 10)

        with self.assertRaises(TypeError):
            sum_two(1, 9.0)

    def test_type_float(self):
        @strict
        def sum_two(a: float, b: float) -> float:
            return a + b

        self.assertEqual(sum_two(1.0, 9.0), 10.0)

        with self.assertRaises(TypeError):
            sum_two(1, 9.0)

    def test_type_str(self):
        @strict
        def sum_two(a: str, b: str) -> str:
            return a + b

        self.assertEqual(sum_two('Hello ', 'world!'), 'Hello world!')

        with self.assertRaises(TypeError):
            sum_two(1, 'world!')

    def test_invalid_type_return(self):
        @strict
        def sum_two(a: int, b: int) -> int:
            return str(a + b)

        with self.assertRaises(TypeError):
            sum_two(5, 5)
