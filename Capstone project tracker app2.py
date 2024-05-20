import sqlite3
import questionary

# Connect to the SQLite database
conn = sqlite3.connect('budget_tracker.db')
cursor = conn.cursor()

# Create tables for expenses, income, budgets, and financial goals
cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY,
                    category TEXT,
                    amount REAL
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS income (
                    id INTEGER PRIMARY KEY,
                    category TEXT,
                    amount REAL
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS budgets (
                    id INTEGER PRIMARY KEY,
                    category TEXT,
                    amount REAL
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS financial_goals (
                    id INTEGER PRIMARY KEY,
                    goal TEXT,
                    achieved INTEGER
                )''')

conn.commit()

def add_expense_category():
    """Add new expense category using questionary."""
    category = questionary.text("Enter the expense category:").ask()
    new_expense = float(questionary.text("Enter the expense amount:").ask())

    cursor.execute("SELECT amount FROM expenses WHERE category = ?", (category,))
    existing_expense = cursor.fetchone()

    if existing_expense:
        updated_expense = existing_expense[0] + new_expense
        cursor.execute("UPDATE expenses SET amount = ? WHERE category = ?", (updated_expense, category))
        conn.commit()
        print(f"Expense for '{category}' updated successfully. New expense: R{updated_expense:.2f}")
    else:
        cursor.execute("INSERT INTO expenses (category, amount) VALUES (?, ?)", (category, new_expense))
        conn.commit()
        print(f"Expense for '{category}' set to R{new_expense:.2f}")

def view_expenses():
    """View all expenses."""
    cursor.execute('''SELECT * FROM expenses''')
    expenses = cursor.fetchall()
    for expense in expenses:
        print(expense)

def view_expenses_by_category():
    """View expenses by category."""
    category = questionary.text("Enter the expense category to view:").ask()
    cursor.execute('''SELECT * FROM expenses WHERE category = ?''', (category,))
    expenses = cursor.fetchall()
    for expense in expenses:
        print(expense)

def add_income_category():
    """Add new income category using questionary."""
    category = questionary.text("Enter the income category:").ask()
    new_income = float(questionary.text("Enter the income amount:").ask())

    cursor.execute("SELECT amount FROM income WHERE category = ?", (category,))
    existing_income = cursor.fetchone()

    if existing_income:
        updated_income = existing_income[0] + new_income
        cursor.execute("UPDATE income SET amount = ? WHERE category = ?", (updated_income, category))
        conn.commit()
        print(f"Income for '{category}' updated successfully. New income: R{updated_income:.2f}")
    else:
        cursor.execute("INSERT INTO income (category, amount) VALUES (?, ?)", (category, new_income))
        conn.commit()
        print(f"Income for '{category}' set to R{new_income:.2f}")

def view_income():
    """View all income."""
    cursor.execute('''SELECT * FROM income''')
    income = cursor.fetchall()
    for entry in income:
        print(entry)

def view_income_by_category():
    """View income by category."""
    category = questionary.text("Enter the income category to view:").ask()
    cursor.execute('''SELECT * FROM income WHERE category = ?''', (category,))
    income = cursor.fetchall()
    for entry in income:
        print(entry)

def set_budget():
    """Set budget for a category."""
    category = questionary.text("Enter the category to set budget for:").ask()
    new_budget = float(questionary.text("Enter the new budget amount:").ask())

    cursor.execute("SELECT amount FROM budgets WHERE category = ?", (category,))
    existing_budget = cursor.fetchone()

    if existing_budget:
        updated_budget = existing_budget[0] + new_budget
        cursor.execute("UPDATE budgets SET amount = ? WHERE category = ?", (updated_budget, category))
        conn.commit()
        print(f"Budget for '{category}' updated successfully. New budget: R{updated_budget:.2f}")
    else:
        cursor.execute("INSERT INTO budgets (category, amount) VALUES (?, ?)", (category, new_budget))
        conn.commit()
        print(f"Budget for '{category}' set to R{new_budget:.2f}")

def view_budget():
    """View budget for a category."""
    category = questionary.text("Enter the category to view budget:").ask()

    cursor.execute("SELECT amount FROM budgets WHERE category = ?", (category,))
    budget = cursor.fetchone()

    if budget:
        cursor.execute("SELECT SUM(amount) FROM expenses WHERE category = ?", (category,))
        total_expenses = cursor.fetchone()[0]

        if total_expenses is None:
            total_expenses = 0.0

        available_budget = budget[0] - total_expenses

        cursor.execute("UPDATE budgets SET amount = ? WHERE category = ?", (available_budget, category))
        conn.commit()

        print(f"Budget for '{category}': R{budget[0]:.2f}")
        print(f"Total expenses: R{total_expenses:.2f}")
        print(f"Available budget: R{available_budget:.2f}")
    else:
        print(f"No budget found for '{category}'.")

def update_budget(amount):
    """Update budget amount."""

def set_financial_goals():
    """Set financial goals."""
    goal = questionary.text("Enter your financial goal:").ask()
    cursor.execute('''INSERT INTO financial_goals (goal, achieved) VALUES (?, 0)''', (goal,))
    conn.commit()
    update_progress()

def update_progress():
    """Update progress towards financial goals."""
    cursor.execute('''SELECT * FROM financial_goals''')
    goals = cursor.fetchall()

    for goal in goals:
        cursor.execute('''SELECT SUM(amount) FROM income''')
        total_income = cursor.fetchone()[0]

        cursor.execute('''SELECT SUM(amount) FROM expenses''')
        total_expenses = cursor.fetchone()[0]

        if total_income is None:
            total_income = 0.0

        if total_expenses is None:
            total_expenses = 0.0

        difference = total_income - total_expenses

        if difference >= float(goal[1]):
            cursor.execute('''UPDATE financial_goals SET achieved = 1 WHERE id = ?''', (goal[0],))
        else:
            cursor.execute('''UPDATE financial_goals SET achieved = 0 WHERE id = ?''', (goal[0],))
        conn.commit()

def view_progress_goals():
    """View progress towards financial goals."""
    cursor.execute('''SELECT * FROM financial_goals''')
    goals = cursor.fetchall()

    for goal in goals:
        if goal[2] == 1:
            status = "Achieved"
        else:
            status = "Not Achieved"
        print(f"{goal[1]} - {status}")



while True:
    user_choice = questionary.select("Choose an option:", ["Add Expense", "View Expenses", "View Expenses by Category", "Add Income", "View Income", "View Income by Category", "Set Budget for a Category", "View Budget for a Category", "Set Financial Goals", "View Progress Towards Financial Goals", "Quit"]).ask()

    if user_choice == "Add Expense":
        add_expense_category()
    elif user_choice == "View Expenses":
        view_expenses()
    elif user_choice == "View Expenses by Category":
        view_expenses_by_category()
    elif user_choice == "Add Income":
        add_income_category()
    elif user_choice == "View Income":
        view_income()
    elif user_choice == "View Income by Category":
        view_income_by_category()
    elif user_choice == "Set Budget for a Category":
        set_budget()
    elif user_choice == "View Budget for a Category":
        view_budget()
    elif user_choice == "Set Financial Goals":
        set_financial_goals()
    elif user_choice == "View Progress Towards Financial Goals":
        view_progress_goals()
    elif user_choice == "Quit":
        print("System shutting down. Goodbye!")
        break

conn.close()
