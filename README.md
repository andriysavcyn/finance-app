# 💰 Personal Finance Manager

A cross-platform desktop application built with Python and Tkinter for tracking personal finances. The project is designed using the **Model-View-Controller (MVC)** architectural pattern to ensure a clean separation of concerns, high maintainability, and scalable code.

## ✨ Key Features

* **Complete CRUD Operations:** Easily add, edit, delete, and view income and expense transactions.
* **Multi-Currency Support:** Handles UAH, USD, EUR, GBP, and PLN with automatic real-time exchange rate updates via the National Bank of Ukraine (NBU) API.
* **Interactive Dashboard:** Features dynamic bar charts for monthly trends and pie charts for expense/income categories, along with a real-time budget progress bar.
* **Advanced Data Management:** Supports filtering by category/type, sorting by multiple parameters, text search, and manual drag-and-drop reordering.
* **Dynamic Localization:** Instantly switch between English and Ukrainian UI without restarting the application.
* **Zero External Dependencies:** Built entirely using Python's standard libraries (Tkinter, json, urllib, csv). No virtual environments or external packages (like `pandas` or `matplotlib`) are required to run the app.
* **Local Persistence & Export:** Automatically saves data to a local JSON file ensuring full user privacy, with the ability to export records to a CSV file for spreadsheet analysis.

## 🏗️ Architecture (MVC)

The application strictly follows the MVC pattern:

* **`model.py` (Model):** Contains the core business logic. Manages the `Transaction` data class, handles JSON serialization/deserialization, performs currency conversions, fetches API data, and processes statistical calculations.
* **`view.py` (View):** Responsible solely for the Graphical User Interface. Utilizes `tkinter` and `ttk` to render styled components, dialog windows, and custom canvas-based charts. Contains no business logic.
* **`controller.py` (Controller):** Acts as the bridge between the Model and View. Binds UI events (clicks, text input, drag-and-drop) to Model updates, and triggers View refreshes when data changes.

## 📂 Project Structure

```text
├── main.py              # Application entry point
├── controller.py        # MVC Controller (FinanceController)
├── model.py             # MVC Model (FinanceModel, Transaction)
├── view.py              # MVC View (MainView, TransactionDialog)
├── config.py            # App configurations (colors, fonts, translations)
├── finance_data.json    # Local database (auto-generated)
└── docs/                # Project documentation

How to Run

Since the project uses only Python's standard libraries, installation is incredibly simple.

1. Clone the repository:

git clone [https://github.com/yourusername/finance-manager.git](https://github.com/yourusername/finance-manager.git)
cd finance-manager

2. Run the application (requires Python 3.10+):

python main.py
(Use python3 main.py on macOS/Linux)