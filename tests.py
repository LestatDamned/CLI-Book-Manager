import os
from unittest import TestCase

from managers import JSONManager, IDManager, BookManager


class JSONManagerTestCase(TestCase):
    def setUp(self):
        self.file_name = "test.json"
        self.manager = JSONManager(file_name=self.file_name)

    def tearDown(self):
        if os.path.exists(self.file_name):
            os.remove(self.file_name)

    def test_create_json(self):
        read_json = self.manager.read_json()
        self.assertEqual(read_json, [])

    def test_write_json(self):
        data = "test"
        self.manager.save_json(data)
        storage = self.manager.read_json()
        self.assertEqual(storage, data)


class IDManagerTestCase(TestCase):
    def setUp(self):
        self.file_name = "test_id.json"
        self.manager = IDManager(file_name=self.file_name)

    def tearDown(self):
        if os.path.exists(self.file_name):
            os.remove(self.file_name)

    def test_next_id(self):
        self.assertEqual(self.manager.get_next_id(), 1)


class BookManagerTestCase(TestCase):
    def setUp(self):
        self.book_file = "test_book.json"
        self.id_file = "test_book_id.json"
        self.manager = BookManager(file_name=self.book_file)
        self.manager.book_id = IDManager(file_name=self.id_file)
        self.manager.save_json([])

    def tearDown(self):
        for file in [self.book_file, self.id_file]:
            if os.path.exists(file):
                os.remove(file)

    def test_create_book(self):
        title, author, year = "test", "test", "2022"
        self.manager.add_book(title, author, year)
        self.assertEqual(len(self.manager.books), 1)
        self.assertEqual(self.manager.books[0]["title"], title)
        self.assertEqual(self.manager.books[0]["author"], author)
        self.assertEqual(self.manager.books[0]["year"], year)

    def test_read_book(self):
        self.manager.add_book("book1", "author1", 2020)
        self.manager.add_book("book2", "author2", 2021)
        books = self.manager.books
        self.assertEqual(len(books), 2)
        self.assertEqual(books[1]["author"], "author2")

    def test_delete_book(self):
        self.manager.add_book("book1", "author1", 2020)
        book_id = self.manager.books[0]["id"]
        self.manager.delete_books(book_id)
        self.assertEqual(len(self.manager.books), 0)

    def test_change_book_status(self):
        self.manager.add_book("book1", "author1", 2020)
        book_id = self.manager.books[0]["id"]
        self.manager.change_book_status(book_id, "выдана")
        self.assertEqual(self.manager.books[0]["status"], "выдана")

    def test_search_book(self):
        self.manager.add_book("search_book_title", "test", 1999)

        self.manager.search_books("1", "search_book_title")
        self.assertEqual(self.manager.books[0]["title"], "search_book_title")

        self.manager.add_book("test", "search_book_author", 1999)

        self.manager.search_books("2", "search_book_author")
        self.assertEqual(self.manager.books[1]["author"], "search_book_author")

        self.manager.add_book("test", "test_author", 1999)

        self.manager.search_books("3", 1999)
        self.assertEqual(self.manager.books[2]["year"], 1999)
