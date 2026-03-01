from model.finance_tracker import FinanceTracker
from model.transaction import TransactionCategory, TransactionType


def add_transaction_cli(tracker: FinanceTracker):
    amount = input("Amount: ")
    transaction_type = input("Transaction type [expense / income]: ")

    try:
        amount = float(amount)
    except ValueError:
        print(f"Error, {amount} is not a number")
        return

    try:
        transaction_type = TransactionType[transaction_type.upper()]
    except KeyError:
        print(f"Error, invalid transaction type {transaction_type}")
        return

    if transaction_type == TransactionType.EXPENSE:
        transaction_category = input("Transaction category [need / want / saving]: ")
    else:
        transaction_category = input(
            "Transaction category [salary / scholarship / pocket money / other]: "
        )

    transaction_details = input("Transaction details: ")

    try:
        transaction_category = TransactionCategory[
            transaction_category.upper().replace(" ", "_")
        ]
    except KeyError:
        print(f"Error, invalid transaction category {transaction_category}")
        return

    try:
        tracker.add_transaction(
            amount, transaction_type, transaction_category, transaction_details
        )
    except ValueError as e:
        print(f"Error, {e}")


def print_transactions_by_type_cli(tracker: FinanceTracker):
    t_type = input("Type [income / expense]: ")
    try:
        transaction_type = TransactionType[t_type.upper()]
    except KeyError:
        print(f"Error, invalid transaction type {t_type}")
        return

    transactions = tracker.get_transactions_by_type(transaction_type)
    for t in transactions:
        print(t)


def print_transactions_by_category_cli(tracker: FinanceTracker):
    t_category = input("Category [need / want / saving]: ")
    try:
        transaction_category = TransactionCategory[t_category.upper()]
    except KeyError:
        print(f"Error, invalid transaction category {t_category}")
        return
    transactions = tracker.get_transactions_by_category(transaction_category)
    for t in transactions:
        print(t)


def main():
    tracker = FinanceTracker("./data/sample_data.json")

    cont = True
    while cont:
        print("\nFinance Tracker")
        print("1. Add Transaction")
        print("2. Show Total Income")
        print("3. Show Total Expenses")
        print("4. Show Balance")
        print("5. Show by Type")
        print("6. Show by Category")
        print("7. Exit")

        choice = input("Choose from action 1 - 7: ")
        try:
            choice = int(choice)
        except ValueError:
            print(f"Error, {choice} is not a number")
            continue

        if not 0 < choice <= 7:
            print(f"Error, invalid action {choice}")
            continue

        match (choice):
            case 1:
                add_transaction_cli(tracker)
            case 2:
                print(f"Your total income is {round(tracker.get_total_income(), 2)}")
            case 3:
                print(
                    f"Your total expenses are {round(tracker.get_total_expenses(), 2)}"
                )
            case 4:
                print(f"Your balance is {round(tracker.get_balance(), 2)}")
            case 5:
                print_transactions_by_type_cli(tracker)
            case 6:
                print_transactions_by_category_cli(tracker)
            case 7:
                cont = False

    else:
        print("Finance Tracker exited")


if __name__ == "__main__":
    main()
