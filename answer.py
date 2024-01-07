
"""accounting system"""
import csv
from datetime import datetime
import random

ledger_file = "ledger.csv"


def get_last_entry(filename):
    """to get the last entry from ledger"""
    with open(filename, "r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        last_entry = list(reader)[-1]
    return last_entry


def get_last_balance(filename):
    """to get the last balance from ledger"""
    last_entry = get_last_entry(filename)
    return float(last_entry[5])


def credit(amount):
    """this is credit func"""
    last_entry = get_last_entry(ledger_file)
    new_balance = float(last_entry[1]) + amount
    ledger(
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        amount,
        "credit",
        "credit transaction",
        "Not_avail",
        new_balance,
    )
    return new_balance


def debit(amount):
    """Func to debit amount"""
    last_entry = get_last_entry(ledger_file)
    new_balance = float(last_entry[1]) - amount
    ledger(
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        amount,
        "debit",
        "debit transaction",
        "Not_avail",
        new_balance,
    )
    return new_balance


def transaction(amount, category, desc, mode_of_payment, credit=False):
    """Function to make a transaction"""

    if credit:
        credit(amount)
    else:
        debit(amount)
    return get_last_balance(ledger_file)


def ledger(date, amount, category, desc, mode_of_payment, balance):
    """Function to store all information in ledger"""
    with open(ledger_file, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([date, amount, category, desc, mode_of_payment, balance])


def generate_category_report(filename):
    """Function to generate category report"""
    categories = set()
    with open(filename, "r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            # print(row)
            categories.add(row[2])
    # print(categories)
    for category in categories:
        category_data = []
        with open(filename, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                if row[2] == category:
                    category_data.append([row[0], row[3], row[1], row[4]])

        category_filename = f"{category}.csv"
        with open(
            category_filename, "w", newline="", encoding="utf-8"
        ) as category_file:
            writer = csv.writer(category_file)
            writer.writerow(["date", "descriptions", "Amount", "mode of Payment"])
            writer.writerows(category_data)


def generate_payment_report(filename):
    """to generate payment report"""
    payments = set()
    with open(filename, "r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            payments.add(row[4])

    for payment in payments:
        payment_data = []
        with open(filename, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                if row[4] == payment:
                    payment_data.append([row[0], row[2], row[1], row[3]])

        payment_filename = f"{payment}.csv"
        with open(payment_filename, "w", newline="", encoding="utf-8") as payment_file:
            writer = csv.writer(payment_file)
            writer.writerow(["date", "category", "amount", "descriptions"])
            writer.writerows(payment_data)


def print_reports():
    """print report"""
    categories = set()
    months = set()
    data = {}

    with open(ledger_file, "r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            date = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
            month = date.strftime("%B")
            category = row[2]
            categories.add(category)
            months.add(month)

            if category not in data:
                data[category] = {}
            if month not in data[category]:
                data[category][month] = 0
            data[category][month] += float(row[1])

    all_months = sorted(list(months))
    print("\t".join(["Category"] + all_months))
    for category, month_data in data.items():
        values = [f"{month_data.get(month, 0):.2f}" for month in all_months]
        print("\t".join([category] + values))

    return data


def generate_txt(report_data):
    """to generate text file"""
    with open("report.txt", "w", encoding="utf-8") as file:
        for cat, month in report_data.items():
            file.write(
                cat
                + "\t"
                + "\t".join(f"{m}: {amount:.2f}" for m, amount in month.items())
                + "\n"
            )


def generate_random_data():
    """this creates random data for checking"""
    categories = ["Food", "Rent", "Utilities", "Entertainment", "Travel"]
    descriptions = ["Groceries", "Restaurant", "Internet", "Movie", "Flight"]
    modes_of_payment = ["Credit Card", "Debit Card", "Cash", "G-pay", "Paytm"]

    for _ in range(10):
        amount = round(random.randint(1000, 10000))
        category = random.choice(categories)
        desc = random.choice(descriptions)
        mode_of_payment = random.choice(modes_of_payment)
        credit_amount = random.choice([True, False])

        if credit_amount:
            credit(amount)
        else:
            debit(amount)

        ledger(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            amount,
            category,
            desc,
            mode_of_payment,
            get_last_balance(ledger_file),
        )


if __name__ == "__main__":
    generate_random_data()
    report_data = print_reports()
    print_reports()
    generate_category_report(ledger_file)
    generate_txt(report_data)
    print(credit(4000))
    print(debit(2000))
