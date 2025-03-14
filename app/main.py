from typing import List, Tuple, Dict, Optional


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        """
        Инициализация палубы корабля.

        :param row: Номер строки.
        :param column: Номер столбца.
        :param is_alive: Статус палубы (жива/уничтожена).
        """
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def __repr__(self) -> str:
        """
        Возвращает строковое представление палубы.
        """
        return f"Deck({self.row}, {self.column}, is_alive={self.is_alive})"


class Ship:
    def __init__(self, start: Tuple[int, int], end: Tuple[int, int],
                 is_drowned: bool = False) -> None:
        """
        Инициализация корабля.

        :param start: Координаты начала корабля (строка, столбец).
        :param end: Координаты конца корабля (строка, столбец).
        :param is_drowned: Статус корабля (потоплен/не потоплен).
        """
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = self._create_decks()

    def _create_decks(self) -> List[Deck]:
        """
        Создает список палуб корабля.

        :return: Список объектов Deck.
        """
        decks = []
        start_row, start_column = self.start
        end_row, end_column = self.end

        if start_row == end_row:  # Горизонтальный корабль
            for column in range(start_column, end_column + 1):
                decks.append(Deck(start_row, column))
        elif start_column == end_column:  # Вертикальный корабль
            for row in range(start_row, end_row + 1):
                decks.append(Deck(row, start_column))

        return decks

    def get_deck(self, row: int, column: int) -> Optional[Deck]:
        """
        Возвращает палубу по координатам.

        :param row: Номер строки.
        :param column: Номер столбца.
        :return: Объект Deck или None, если палуба не найдена.
        """
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> str:
        """
        Обрабатывает выстрел по палубе.

        :param row: Номер строки.
        :param column: Номер столбца.
        :return: Результат выстрела ("Hit!" или "Sunk!").
        """
        deck = self.get_deck(row, column)
        if deck and deck.is_alive:
            deck.is_alive = False
            if all(not deck.is_alive for deck in self.decks):
                self.is_drowned = True
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    def __repr__(self) -> str:
        """
        Возвращает строковое представление корабля.
        """
        return (f"Ship(start={self.start}, end={self.end}"
                f", is_drowned={self.is_drowned})")


class Battleship:
    def __init__(self, ships: List[Tuple[Tuple[int, int],
                 Tuple[int, int]]]) -> None:
        """
        Инициализация игрового поля.

        :param ships: Список кораблей, где каждый корабль представлен кортежем
                      из двух координат (начало и конец).
        """
        self.field: Dict[Tuple[int, int], Ship] = {}
        for ship in ships:
            new_ship = Ship(ship[0], ship[1])
            for deck in new_ship.decks:
                self.field[(deck.row, deck.column)] = new_ship

    def fire(self, location: Tuple[int, int]) -> str:
        """
        Обрабатывает выстрел по клетке.

        :param location: Координаты клетки (строка, столбец).
        :return: Результат выстрела ("Miss!", "Hit!", "Sunk!").
        """
        if location in self.field:
            ship = self.field[location]
            return ship.fire(location[0], location[1])
        return "Miss!"

    def print_field(self) -> None:
        """
        Выводит текущее состояние поля.
        """
        for row in range(10):
            for column in range(10):
                if (row, column) in self.field:
                    ship = self.field[(row, column)]
                    deck = ship.get_deck(row, column)
                    if deck and not deck.is_alive:
                        if ship.is_drowned:
                            print("x", end="\t")
                        else:
                            print("*", end="\t")
                    else:
                        print("□", end="\t")
                else:
                    print("~", end="\t")
            print()


# Пример использования
if __name__ == "__main__":
    # Создаем корабли
    ships = [
        ((0, 0), (0, 3)),  # 4-палубный корабль
        ((2, 0), (2, 1)),  # 2-палубный корабль
        ((4, 4), (4, 4)),  # 1-палубный корабль
    ]

    # Создаем игровое поле
    battleship = Battleship(ships)

    # Выводим начальное состояние поля
    print("Initial field:")
    battleship.print_field()

    # Выстрелы
    print(battleship.fire((0, 0)))  # Hit!
    print(battleship.fire((0, 1)))  # Hit!
    print(battleship.fire((0, 2)))  # Hit!
    print(battleship.fire((0, 3)))  # Sunk!
    print(battleship.fire((4, 4)))  # Sunk!
    print(battleship.fire((9, 9)))  # Miss!

    # Выводим состояние поля после выстрелов
    print("\nField after firing:")
    battleship.print_field()
