
import csv
import datetime


class DataError(Exception):
    def __init__(self, message):
        self.message = message


class AccountType:
    CHECKING = "1"
    SAVINGS = "2"


DOCTEST = False
FILE = "account.csv"
LOGGING_FILE = "logging.csv"


def log_event(event_type: str, success: bool, time: datetime):
    with open(LOGGING_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["event_type", "success", "date"])
        f.seek(2)
        writer.writerow({"event_type": event_type, "success": success, "date": time})


def open_file() -> list:
    try:
        with open(FILE, "r") as f:
            reader = csv.DictReader(f)
            account_details = [account for account in reader]
        if not account_details:
            raise DataError("account unavailable")
        return account_details
    except FileNotFoundError as e:
        raise FileNotFoundError("database not found")


def write_file(account_details: list):
    with open(FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=account_details[0].keys())
        writer.writeheader()
        writer.writerows(account_details)


def withdraw():
    event = "withdraw"
    try:
        account_details = open_file()
        checking, savings = float(account_details[0]["checking"]), float(account_details[0]["savings"])
        selection = input("which account do you want to withdraw from?\n1. Checking  2. Savings\n>>>: ")
        amount = float(input("how much do you want to withdraw?: "))
        if selection == AccountType.CHECKING:
            if amount <= checking:
                account_details[0]["checking"] = checking - amount
                write_file(account_details)
                log_event(event, True, datetime.datetime.now())
            else:
                print("insufficient funds")
                log_event(event, False, datetime.datetime.now())
        elif selection == AccountType.SAVINGS:
            if amount <= savings:
                account_details[0]["savings"] = savings - amount
                write_file(account_details)
                log_event(event, True, datetime.datetime.now())
            else:
                print("insufficient funds")
                log_event(event, False, datetime.datetime.now())
    except (DataError, FileNotFoundError, ValueError) as e:
        log_event(event, False, datetime.datetime.now())
        print(e)


def deposit():
    event = "deposit"
    try:
        account_details = open_file()
        checking, savings = float(account_details[0]["checking"]), float(account_details[0]["savings"])
        selection = input("which account do you want to deposit to?\n1. Checking  2. Savings\n>>>: ")
        amount = float(input("how much do you want to deposit?: "))
        if selection == AccountType.CHECKING:
            account_details[0]["checking"] = checking + amount
            write_file(account_details)
            log_event(event, True, datetime.datetime.now())
        elif selection == AccountType.SAVINGS:
            account_details[0]["savings"] = savings + amount
            write_file(account_details)
            log_event(event, True, datetime.datetime.now())
    except (DataError, FileNotFoundError, ValueError) as e:
        log_event(event, False, datetime.datetime.now())


def transfer():
    event = "transfer"
    try:
        account_details = open_file()
        checking, savings = float(account_details[0]["checking"]), float(account_details[0]["savings"])
        selection = input("which account do you want to transfer to?\n1. Checking  2. Savings\n>>>: ")
        amount = float(input("how much do you want to transfer?: "))
        if selection == AccountType.CHECKING:
            if amount <= savings:
                account_details[0]["checking"] = checking + amount
                account_details[0]["savings"] = savings - amount
                write_file(account_details)
                log_event(event, True, datetime.datetime.now())
            else:
                print("insufficient funds")
                log_event(event, False, datetime.datetime.now())
        elif selection == AccountType.SAVINGS:
            if amount <= checking:
                account_details[0]["savings"] = savings + amount
                account_details[0]["checking"] = checking - amount
                write_file(account_details)
                log_event(event, True, datetime.datetime.now())
            else:
                print("insufficient funds")
                log_event(event, False, datetime.datetime.now())
    except (DataError, FileNotFoundError, ValueError) as e:
        log_event(event, False, datetime.datetime.now())


def balance():
    event = "view balance"
    try:
        account_details = open_file()
        checking, savings = float(account_details[0]["checking"]), float(account_details[0]["savings"])
        print(f"you have a balance of: Checking ${checking:.2f} | Savings ${savings:.2f}")
        log_event(event, True, datetime.datetime.now())
    except (DataError, FileNotFoundError) as e:
        log_event(event, False, datetime.datetime.now())


def main():
    print("WELCOME TO CODERS BANK")
    account_details = open_file()
    pin = account_details[0]["pin"]
    functions = {"1": withdraw, "2": deposit, "3": transfer, "4": balance}
    for _ in range(30):
        entered_pin = input("enter your pin: ")
        if entered_pin == pin:
            selection = input("What would you like to do?\n"
                              "1. Withdraw  2. Deposit\n"
                              "3. Transfer  4. Balance\n"
                              "5. Exit\n"
                              ">>>:")
            if selection == "5":
                break
            else:
                functions[selection]()
        else:
            print("wrong pin!")


if __name__ == '__main__':
    main()
