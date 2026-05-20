"""
model.py — Model шар (MVC)
Відповідає за дані, бізнес-логіку та збереження/завантаження.
"""

import os
import csv
import json
import urllib.request
from typing import List, Optional
from dataclasses import dataclass, asdict

@dataclass
class Transaction:
    # Структура даних для однієї транзакції
    id: int
    type: str  # "income" | "expense"
    amount: float
    category: str
    description: str
    date: str  # ISO format YYYY-MM-DD
    currency: str = "UAH"

    def to_dict(self):
        # Конвертування в словник для збереження в JSON
        return asdict(self)

    @staticmethod
    def from_dict(d: dict) -> "Transaction":
        # Розпакування даних зі словника
        return Transaction(**d)


class FinanceModel:
    # Головна модель даних. Зберігає транзакції та надає методи аналізу
    DEFAULT_RATES = {
        "UAH": 1,
        "USD": 43.8,
        "EUR": 51.6,
        "GBP": 58.65,
        "PLN": 12,
    }

    def __init__(self, data_path: str = "finance_data.json"):
        self.data_path = data_path
        self.transactions: List[Transaction] = []
        self._next_id: int = 1
        self.rates = self.DEFAULT_RATES.copy()

        self.load()
        self.update_rates_from_api()

    def update_rates_from_api(self):
        # Отримання актуального курсу валют з API НБУ
        try:
            url = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"
            with urllib.request.urlopen(url, timeout=3) as response:
                api_data = json.loads(response.read().decode())
                for item in api_data:
                    code = item.get("cc")
                    rate = item.get("rate")
                    if code in self.rates:
                        self.rates[code] = float(rate)
            print("Курси валют успішно оновлено через API НБУ.")
        except Exception as e:
            print(f"API недоступне, використано стандартні курси. Помилка: {e}")

    def _to_base(self, amount: float, currency: str) -> float:
        # Конвертування суми у UAH, використовуючи актуальні курси
        rate = self.rates.get(currency, 1.0)
        return amount * rate

    def add_transaction(
        # Створення нового запису, присвоєння йому унікального ID і зберігання у файл
        self,
        type_: str,
        amount: float,
        category: str,
        description: str,
        date: str,
        currency: str = "UAH",
    ) -> Transaction:
        t = Transaction(
            id=self._next_id,
            type=type_,
            amount=round(amount, 2),
            category=category,
            description=description,
            date=date,
            currency=currency,
        )
        self.transactions.append(t)
        self._next_id += 1
        self.save()
        return t

    def update_transaction(self, id_: int, **kwargs) -> bool:
        # Пошук транзакцій по ID і оновлювання в них тільки тих полів, які передали.
        for t in self.transactions:
            if t.id == id_:
                for k, v in kwargs.items():
                    setattr(t, k, v)
                self.save()
                return True
        return False

    def delete_transaction(self, id_: int) -> bool:
        # Видалення певної транзакції
        for i, t in enumerate(self.transactions):
            if t.id == id_:
                self.transactions.pop(i)
                self.save()
                return True
        return False

    def get_by_id(self, id_: int) -> Optional[Transaction]:
        # Витяг транзакції за її ID
        return next((t for t in self.transactions if t.id == id_), None)

    def filter(
        self,
        type_: str = None,
        category: str = None,
    ) -> List[Transaction]:
        # Відсіювання транзакції за типом або категорією. Повертання нового список.
        result = self.transactions[:]
        if type_:
            result = [t for t in result if t.type == type_]
        if category:
            result = [t for t in result if t.category == category]
        return result

    def sort(
        self,
        transactions: List[Transaction],
        key: str = "date",
        reverse: bool = True,
    ) -> List[Transaction]:
        # Сортування транзакції по потрібному критерію (дата, сума тощо) або ручне (Drag & Drop). За дефолтом — дата.
        return sorted(
            transactions, key=lambda t: getattr(t, key), reverse=reverse
        )

    def search(self, query: str) -> List[Transaction]:
        # Пошук по тексту опису або категорії
        q = query.lower()
        return [
            t
            for t in self.transactions
            if q in t.description.lower() or q in t.category.lower()
        ]

    def total_income(self, transactions: List[Transaction] = None) -> float:
        # Рахування загальної суми доходу (з конвертацією в гривні)
        src = transactions if transactions is not None else self.transactions
        # Конвертуємо кожну суму перед додаванням
        return round(
            sum(
                self._to_base(t.amount, t.currency)
                for t in src
                if t.type == "income"
            ),
            2,
        )

    def total_expense(self, transactions: List[Transaction] = None) -> float:
        # Рахування загальної суми витрат (з конвертацією в гривні)
        src = transactions if transactions is not None else self.transactions
        return round(
            sum(
                self._to_base(t.amount, t.currency)
                for t in src
                if t.type == "expense"
            ),
            2,
        )

    def balance(self, transactions: List[Transaction] = None) -> float:
        # Рахування поточного балансу (з конвертацією в гривні)
        return round(
            self.total_income(transactions) - self.total_expense(transactions),
            2,
        )

    def by_category(
        self, type_: str, transactions: List[Transaction] = None
    ) -> dict:
        # Групування сум по категоріях для кругової діаграми
        src = transactions if transactions is not None else self.transactions
        result = {}
        for t in src:
            if t.type == type_:
                # Конвертуємо суму
                base_amount = self._to_base(t.amount, t.currency)
                result[t.category] = round(
                    result.get(t.category, 0) + base_amount, 2
                )
        return dict(sorted(result.items(), key=lambda x: x[1], reverse=True))

    def monthly_summary(self) -> dict:
        #  Збирання статистики по місяцях (YYYY-MM) для стовпчикового графіка.
        summary = {}
        for t in self.transactions:
            month = t.date[:7]
            if month not in summary:
                summary[month] = {"income": 0.0, "expense": 0.0}

            base_amount = self._to_base(t.amount, t.currency)
            summary[month][t.type] = round(
                summary[month][t.type] + base_amount, 2
            )

        for m in summary:
            summary[m]["balance"] = round(
                summary[m]["income"] - summary[m]["expense"], 2
            )
        return dict(sorted(summary.items()))

    def save(self):
        # Скидання всіх даних в JSON файл. Викликається при кожній зміні бази
        data = {
            "next_id": self._next_id,
            "transactions": [t.to_dict() for t in self.transactions],
        }
        with open(self.data_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load(self):
        #  Підтягування даних з JSON при старті програми
        if not os.path.exists(self.data_path):
            return
        try:
            with open(self.data_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.transactions = [
                Transaction.from_dict(d) for d in data.get("transactions", [])
            ]
            if self.transactions:
                max_id = max(t.id for t in self.transactions)
                self._next_id = max_id + 1
            else:
                self._next_id = data.get("next_id", 1)

        except (json.JSONDecodeError, KeyError) as e:
            self.transactions = []
            self._next_id = 1

    def export_csv(self, path: str, transactions: List[Transaction] = None):
        # Вивантажування список транзакцій у CSV, щоб можна було відкрити в Excel.
        src = transactions if transactions is not None else self.transactions
        with open(path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "id",
                    "date",
                    "type",
                    "category",
                    "description",
                    "amount",
                    "currency",
                ],
            )
            writer.writeheader()
            for t in src:
                writer.writerow(t.to_dict())
