# FinTrack

A simple GUI or CLI tool to keep track of finances. Users can add, categorize and view information about transactions.

# Screenshots

## GUI

![GUI Screenshot](https://i.imgur.com/gmhlwGn.gif)

## CLI

![CLI Screenshot](https://i.imgur.com/TVIMag0.png)

# Features

- Add expese or income transactions with categories (e.g. Utility, Rent, Groceries, etc...).
- Show the sum of expense or income transactions.
- Show the current balance.
- Show transactions filtered by category.
- Persistant storage using a JSON file for reuse across sessions.
- GUI for easy operation by user.
- Exception handling for invalid inputs.

# Technologies

- Python 3.11.6
- JSON for data storage
- PySide6 (QT for Python) for GUI creation
- Built-in libraries: datetime, enum, json, os

# Setup

1. Clone the repository:

```
git clone https://github.com/RenDev00/finance_tracker.git
```

2. Navigate to the cloned repository:

```
cd finance_tracker
```

3. Install the requirements:

```
pip install -r requirements.txt
```

4. Run the application:

- CLI

```
python ./src/main_cli.py
```

- GUI

```
python ./src/main_gui.py
```

# Usage

## For CLI:

Run the program and follow the menu prompts.

Example commands:

- Add a transaction: Choose option 1, enter amount, type [expense / income], and category.
- Filter by category: Choose option 6, enter category.

## For GUI:

Run the program and follow the menu prompts.

Example commands:

- Add a transaction: Click the "Add" button and provide the necessary information.
- Filter and search: Enter a search term in the search bar and select whether to display all or only expense or income transactions using the dropdown.

# License

MIT License
