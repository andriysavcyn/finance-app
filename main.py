"""
main.py — Точка входу додатка
Особистий фінансовий менеджер
Курсова робота з дисципліни «Розробка кросплатформенних додатків»
Студент: Андрій Савчин, гр. ПП-21, НУЛП, 2026
"""

from controller import FinanceController

if __name__ == "__main__":
    app = FinanceController()
    app.run()
