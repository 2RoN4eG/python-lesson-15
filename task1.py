import pathlib, sqlite3
import csv


database_name = "weather.db"
csvfilename = "weather.csv"

is_new = not pathlib.Path(database_name).exists()
connection = sqlite3.connect(database_name)
if is_new:
    cursor = connection.cursor()

    # - `id` — уникальный идентификатор измерения(задавать автоматически, при добавлении записи в таблицу);
    # - `date` — дата измерения;
    # - `time` — время измерения;
    # - `temperature` — температура воздуха в °C;
    # - `precipitation` — вид осадков;
    # - `wind_speed` — скорость ветра в км/ч.

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS measurements (
        id INTEGER PRIMARY KEY,
        date DATE NOT NULL,
        time TIME NOT NULL,
        temperature INTEGER,
        precipitation VARCHAR,
        wind_speed INTEGER
    )
    """)

    connection.commit()

    insert_query = """
    INSERT INTO measurements (
        id,
        date,
        time,
        temperature,
        precipitation,
        wind_speed
    )
    VALUES (
        :id,
        :date,
        :time,
        :temperature,
        :precipitation,
        :wind_speed
    )
    """

    with open(csvfilename, "r", newline='') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            cursor.execute(insert_query, row)

    connection.commit()
    cursor.close()

else:
    print("Database exists.")

connection.close()


def menu():
    print("""
1. Вывести все данные.
2. Вывести только дату, время и температуру.
3. Найти все измерения, где температура ниже 0.
4. Найти все записи с дождём (rain).
5. Найти измерения, где скорость ветра больше 20 км/ч.
6. Отсортировать все измерения на заданную дату по температуре по возрастанию.
7. Показать все снежные (snow) измерения, отсортированные по температуре.
8. Найти измерения без осадков (null) и отсортировать по скорости ветра от большей к меньшей.
""")


def case1():
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM measurements")
    for id, date, time, temperature, precipitation, wind_speed in cursor:
        print(id, date, time, temperature, precipitation, wind_speed)

    cursor.close()
    connection.close()


def case2():
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()
    cursor.execute("SELECT date, time, temperature FROM measurements")
    for date, time, temperature in cursor:
        print(date, time, temperature)

    cursor.close()
    connection.close()


def case3():
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM measurements WHERE temperature < 0")
    for id, date, time, temperature, precipitation, wind_speed in cursor:
        print(id, date, time, temperature, precipitation, wind_speed)

    cursor.close()
    connection.close()


def case4():
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM measurements WHERE precipitation = 'rain'")
    for id, date, time, temperature, precipitation, wind_speed in cursor:
        print(id, date, time, temperature, precipitation, wind_speed)

    cursor.close()
    connection.close()


def case5():
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM measurements WHERE wind_speed > 20")
    for id, date, time, temperature, precipitation, wind_speed in cursor:
        print(id, date, time, temperature, precipitation, wind_speed)

    cursor.close()
    connection.close()


def case6():
    date = input("Введите дату: ")
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM measurements WHERE date = '{date}' ORDER BY temperature ASC")
    for id, date, time, temperature, precipitation, wind_speed in cursor:
        print(id, date, time, temperature, precipitation, wind_speed)

    cursor.close()
    connection.close()


def case7():
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM measurements WHERE precipitation = 'snow' ORDER BY temperature")
    for id, date, time, temperature, precipitation, wind_speed in cursor:
        print(id, date, time, temperature, precipitation, wind_speed)

    cursor.close()
    connection.close()


def case8():
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM measurements WHERE precipitation IS NULL OR precipitation = 'null' ORDER BY temperature DESC")
    for id, date, time, temperature, precipitation, wind_speed in cursor:
        print(id, date, time, temperature, precipitation, wind_speed)

    cursor.close()
    connection.close()


if __name__ == "__main__":
    while True:
        menu()
        number = input("Выберети пункт меню: ")

        match(number):
            case "1":
                case1()
            case "2":
                case2()
            case "3":
                case3()
            case "4":
                case4()
            case "5":
                case5()
            case "6":
                case6()
            case "7":
                case7()
            case "8":
                case8()
            case "0":
                break
