import sqlite3

class BudgetManager:
    def __init__(self, db_name='budget.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS categories (
                               id INTEGER PRIMARY KEY AUTOINCREMENT,
                               category_name TEXT NOT NULL)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                               id INTEGER PRIMARY KEY AUTOINCREMENT,
                               amount REAL NOT NULL,
                               category_id INTEGER REFERENCES categories(id),
                               date TEXT NOT NULL)''')
        self.conn.commit()

    def add_category(self, category_name):
        self.cursor.execute("INSERT INTO categories (category_name) VALUES (?)", (category_name,))
        self.conn.commit()

    def add_expense(self, amount, category_name, date):
        self.cursor.execute("SELECT id FROM categories WHERE categories.category_name = ?", (category_name,))
        result = self.cursor.fetchone()
        if not result:
            print('Error 404 not found(no such category). Make one with a method add_category.')
        else:
            category_id = result[0]
            self.cursor.execute("INSERT INTO expenses (amount, category_id, date) VALUES (?, ?, ?)", (amount, category_id, date))
            self.conn.commit()

    def get_report(self):
        self.cursor.execute("SELECT category_name, SUM(amount) AS total_amount" \
        "                    FROM categories" \
        "                    JOIN expenses ON expenses.category_id=categories.id" \
        "                    GROUP BY categories.id" \
        "                    ORDER BY total_amount DESC")
        report_data = self.cursor.fetchall()
        print('ФИНАНСОВЫЙ ОТЧЕТ ПО БАЗЕ ДАННЫХ')
        if not report_data:
            print('Расходов пока нет!')
        for category_name, total_amount in report_data:
            print(f"Категория {category_name} составила общую сумму в {total_amount} рублей.")
    
    def close_connection(self):
        self.conn.close()
        
if __name__ == '__main__':
    #проверка работы
    manager = BudgetManager()
    manager.add_category("Еда")
    manager.add_category("Игры")
    manager.add_category("Одежда")
    manager.add_expense(15, "Игры", "2026-11-01")
    manager.add_expense(45, "Игры", "2026-11-01")
    manager.add_expense(120, "Еда", "2026-11-01")
    manager.add_expense(500, "Космос", "2026-11-01")
    manager.get_report()
