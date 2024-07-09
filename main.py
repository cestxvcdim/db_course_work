from set_db import init_db
from db_work import fill_db, load_data


def main():
    # Инициализация базы данных описанными таблицами
    init_db()
    # Загрузка данных из файла
    data = load_data("./data/companies.json")
    # Заполнение базы данных
    fill_db(data)


if __name__ == "__main__":
    main()
