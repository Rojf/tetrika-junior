import unittest
from unittest.mock import patch, mock_open
from collections import defaultdict

from task2.solution import (
    write_csv,
    format_count_to_csv,
    count_animals_by_first_letter,
    get_next_page_path
)


class TestAnimalScraper(unittest.TestCase):

    def test_format_count_to_csv(self):
        data = defaultdict(int, {'А': 2, 'Б': 3})
        expected = "А,2\nБ,3\n"
        self.assertEqual(format_count_to_csv(data), expected)

    @patch("builtins.open", new_callable=mock_open)
    def test_write_csv(self, mock_file):
        content = "А,2\nБ,3\n"
        write_csv(content, file_name="testfile")

        mock_file.assert_called_once_with("testfile.csv", mode="w", encoding="utf-8")
        mock_file().write.assert_called_once_with(content)

    def test_count_animals_by_first_letter(self):
        html = """
        <div class="mw-category-generated">
          <div id="mw-pages">
            <div class="mw-content-ltr">
              <ul>
                <li><a href="/wiki/Aardvark">Антилопа</a></li>
                <li><a href="/wiki/Baboon">Бабуин</a></li>
              </ul>
            </div>
          </div>
        </div>
        """
        count = defaultdict(int)
        count_animals_by_first_letter(html, count)

        self.assertEqual(count["А"], 1)
        self.assertEqual(count["Б"], 1)

    def test_get_next_page_path_found(self):
        html = """
        <div id="mw-pages">
            <a href="/wiki/Категория:Животные_по_алфавиту?page=2">Следующая страница</a>
        </div>
        """
        result = get_next_page_path(html)
        self.assertEqual(result, "/wiki/Категория:Животные_по_алфавиту?page=2")

    def test_get_next_page_path_not_found(self):
        html = '<div id="mw-pages"></div>'
        self.assertIsNone(get_next_page_path(html))


if __name__ == "__main__":
    unittest.main()

