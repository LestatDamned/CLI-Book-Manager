from managers import BookManager


class Command:
    """Базовый класс для реализации команды."""

    def execute(self):
        raise NotImplementedError("Метод execute() должен быть реализован")


class DisplayBooksCommand(Command):
    """Класс команды для отображения всех книг."""

    def __init__(self, receiver: BookManager):
        self.receiver = receiver

    def execute(self):
        print("Отображение всех книг:")
        self.receiver.show_all_books()


class AddBookCommand(Command):
    """Класс команды для добавления книги."""

    def __init__(self, receiver: BookManager):
        self.receiver = receiver

    def execute(self):
        print("Вы в разделе добавления книги: введите название книги, автора книги, год выхода книги")
        title = input("Название книги: ")
        author = input("Автор книги: ")
        year = input("Год выхода книги: ")
        self.receiver.add_book(title, author, year)


class DeleteBookCommand(Command):
    """Класс команды для удаления книги."""

    def __init__(self, receiver: BookManager):
        self.receiver = receiver

    def execute(self):
        print("Вы выбрали удаление книг: чтобы удалить книгу нужно ввести ее id")
        book_id = int(input("Введите id книги: "))
        self.receiver.delete_books(book_id)


class SearchBookCommand(Command):
    """Класс команды для поиска книг."""

    def __init__(self, receiver: BookManager):
        self.receiver = receiver

    def execute(self):
        print("Вы выбрали поиск книги, вы можете найти книгу:")
        print("[1] по названию")
        print("[2] по автору")
        print("[3] по году выпуска")
        choice = input(">>> ")
        match choice:
            case '1':
                title = input("Введите название книги: ")
                self.receiver.search_books(choice, title)
            case '2':
                author = input("Введите автора: ")
                self.receiver.search_books(choice, author)
            case '3':
                year = int(input("Введите год выпуска: "))
                self.receiver.search_books(choice, year)
            case _:
                print("Неверный выбор")


class ChangeStatusCommand(Command):
    """Класс команды для изменения статуса книги."""

    def __init__(self, receiver: BookManager):
        self.receiver = receiver

    def execute(self):
        print("Вы выбрали изменение статуса книги: введите id книги которой хотите изменить статус")
        book_id = int(input("Введите id книги: "))
        print("[1] для изменения статуса книги на 'в наличии'")
        print("[2] для изменения на статус 'выдана'")
        choice = input(">>> ")
        match choice:
            case '1':
                status = "в наличии"
                self.receiver.change_book_status(book_id, status)
            case '2':
                status = "выдана"
                self.receiver.change_book_status(book_id, status)
            case _:
                print("Неверный выбор")


class Menu:
    """Класс для управления меню программы и выбора команд."""

    def __init__(self):
        self.commands = {}  # Словарь зарегистрированных команд (ключ - номер в меню, значение - команда).

    def register_command(self, key, command):
        """Регистрирует новую команду в меню."""
        self.commands[key] = command

    def show_menu(self):
        """Выводит меню, обрабатывает выбор пользователя и выполняет соответствующую команду."""

        while True:
            print("""
        [1] Отобразить все книги
        [2] Добавить книгу
        [3] Удалить книгу
        [4] Поиск книги
        [5] Изменение статуса книги
        [0] Выход
        """)
            choice = input(">>> ")
            match choice:
                case '0':
                    print("Выход из программы")
                    break
                case _ if (command := self.commands.get(choice)):
                    command.execute()
                    self.ask_to_show_menu(command)
                case _:
                    print("Неверный выбор")

    def ask_to_show_menu(self, command):
        """Позволяет вернуться в главное меню, повторить действие или выйти из программы."""

        while True:
            go_back_choice = input("\n[1] Вернуться в главное меню | "
                                   "[2] Повторить последнее действие | "
                                   "[0] Выйти из программы. \n")
            match go_back_choice:
                case '1':
                    break
                case '0':
                    print("До свидания!")
                    exit()
                case '2':
                    command.execute()
                case _:
                    print("Неверный ввод.")


books_manager = BookManager()

display_books = DisplayBooksCommand(books_manager)
add_book = AddBookCommand(books_manager)
delete_book = DeleteBookCommand(books_manager)
search_book = SearchBookCommand(books_manager)
change_status = ChangeStatusCommand(books_manager)

menu = Menu()
menu.register_command("1", display_books)
menu.register_command("2", add_book)
menu.register_command("3", delete_book)
menu.register_command("4", search_book)
menu.register_command("5", change_status)

menu.show_menu()
