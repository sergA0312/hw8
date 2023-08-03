import sqlite3

# Подключение к базе данных и создание таблиц, если их ещё нет
conn = sqlite3.connect('my_database.db')
cursor = conn.cursor()

# Создание таблицы countries, если её ещё нет
cursor.execute('''
    CREATE TABLE IF NOT EXISTS countries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL
    )
''')

# Добавление записей в таблицу countries
cursor.executemany('INSERT INTO countries (title) VALUES (?)', [('Россия',), ('США',), ('Германия',)])

# Создание таблицы cities, если её ещё нет
cursor.execute('''
    CREATE TABLE IF NOT EXISTS cities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        area REAL DEFAULT 0,
        country_id INTEGER,
        FOREIGN KEY (country_id) REFERENCES countries(id)
    )
''')

# Добавление записей в таблицу cities
cities_data = [
    ('Москва', 2561.5, 1),
    ('Нью-Йорк', 789.9, 2),
    ('Берлин', 891.4, 3),
    # Добавьте остальные города
]
cursor.executemany('INSERT INTO cities (title, area, country_id) VALUES (?, ?, ?)', cities_data)

# Создание таблицы employees, если её ещё нет
cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        city_id INTEGER,
        FOREIGN KEY (city_id) REFERENCES cities(id)
    )
''')

# Добавление записей в таблицу employees
employees_data = [
    ('Иван', 'Иванов', 1),
    ('Петр', 'Петров', 2),
    ('Екатерина', 'Мизулина', 3),
    ('Сергей', 'Смирнов', 4),

    # Добавьте остальных сотрудников
]
cursor.executemany('INSERT INTO employees (first_name, last_name, city_id) VALUES (?, ?, ?)', employees_data)

# Сохранение изменений и закрытие соединения
conn.commit()
conn.close()

# Здесь начинается код для запроса данных
conn = sqlite3.connect('my_database.db')
cursor = conn.cursor()

# Шаг 2: Получение списка городов
cursor.execute('SELECT id, title FROM cities')
cities_data = cursor.fetchall()

# Шаг 3: Вывод списка городов
print("Список городов:")
for city in cities_data:
    print(f"{city[0]}. {city[1]}")

# Закрытие соединения с базой данных
conn.close()


# Шаг 4: Запрос id города у пользователя
selected_city_id = int(input("Введите id города для просмотра сотрудников (0 для выхода): "))

# Шаг 5 и 6: Получение и вывод информации о сотрудниках в выбранном городе
if selected_city_id != 0:
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT e.first_name, e.last_name, c.title AS city, co.title AS country, c.area AS city_area
        FROM employees e
        INNER JOIN cities c ON e.city_id = c.id
        INNER JOIN countries co ON c.country_id = co.id
        WHERE e.city_id = ?
    ''', (selected_city_id,))
    employees_data = cursor.fetchall()

    if employees_data:
        print(f"\nСотрудники, проживающие в выбранном городе:")
        for employee in employees_data:
            print(f"Имя: {employee[0]}, Фамилия: {employee[1]}, Город: {employee[2]}, Страна: {employee[3]}, Площадь города: {employee[4]}")
    else:
        print("Нет сотрудников, проживающих в выбранном городе.")

    # Закрытие соединения с базой данных после выполнения всех операций.
    conn.close()
