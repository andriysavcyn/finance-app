"""
config.py
Ресурсна база: кольори, шрифти, переклади, категорії.
"""

# Кольори
COLORS = {
    "bg": "#0D1117",  # основний фон
    "surface": "#161B22",  # картки і панелі
    "surface2": "#21262D",  # рядки таблиці, інпути
    "accent": "#8B5CF6",  # фіолетовий акцент
    "income": "#2EA043",  # зелений — дохід
    "expense": "#F85149",  # червоний — витрата
    "neutral": "#58A6FF",  # блакитний — баланс
    "text": "#C9D1D9",
    "text_dim": "#8B949E",  # підписи, підказки
    "border": "#30363D",
    "hover": "#2D333B",
    "warning": "#D29922",
}

# Шрифти
FONTS = {
    "title": ("Segoe UI", 18, "bold"),
    "heading": ("Segoe UI", 12, "bold"),
    "body": ("Segoe UI", 10),
    "small": ("Segoe UI", 9),
    "mono": ("Consolas", 11),
    "big": ("Segoe UI", 24, "bold"),
}

# Переклади двома мовами UA & EN
TRANSLATIONS = {
    "ua": {
        "app_title": "💰 Фінансовий менеджер",
        "menu_file": "Файл",
        "menu_export": "Експорт CSV...",
        "menu_import": "Змінити файл даних...",
        "menu_exit": "Вихід",
        "menu_view": "Вигляд",
        "menu_lang": "Мова → English",
        "menu_theme": "Тема",
        "menu_help": "Довідка",
        "menu_about": "Про програму",
        "tab_dash": "📊 Дашборд",
        "tab_trans": "📋 Транзакції",
        "tab_stats": "📈 Статистика",
        "lbl_income": "Загальна сума доходів",
        "lbl_expense": "Загальна сума витрат",
        "lbl_balance": "Баланс",
        "lbl_this_month": "Цього місяця",
        "lbl_recent": "5 останніх транзакцій",
        "btn_add": "+ Додати",
        "btn_edit": "✏ Редагувати",
        "btn_delete": "🗑 Видалити",
        "btn_refresh": "⟳ Оновити",
        "btn_save": "Зберегти",
        "btn_cancel": "Скасувати",
        "btn_export": "Експорт CSV",
        "col_date": "Дата",
        "col_type": "Тип",
        "col_category": "Категорія",
        "col_desc": "Опис",
        "col_amount": "Сума",
        "income_lbl": "Дохід",
        "expense_lbl": "Витрата",
        "dlg_add_title": "Додати транзакцію",
        "dlg_edit_title": "Редагувати транзакцію",
        "fld_type": "Тип",
        "fld_amount": "Сума",
        "fld_category": "Категорія",
        "fld_desc": "Опис",
        "fld_date": "Дата (РРРР-ММ-ДД)",
        "fld_currency": "Валюта",
        "filter_all": "Всі",
        "filter_type": "Фільтр за типом транзакції:",
        "filter_cat": "Категорія транзакції:",
        "filter_search": "Пошук:",
        "sort_by": "Сортувати:",
        "sort_date": "Дата",
        "sort_amount": "Сума",
        "sort_category": "Категорія",
        "sort_manual": "Ручне",
        "err_amount": "Введіть коректну суму (число > 0)",
        "err_date": "Невірний формат дати. Використовуйте РРРР-ММ-ДД",
        "err_select": "Спочатку оберіть транзакцію",
        "err_empty": "Заповніть усі обов'язкові поля",
        "msg_deleted": "Транзакцію видалено",
        "msg_saved": "CSV-файл збережено: ",
        "ask_delete": "Видалити цю транзакцію?",
        "about_text": "Фінансовий менеджер v1.0\nРозробник: Андрій Савчин\nГрупа: ПП-21\nNULP, 2026",
        "no_data": "Немає даних",
        "monthly": "Динаміка витрат і доходів по місяцях",
        "by_category": "Витрати за категоріями",
        "stat_income_cat": "Доходи за категоріями",
        "progress_lbl": "Витрати відносно доходів",
        "drag_hint": "Перетягніть транзакцію щоб змінити порядок",
        "note_multicurrency": "* Дашборд конвертує всі валюти в UAH",
    },
    "en": {
        "app_title": "💰 Finance Manager",
        "menu_file": "File",
        "menu_export": "Export CSV...",
        "menu_import": "Change data file...",
        "menu_exit": "Exit",
        "menu_view": "View",
        "menu_lang": "Language → Українська",
        "menu_theme": "Theme",
        "menu_help": "Help",
        "menu_about": "About",
        "tab_dash": "📊 Dashboard",
        "tab_trans": "📋 Transactions",
        "tab_stats": "📈 Statistics",
        "lbl_income": "Total incomes",
        "lbl_expense": "Total expenses",
        "lbl_balance": "Balance",
        "lbl_this_month": "This month",
        "lbl_recent": "Last 5 transactions",
        "btn_add": "+ Add",
        "btn_edit": "✏ Edit",
        "btn_delete": "🗑 Delete",
        "btn_refresh": "⟳ Refresh",
        "btn_save": "Save",
        "btn_cancel": "Cancel",
        "btn_export": "Export CSV",
        "col_date": "Date",
        "col_type": "Type",
        "col_category": "Category",
        "col_desc": "Description",
        "col_amount": "Amount",
        "income_lbl": "Income",
        "expense_lbl": "Expense",
        "dlg_add_title": "Add Transaction",
        "dlg_edit_title": "Edit Transaction",
        "fld_type": "Type",
        "fld_amount": "Amount",
        "fld_category": "Category",
        "fld_desc": "Description",
        "fld_date": "Date (YYYY-MM-DD)",
        "fld_currency": "Currency",
        "filter_all": "All",
        "filter_type": "Filter by transaction type:",
        "filter_cat": "Transaction category:",
        "filter_search": "Search:",
        "sort_by": "Sort by:",
        "sort_date": "Date",
        "sort_amount": "Amount",
        "sort_category": "Category",
        "sort_manual": "Manual",
        "err_amount": "Enter a valid amount (number > 0)",
        "err_date": "Invalid date format. Use YYYY-MM-DD",
        "err_select": "Please select a transaction first",
        "err_empty": "Please fill all required fields",
        "msg_deleted": "Transaction deleted",
        "msg_saved": "CSV saved: ",
        "ask_delete": "Delete this transaction?",
        "about_text": "Finance Manager v1.0\nDeveloper: Andriy Savchyn\nGroup: PP-21\nNULP, 2026",
        "no_data": "No data",
        "monthly": "Dynamics of expenses and income by month",
        "by_category": "Expenses by category",
        "stat_income_cat": "Income by category",
        "progress_lbl": "Expenses vs Income",
        "drag_hint": "Drag a transaction to reorder",
        "note_multicurrency": "* Dashboard converts all currencies to UAH",
    },
}

