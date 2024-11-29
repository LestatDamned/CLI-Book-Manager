import json


class JSONManager:
    def __init__(self, file_name):
        self.file_name: str = file_name
        self.data = self.read_json()

    def read_json(self):
        try:
            with open(self.file_name, 'r', encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            with open(self.file_name, 'w', encoding="utf-8") as f:
                return json.dump([], f, indent=4)

    def save_json(self, data):
        with open(self.file_name, 'w', encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)


class IDManager(JSONManager):

    def __init__(self, file_name="json/id_storage.json"):
        super().__init__(file_name)

    def get_next_id(self):
        if not self.data:
            self.data = {"id": 0}
        self.data["id"] += 1
        self.save_json(self.data)
        return self.data["id"]


class BookManager(JSONManager):
    def __init__(self):
        super().__init__(file_name="json/books.json")
        self.books = self.data
        self.book_id = IDManager()

    def show_all_books(self):
        if not self.books:
            print("Список книг пуст")
        else:
            for book in self.books:
                print(f"id: {book['id']}, название: {book['title']},"
                      f" автор: {book['author']}, год выпуска: {book['year']},"
                      f" статус: {book['status']}")

    def add_book(self, title, author, year):
        new_book = {
            "id": self.book_id.get_next_id(),
            "title": title,
            "author": author,
            "year": year,
            "status": "в наличии"
        }
        self.books.append(new_book)
        self.save_json(self.books)
        print(f"Книга добавлена:\nid: {new_book['id']}, название: {new_book['title']}, "
              f"автор: {new_book['author']}, год выпуска: {new_book['year']}, "
              f"статус: {new_book['status']}")

    def delete_books(self, book_id: int):
        book_to_delete = None
        for book in self.books:
            if book["id"] == book_id:
                book_to_delete = book
                break

        if book_to_delete:
            self.books = [book for book in self.books if book["id"] != book_id]
            self.save_json(self.books)
            print(f"Книга удалена:\nid: {book_to_delete['id']}, название: {book_to_delete['title']}, "
                  f"автор: {book_to_delete['author']}, год выпуска: {book_to_delete['year']}, "
                  f"статус: {book_to_delete['status']}")
        else:
            print("Книга не найдена")

    def search_books(self, choice, key):
        field = {"1": "title", "2": "author", "3": "year"}
        if choice not in field:
            print("Неверный выбор поля для поиска. 1 - поиск по названию, 2 - поиск по автору, 3 - поиск по году")
            return

        found_books = [book for book in self.books if str(key).lower() in str(book[field[choice]]).lower()]

        if found_books:
            for book in found_books:
                print(f"id: {book['id']}, название: {book['title']}, автор: {book['author']},"
                      f" год выпуска: {book['year']}, статус: {book['status']}")
        else:
            print(f"Книги по запросу '{key}' не найдены.")

    def change_book_status(self, book_id: int, status):
        for book in self.books:
            if book["id"] == book_id:
                book["status"] = status
                self.save_json(self.books)
                print(f"Статус изменен на '{book["status"]}'\n"
                      f"Книга: id: {book["id"]}, название: {book["title"]}, автор: {book["author"]}, "
                      f"год выпуска: {book["year"]}")
                return
        print(f"Книга с id {book_id} не найдена")
