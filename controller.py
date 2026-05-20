""" 
controller.py
З'єднує Model і View: реагує на події, викликає модель, оновлює інтерфейс.
"""

from tkinter import filedialog, messagebox
from model import FinanceModel
from view import MainView, TransactionDialog
from config import tr, tr_cat, COLORS, FONTS, CATEGORIES


class FinanceController:

    def __init__(self):
        self.model = FinanceModel()
        self.view = MainView()

        if getattr(self.model, "_load_error", None):
            messagebox.showwarning(
                "Помилка даних",
                f"Файл даних пошкоджено і не може бути прочитаний.\n"
                f"Розпочато з порожнього списку.\n\nДеталі: {self.model._load_error}",
            )

        self._wire_callbacks()
        self._update_filter_options()
        self.refresh()

    def _wire_callbacks(self):
        # Прив'язування функції до кнопок, менюшок та подій (кліки, зміни в тексті)
        v = self.view
        # для кнопок
        v.btn_add.config(command=self.on_add)
        v.btn_edit.config(command=self.on_edit)
        v.btn_delete.config(command=self.on_delete)
        v.btn_export.config(command=self.on_export_csv)
        v.btn_lang.config(command=self.on_toggle_lang)
        # для меню
        v._on_export_csv = self.on_export_csv
        v._on_change_file = self.on_change_file
        v._on_toggle_lang = self.on_toggle_lang

        v._file_menu.entryconfig(0, command=self.on_export_csv)
        v._file_menu.entryconfig(1, command=self.on_change_file)
        v._help_menu.entryconfig(
            0,
            command=lambda: messagebox.showinfo(
                "About", tr(v.lang, "about_text")
            ),
        )
        # для контекстного меню на вкладці транзакції
        v.context_menu.entryconfig(0, command=self.on_edit)
        v.context_menu.entryconfig(1, command=self.on_delete)
        # для фільтрів, сортувань та пошуку транзакцій
        v.filter_type_var.trace_add(
            "write", lambda *_: (self._update_category_filter(), self.refresh())
        )
        v.filter_cat_var.trace_add("write", lambda *_: self.refresh())
        v.sort_var.trace_add("write", lambda *_: self.refresh())
        v.search_var.trace_add("write", lambda *_: self.refresh())
        # Перевірка, коли здійснюється перехід на 3 вкладку "Статистика" чи потрібно малювати графіки?
        v.notebook.bind("<<NotebookTabChanged>>", self._on_tab_changed)
        # Слідкування за розміром вікна, щоб перемальовувати графіки
        self._last_canvas_size = {}
        for canvas in (v.monthly_canvas, v.stat_exp_canvas, v.stat_inc_canvas):
            canvas.bind("<Configure>", self._on_canvas_resize)

        def _on_drag(new_order):
            # Ручне перетягування рядків у таблиці (drag & drop)
            new_order_ids = [int(tid) for tid in new_order]
            lookup = {t.id: t for t in self.model.transactions}

            self.model.transactions = [
                lookup[tid] for tid in new_order_ids if tid in lookup
            ]
            self.model.save()

            self.view.sort_var.set(tr(self.view.lang, "sort_manual"))

            self.refresh()

        self.view._drag_callback = _on_drag

    def refresh(self):
        # Комплексне оновлення всього, що є на екрані, після будь-якої зміни
        self._repopulate_tree()
        self._update_dashboard()
        self._draw_charts()

    def _get_filtered_sorted(self):
        # Витягування даних з моделі для застосування до них поточних фільтрів (за типом та категорією транзакції) та сортувань (за датою, категорією сумою та ручне)
        v = self.view
        lang = v.lang

        type_val = v.filter_type_var.get()
        cat_val = v.filter_cat_var.get()
        search = v.search_var.get().strip()
        all_lbl = tr(lang, "filter_all")

        type_key = None
        if type_val == tr(lang, "income_lbl"):
            type_key = "income"
        elif type_val == tr(lang, "expense_lbl"):
            type_key = "expense"

        cat_key = None if cat_val == all_lbl else cat_val

        data = self.model.filter(type_=type_key, category=cat_key)

        if search:
            q = search.lower()
            data = [
                t
                for t in data
                if q in t.description.lower() or q in t.category.lower()
            ]

        sort_val = v.sort_var.get()

        if sort_val == tr(lang, "sort_manual"):
            return data

        sort_map = {
            tr(lang, "sort_date"): "date",
            tr(lang, "sort_amount"): "amount",
            tr(lang, "sort_category"): "category",
        }
        return self.model.sort(data, key=sort_map.get(sort_val, "date"))

    def _repopulate_tree(self):
        # Очищання головної таблиці і занесення туди актуальних відфільтрованих даних
        tree = self.view.tree
        tree.delete(*tree.get_children())

        lang = self.view.lang
        type_labels = {
            "income": tr(lang, "income_lbl"),
            "expense": tr(lang, "expense_lbl"),
        }

        for i, t in enumerate(self._get_filtered_sorted()):
            sign = "+" if t.type == "income" else "−"
            amount = f"{sign}{t.amount:,.2f} {t.currency}"
            tags = (t.type, "even" if i % 2 == 0 else "odd")
            tree.insert(
                "",
                "end",
                iid=str(t.id),
                tags=tags,
                values=(
                    t.id,
                    t.date,
                    type_labels[t.type],
                    tr_cat(t.category, lang),
                    t.description,
                    amount,
                    t.currency,
                ),
            )

    def _update_dashboard(self):
        # Перераховування всіх цифри на головній вкладці (загальна сума доходів і витрат, баланс)
        v = self.view
        data = self.model.transactions

        income = self.model.total_income(data)
        expense = self.model.total_expense(data)
        balance = self.model.balance(data)

        def fmt(val):
            return f"{val:,.2f}"

        v.card_income._val_label.config(text=fmt(income))
        v.card_expense._val_label.config(text=fmt(expense))

        bal_color = COLORS["income"] if balance >= 0 else COLORS["expense"]
        v.card_balance._val_label.config(text=fmt(balance), fg=bal_color)

        pct = min(expense / income * 100, 100) if income > 0 else 0
        v.progress_var.set(pct)
        v.progress_pct_lbl.config(text=f"{pct:.0f}%")
        bar_color = (
            COLORS["income"]
            if pct < 70
            else COLORS["warning"] if pct < 90 else COLORS["expense"]
        )
        v._apply_ttk_style(bar_color)

        rt = v.recent_tree
        rt.delete(*rt.get_children())
        for t in sorted(data, key=lambda x: x.date, reverse=True)[:5]:
            sign = "+" if t.type == "income" else "−"
            rt.insert(
                "",
                "end",
                values=(
                    t.date,
                    t.description[:18],
                    f"{sign}{t.amount:.2f}",
                    t.currency,
                ),
            )

    def _on_tab_changed(self, event):
        # Малювання графіків при переході на вкладку "Статистика"
        if self.view.notebook.index("current") == 2:
            self._draw_charts()

    def _on_canvas_resize(self, event):
        # Метод для масштабування графіків
        key = str(event.widget)
        new_size = (event.width, event.height)
        if self._last_canvas_size.get(key) == new_size:
            return
        self._last_canvas_size[key] = new_size
        self._draw_charts()

    def _draw_charts(self):
        # Перемалювання графіків при зміні даних або розміру вікна
        self._draw_monthly_bar()
        self._draw_pie(
            self.view.stat_exp_canvas, self.model.by_category("expense")
        )
        self._draw_pie(
            self.view.stat_inc_canvas, self.model.by_category("income")
        )

    def _draw_monthly_bar(self):
        # Малювання стовпчикової діаграми доходів/витрат за останні півроку по місяцях
        canvas = self.view.monthly_canvas
        canvas.delete("all")
        canvas.update_idletasks()
        W = canvas.winfo_width() or 400
        H = canvas.winfo_height() or 200

        summary = self.model.monthly_summary()
        if not summary:
            canvas.create_text(
                W // 2,
                H // 2,
                text=tr(self.view.lang, "no_data"),
                fill=COLORS["text_dim"],
                font=FONTS["body"],
            )
            return

        months = list(summary.keys())[-6:]
        max_val = (
            max(
                max(summary[m]["income"], summary[m]["expense"]) for m in months
            )
            or 1
        )

        bar_w = max(8, (W - 60) // (len(months) * 2 + 1))
        gap = bar_w // 2
        x0 = 40

        for i, month in enumerate(months):
            inc = summary[month]["income"]
            exp = summary[month]["expense"]
            x = x0 + i * (bar_w * 2 + gap * 2)

            bh = int((inc / max_val) * (H - 50))
            canvas.create_rectangle(
                x,
                H - 30 - bh,
                x + bar_w,
                H - 30,
                fill=COLORS["income"],
                outline="",
            )
            bh2 = int((exp / max_val) * (H - 50))
            canvas.create_rectangle(
                x + bar_w + 2,
                H - 30 - bh2,
                x + bar_w * 2 + 2,
                H - 30,
                fill=COLORS["expense"],
                outline="",
            )
            canvas.create_text(
                x + bar_w,
                H - 12,
                text=month[5:],
                fill=COLORS["text_dim"],
                font=FONTS["small"],
                anchor="center",
            )

        canvas.create_line(35, 10, 35, H - 30, fill=COLORS["border"])
        canvas.create_line(35, H - 30, W - 5, H - 30, fill=COLORS["border"])

    def _draw_pie(self, canvas, data: dict):
        # Малювання кругової діаграми і підписи збоку
        canvas.delete("all")
        canvas.update_idletasks()
        W = canvas.winfo_width() or 300
        H = canvas.winfo_height() or 250

        if not data:
            canvas.create_text(
                W // 2,
                H // 2,
                text=tr(self.view.lang, "no_data"),
                fill=COLORS["text_dim"],
                font=FONTS["body"],
            )
            return

        total = sum(data.values())
        palette = [
            "#7C6AF7",
            "#50FA7B",
            "#FF6B6B",
            "#8BE9FD",
            "#FFB86C",
            "#FF79C6",
            "#BD93F9",
            "#F1FA8C",
        ]
        cx, cy, r = W // 3, H // 2, min(W // 3, H // 2) - 10

        # сектори
        start = 0.0
        items = list(data.items())
        for idx, (cat, val) in enumerate(items):
            extent = 360 * val / total
            canvas.create_arc(
                cx - r,
                cy - r,
                cx + r,
                cy + r,
                start=start,
                extent=extent,
                fill=palette[idx % len(palette)],
                outline=COLORS["bg"],
                width=2,
            )
            start += extent

        lang = self.view.lang
        lx, ly = cx + r + 16, 20
        for idx, (cat, val) in enumerate(items):
            canvas.create_rectangle(
                lx,
                ly,
                lx + 12,
                ly + 12,
                fill=palette[idx % len(palette)],
                outline="",
            )
            pct = val / total * 100
            canvas.create_text(
                lx + 16,
                ly + 6,
                text=f"{tr_cat(cat, lang)}: {val:,.0f} ({pct:.0f}%)",
                fill=COLORS["text"],
                font=FONTS["small"],
                anchor="w",
            )
            ly += 20

    def _categories(self):
        return CATEGORIES["ua"] if self.view.lang == "ua" else CATEGORIES["en"]

    def on_add(self):
        # Відкривання діалогово вікна для створення нової транзакції
        dlg = TransactionDialog(
            self.view,
            self.view.lang,
            self._categories(),
            title=tr(self.view.lang, "dlg_add_title"),
        )
        self.view.wait_window(dlg)
        if dlg.result:
            result = dict(dlg.result)
            result["type_"] = result.pop("type")
            self.model.add_transaction(**result)
            self.refresh()

    def on_edit(self):
        # Бере виділений рядок, підтягує його дані з моделі і кидає у вікно редагування
        sel = self.view.tree.selection()
        if not sel:
            messagebox.showwarning("", tr(self.view.lang, "err_select"))
            return
        tid = int(sel[0])
        t = self.model.get_by_id(tid)
        if not t:
            return
        init = {
            "type": t.type,
            "amount": t.amount,
            "category": t.category,
            "description": t.description,
            "date": t.date,
            "currency": t.currency,
        }
        dlg = TransactionDialog(
            self.view,
            self.view.lang,
            self._categories(),
            title=tr(self.view.lang, "dlg_edit_title"),
            initial=init,
        )
        self.view.wait_window(dlg)
        if dlg.result:
            result = dict(dlg.result)
            result["type_"] = result.pop("type")
            self.model.update_transaction(tid, **result)
            self.refresh()

    def on_delete(self):
        # Видалення виділеного рядка
        sel = self.view.tree.selection()
        if not sel:
            messagebox.showwarning("", tr(self.view.lang, "err_select"))
            return
        if messagebox.askyesno("", tr(self.view.lang, "ask_delete")):
            self.model.delete_transaction(int(sel[0]))
            self.refresh()

    def on_export_csv(self):
        #  Метод для експорту файла з транзакціями
        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title=tr(self.view.lang, "menu_export"),
        )
        if path:
            self.model.export_csv(path)
            messagebox.showinfo("", tr(self.view.lang, "msg_saved") + path)

    def on_change_file(self):
        #  Метод для імпорту файла з транзакціями
        path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title=tr(self.view.lang, "menu_import"),
            initialfile=self.model.data_path,
        )
        if path:
            self.model.data_path = path
            self.model.load()
            self.refresh()

    def on_toggle_lang(self):
        # Перемикач мови UA <-> EN
        v = self.view
        v.lang = "en" if v.lang == "ua" else "ua"
        self._rebuild_ui()

    def _rebuild_ui(self):
        # Ререписування всіх текстових міток, коли користувач міняє мову
        v = self.view
        lang = v.lang

        v.title(tr(lang, "app_title"))

        v.menu_bar.delete(0, "end")
        # меню при кліку
        v._file_menu.entryconfigure(0, label=tr(lang, "menu_export"))
        v._file_menu.entryconfigure(1, label=tr(lang, "menu_import"))
        v._file_menu.entryconfigure(3, label=tr(lang, "menu_exit"))
        v._help_menu.entryconfigure(0, label=tr(lang, "menu_about"))
        # меню поверхневе
        v.menu_bar.add_cascade(label=tr(lang, "menu_file"), menu=v._file_menu)
        v.menu_bar.add_cascade(label=tr(lang, "menu_help"), menu=v._help_menu)
        # Контекстне меню
        v.context_menu.entryconfigure(0, label=tr(lang, "btn_edit"))
        v.context_menu.entryconfigure(1, label=tr(lang, "btn_delete"))
        # Вкладки
        v.notebook.tab(0, text=tr(lang, "tab_dash"))
        v.notebook.tab(1, text=tr(lang, "tab_trans"))
        v.notebook.tab(2, text=tr(lang, "tab_stats"))
        # Картки дашборду
        v.card_income._title_label.config(text=tr(lang, "lbl_income"))
        v.card_expense._title_label.config(text=tr(lang, "lbl_expense"))
        v.card_balance._title_label.config(text=tr(lang, "lbl_balance"))
        v.monthly_title_label.config(text=tr(lang, "monthly"))
        v.recent_title_label.config(text=tr(lang, "lbl_recent"))
        # Кнопки
        v.btn_add.config(text=tr(lang, "btn_add"))
        v.btn_edit.config(text=tr(lang, "btn_edit"))
        v.btn_delete.config(text=tr(lang, "btn_delete"))
        v.btn_export.config(text=tr(lang, "btn_export"))
        v.btn_lang.config(text=v.lang.upper())
        # Для фільтрів, сортувань та пошуку транзакцій
        v.lbl_filter_type.config(text=tr(lang, "filter_type"))
        v.lbl_filter_cat.config(text=tr(lang, "filter_cat"))
        v.lbl_sort.config(text=tr(lang, "sort_by"))
        v.lbl_search.config(text=tr(lang, "filter_search"))
        # заголовки стовпців загальної таблиці
        for col, key in [
            ("date", "col_date"),
            ("type", "col_type"),
            ("category", "col_category"),
            ("description", "col_desc"),
            ("amount", "col_amount"),
            ("currency", "fld_currency"),
        ]:
            v.tree.heading(col, text=tr(lang, key))
        # Заголовки для таблиуці про 5 останнії трнзакцій
        v.recent_tree.heading("date", text=tr(lang, "col_date"))
        v.recent_tree.heading("desc", text=tr(lang, "col_desc"))
        v.recent_tree.heading("amount", text=tr(lang, "col_amount"))
        v.recent_tree.heading("currency", text=tr(lang, "fld_currency"))
        # решта підписів
        v.progress_label.config(text=tr(lang, "progress_lbl"))
        v.lbl_multicurrency.config(text=tr(lang, "note_multicurrency"))
        v.stat_exp_title.config(text=tr(lang, "by_category"))
        v.stat_inc_title.config(text=tr(lang, "stat_income_cat"))
        v.lbl_drag_hint.config(text=tr(lang, "drag_hint"))

        self._update_filter_options()
        self.refresh()

    def _update_category_filter(self):
        # Динамічне вибирання категорій в залежності від виду транзакції
        v = self.view
        lang = v.lang
        all_lbl = tr(lang, "filter_all")
        cats = CATEGORIES["ua"] if lang == "ua" else CATEGORIES["en"]

        type_val = v.filter_type_var.get()

        if type_val == tr(lang, "income_lbl"):
            options = cats["income"]
        elif type_val == tr(lang, "expense_lbl"):
            options = cats["expense"]
        else:
            options = cats["income"] + cats["expense"]

        v.filter_cat_cb["values"] = [all_lbl] + options
        v.filter_cat_var.set(all_lbl)

    def _update_filter_options(self):
        # Заповнювання випадаючих списків (фільтри і сортування) при старті або при зміні мови.
        v = self.view
        lang = v.lang
        all_lbl = tr(lang, "filter_all")

        type_opts = [all_lbl, tr(lang, "income_lbl"), tr(lang, "expense_lbl")]
        v.filter_type_cb["values"] = type_opts
        v.filter_type_var.set(all_lbl)

        self._update_category_filter()  

        sort_opts = [
            tr(lang, "sort_date"),
            tr(lang, "sort_amount"),
            tr(lang, "sort_category"),
            tr(lang, "sort_manual"),
        ]
        v.sort_cb["values"] = sort_opts
        v.sort_var.set(sort_opts[0])

    def run(self):
        #  Запускання додатку
        self.view.mainloop()
