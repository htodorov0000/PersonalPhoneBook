import unittest
from unittest import mock, TestCase
import main

class TestSearch(TestCase):
    @mock.patch("main.input", create=True)
    
    def test_search_menu(self, mock_input):
        john = ["John", "01", "a@b.c", "-"]
        alex = ["Alex", "01", "a@b.c", "-"]
        john_b = ["John B", "01", "a@b.c", "-"]
        records = [john, alex , john_b]
        mock_input.side_effect = ["John", "john", "jo", "alex", "a1"]
        self.assertEqual(main.search_menu(records), [john,john_b])
        self.assertEqual(main.search_menu(records), [john,john_b])
        self.assertEqual(main.search_menu(records), [john,john_b])
        self.assertEqual(main.search_menu(records), [alex])
        self.assertEqual(main.search_menu(records), records) #returns all records in case no match is found
        

if __name__ == "__main__":
    unittest.main()