# Категорії транзакцій для UA & EN
CATEGORIES = {
    "ua": {
        "income": ["Зарплата", "Фріланс", "Подарунок", "Інвестиції", "Інше"],
        "expense": [
            "Їжа",
            "Транспорт",
            "Комунальні",
            "Розваги",
            "Одяг",
            "Здоров'я",
            "Освіта",
            "Інше",
        ],
    },
    "en": {
        "income": ["Salary", "Freelance", "Gift", "Investments", "Other"],
        "expense": [
            "Food",
            "Transport",
            "Utilities",
            "Entertainment",
            "Clothing",
            "Health",
            "Education",
            "Other",
        ],
    },
}


def tr(lang: str, key: str) -> str:
    # Тягне переклад для інтерфейсу (кнопки, лейбли) зі словника TRANSLATIONS.
    return TRANSLATIONS.get(lang, TRANSLATIONS["ua"]).get(key, key)


def tr_cat(category_name: str, target_lang: str) -> str:
    # Переклад для самих категорій транзакцій (Зарплата, Їжа і т.д.).
    target_flat = (
        CATEGORIES[target_lang]["income"] + CATEGORIES[target_lang]["expense"]
    )
    if category_name in target_flat:
        return category_name

    source_lang = "en" if target_lang == "ua" else "ua"
    source_flat = (
        CATEGORIES[source_lang]["income"] + CATEGORIES[source_lang]["expense"]
    )
    try:
        return target_flat[source_flat.index(category_name)]
    except (ValueError, IndexError):
        return category_name