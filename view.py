"""
view.py — View шар (MVC)
Відповідає за відображення GUI. Не містить бізнес-логіки.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, datetime
from config import tr, COLORS, FONTS


class StyledButton(tk.Button):
    # Кастомна кнопка.
    def __init__(self, parent, text="", color=None, **kwargs):
        c = color or COLORS["accent"]
        super().__init__(
            parent,
            text=text,
            bg=c,
            fg=COLORS["text"],
            activebackground=COLORS["hover"],
            activeforeground=COLORS["text"],
            font=FONTS["body"],
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=6,
            **kwargs,
        )
        self.bind("<Enter>", lambda e: self.config(bg=COLORS["hover"]))
        self.bind("<Leave>", lambda e: self.config(bg=c))

class CardFrame(tk.Frame):
    # Стилізована панель з відступами для дашборду.
    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            bg=COLORS["surface"],
            relief="flat",
            padx=16,
            pady=12,
            **kwargs,
        )

class MainView(tk.Tk):
    # Головне вікно програми.
    def __init__(self):
        super().__init__()
        self.lang = "ua"
        self._setup_window()
        self._apply_ttk_style()
        self._build_menu()
        self._build_notebook()
        self._build_dashboard_tab()
        self._build_transactions_tab()
        self._build_stats_tab()

    def _setup_window(self):
        # Створення головного вікна
        self.title(tr(self.lang, "app_title"))
        w, h = 1100, 700
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")
        self.minsize(900, 600)
        self.configure(bg=COLORS["bg"])

    def _apply_ttk_style(self, bar_color=None):
        # Налаштування стилю
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure("TNotebook", background=COLORS["bg"], borderwidth=0)
        style.configure(
            "TNotebook.Tab",
            background=COLORS["surface"],
            foreground=COLORS["text_dim"],
            font=FONTS["body"],
            padding=[16, 8],
        )
        style.map(
            "TNotebook.Tab",
            background=[("selected", COLORS["accent"])],
            foreground=[("selected", COLORS["text"])],
        )

        style.configure(
            "Treeview",
            background=COLORS["surface"],
            fieldbackground=COLORS["surface"],
            foreground=COLORS["text"],
            rowheight=28,
            font=FONTS["body"],
            borderwidth=0,
        )
        style.configure(
            "Treeview.Heading",
            background=COLORS["surface2"],
            foreground=COLORS["text"],
            font=FONTS["heading"],
            relief="flat",
        )
        style.map(
            "Treeview",
            background=[("selected", COLORS["accent"])],
            foreground=[("selected", COLORS["text"])],
        )

        style.configure(
            "TCombobox",
            fieldbackground=COLORS["surface2"],
            background=COLORS["surface2"],
            foreground=COLORS["text"],
            selectbackground=COLORS["accent"],
            selectforeground=COLORS["text"],
        )
        style.map(
            "TCombobox",
            fieldbackground=[("readonly", COLORS["surface2"])],
            selectbackground=[("readonly", COLORS["accent"])],
        )

        style.configure(
            "TScrollbar",
            background=COLORS["surface2"],
            troughcolor=COLORS["bg"],
            arrowcolor=COLORS["text_dim"],
        )

        style.configure(
            "TProgressbar",
            background=bar_color if bar_color else COLORS["expense"],
            troughcolor=COLORS["surface2"],
            thickness=16,
        )

    def _build_menu(self):
        #  Створення меню
        self.menu_bar = tk.Menu(
            self,
            bg=COLORS["surface"],
            fg=COLORS["text"],
            activebackground=COLORS["accent"],
            activeforeground=COLORS["text"],
            relief="flat",
        )
        self.config(menu=self.menu_bar)

        self._file_menu = tk.Menu(
            self.menu_bar,
            tearoff=0,
            bg=COLORS["surface"],
            fg=COLORS["text"],
            activebackground=COLORS["accent"],
            activeforeground=COLORS["text"],
        )
        self.menu_bar.add_cascade(
            label=tr(self.lang, "menu_file"), menu=self._file_menu
        )

        self._file_menu.add_command(
            label=tr(self.lang, "menu_export"),
            command=self._on_export_csv,
        )
        self._file_menu.add_command(
            label=tr(self.lang, "menu_import"),
            command=self._on_change_file,
        )
        self._file_menu.add_separator()
        self._file_menu.add_command(
            label=tr(self.lang, "menu_exit"),
            command=self.quit,
        )

        self._help_menu = tk.Menu(
            self.menu_bar,
            tearoff=0,
            bg=COLORS["surface"],
            fg=COLORS["text"],
            activebackground=COLORS["accent"],
            activeforeground=COLORS["text"],
        )
        self.menu_bar.add_cascade(
            label=tr(self.lang, "menu_help"), menu=self._help_menu
        )

        self._help_menu.add_command(
            label=tr(self.lang, "menu_about"), command=self._on_about
        )

    def _build_notebook(self):
        # Створення вкладки
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=5)

        self.btn_lang = StyledButton(
            self, text="UA/EN", color=COLORS["surface2"], width=4
        )

        self.btn_lang.place(relx=1.0, x=-25, y=0, anchor="ne")

    # Вкладка №1: дашборд

    def _build_dashboard_tab(self):
        self.dash_frame = tk.Frame(self.notebook, bg=COLORS["bg"])
        self.notebook.add(self.dash_frame, text=tr(self.lang, "tab_dash"))

        cards_row = tk.Frame(self.dash_frame, bg=COLORS["bg"])
        cards_row.pack(fill="x", padx=20, pady=(20, 10))

        self.card_income = self._make_summary_card(
            cards_row, tr(self.lang, "lbl_income"), "0.00", COLORS["income"]
        )
        self.card_expense = self._make_summary_card(
            cards_row, tr(self.lang, "lbl_expense"), "0.00", COLORS["expense"]
        )
        self.card_balance = self._make_summary_card(
            cards_row, tr(self.lang, "lbl_balance"), "0.00", COLORS["neutral"]
        )

        for card in (self.card_income, self.card_expense, self.card_balance):
            card.pack(side="left", expand=True, fill="x", padx=8)

        self.lbl_multicurrency = tk.Label(
            self.dash_frame,
            text=tr(self.lang, "note_multicurrency"),
            bg=COLORS["bg"],
            fg=COLORS["text_dim"],
            font=FONTS["small"],
        )
        self.lbl_multicurrency.pack(anchor="e", padx=28)

        prog_frame = CardFrame(self.dash_frame)
        prog_frame.pack(fill="x", padx=28, pady=(0, 10))

        self.progress_label = tk.Label(
            prog_frame,
            text=tr(self.lang, "progress_lbl"),
            bg=COLORS["surface"],
            fg=COLORS["text_dim"],
            font=FONTS["small"],
        )
        self.progress_label.pack(anchor="w")

        self.progress_var = tk.DoubleVar(value=0)
        self.progress_bar = ttk.Progressbar(
            prog_frame,
            variable=self.progress_var,
            maximum=100,
            length=400,
            style="TProgressbar",
        )
        self.progress_bar.pack(fill="x", pady=(4, 0))
        self.progress_pct_lbl = tk.Label(
            prog_frame,
            text="0%",
            bg=COLORS["surface"],
            fg=COLORS["text"],
            font=FONTS["small"],
        )
        self.progress_pct_lbl.pack(anchor="e")

        bottom = tk.Frame(self.dash_frame, bg=COLORS["bg"])
        bottom.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        chart_card = CardFrame(bottom)
        chart_card.pack(side="left", fill="both", expand=True, padx=(0, 8))
        self.monthly_title_label = tk.Label(
            chart_card,
            text=tr(self.lang, "monthly"),
            bg=COLORS["surface"],
            fg=COLORS["text"],
            font=FONTS["heading"],
        )
        self.monthly_title_label.pack(anchor="w", pady=(0, 8))
        self.monthly_canvas = tk.Canvas(
            chart_card, bg=COLORS["surface"], highlightthickness=0, height=200
        )
        self.monthly_canvas.pack(fill="both", expand=True)

        recent_card = CardFrame(bottom)
        recent_card.pack(side="right", fill="both", expand=True, padx=(8, 0))
        self.recent_title_label = tk.Label(
            recent_card,
            text=tr(self.lang, "lbl_recent"),
            bg=COLORS["surface"],
            fg=COLORS["text"],
            font=FONTS["heading"],
        )
        self.recent_title_label.pack(anchor="w", pady=(0, 8))

        cols = ("date", "desc", "amount", "currency")
        self.recent_tree = ttk.Treeview(
            recent_card,
            columns=cols,
            show="headings",
            height=7,
            selectmode="browse",
        )
        col_labels_recent = {
            "date": tr(self.lang, "col_date"),
            "desc": tr(self.lang, "col_desc"),
            "amount": tr(self.lang, "col_amount"),
            "currency": tr(self.lang, "fld_currency"),
        }
        for c, w in zip(cols, (90, 140, 90, 70)):
            self.recent_tree.heading(c, text=col_labels_recent[c])
            self.recent_tree.column(c, width=w, anchor="center")
        self.recent_tree.pack(fill="both", expand=True)

    def _make_summary_card(
        self, parent, label_text: str, value: str, color: str
    ):
        card = CardFrame(parent)
        lbl = tk.Label(
            card,
            text=label_text,
            bg=COLORS["surface"],
            fg=COLORS["text_dim"],
            font=FONTS["small"],
        )
        lbl.pack(anchor="w")
        card._title_label = lbl
        val_label = tk.Label(
            card, text=value, bg=COLORS["surface"], fg=color, font=FONTS["big"]
        )
        val_label.pack(anchor="w")
        val_label._color = color
        card._val_label = val_label
        return card

    # Вкладка №2: транзакції

    def _build_transactions_tab(self):
        self.trans_frame = tk.Frame(self.notebook, bg=COLORS["bg"])
        self.notebook.add(self.trans_frame, text=tr(self.lang, "tab_trans"))

        toolbar = tk.Frame(self.trans_frame, bg=COLORS["bg"])
        toolbar.pack(fill="x", padx=16, pady=(12, 0))

        self.btn_add = StyledButton(
            toolbar, text=tr(self.lang, "btn_add"), color=COLORS["income"]
        )
        self.btn_edit = StyledButton(
            toolbar, text=tr(self.lang, "btn_edit"), color=COLORS["accent"]
        )
        self.btn_delete = StyledButton(
            toolbar, text=tr(self.lang, "btn_delete"), color=COLORS["expense"]
        )
        self.btn_export = StyledButton(
            toolbar, text=tr(self.lang, "btn_export"), color=COLORS["surface2"]
        )

        for b in (
            self.btn_add,
            self.btn_edit,
            self.btn_delete,
            self.btn_export,
        ):
            b.pack(side="left", padx=4)

        filter_frame = tk.Frame(self.trans_frame, bg=COLORS["bg"])
        filter_frame.pack(fill="x", padx=16, pady=8)

        self.lbl_filter_type = tk.Label(
            filter_frame,
            text=tr(self.lang, "filter_type"),
            bg=COLORS["bg"],
            fg=COLORS["text_dim"],
            font=FONTS["small"],
        )
        self.lbl_filter_type.pack(side="left")
        self.filter_type_var = tk.StringVar(value=tr(self.lang, "filter_all"))
        self.filter_type_cb = ttk.Combobox(
            filter_frame,
            textvariable=self.filter_type_var,
            state="readonly",
            width=12,
        )
        self.filter_type_cb.pack(side="left", padx=(4, 16))

        self.lbl_filter_cat = tk.Label(
            filter_frame,
            text=tr(self.lang, "filter_cat"),
            bg=COLORS["bg"],
            fg=COLORS["text_dim"],
            font=FONTS["small"],
        )
        self.lbl_filter_cat.pack(side="left")
        self.filter_cat_var = tk.StringVar(value=tr(self.lang, "filter_all"))
        self.filter_cat_cb = ttk.Combobox(
            filter_frame,
            textvariable=self.filter_cat_var,
            state="readonly",
            width=14,
        )
        self.filter_cat_cb.pack(side="left", padx=(4, 16))

        self.lbl_sort = tk.Label(
            filter_frame,
            text=tr(self.lang, "sort_by"),
            bg=COLORS["bg"],
            fg=COLORS["text_dim"],
            font=FONTS["small"],
        )
        self.lbl_sort.pack(side="left")
        self.sort_var = tk.StringVar(value=tr(self.lang, "sort_date"))
        self.sort_cb = ttk.Combobox(
            filter_frame, textvariable=self.sort_var, state="readonly", width=10
        )
        self.sort_cb.pack(side="left", padx=(4, 16))

        self.lbl_search = tk.Label(
            filter_frame,
            text=tr(self.lang, "filter_search"),
            bg=COLORS["bg"],
            fg=COLORS["text_dim"],
            font=FONTS["small"],
        )
        self.lbl_search.pack(side="left")
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(
            filter_frame,
            textvariable=self.search_var,
            bg=COLORS["surface2"],
            fg=COLORS["text"],
            insertbackground=COLORS["text"],
            relief="flat",
            font=FONTS["body"],
            width=20,
        )
        search_entry.pack(side="left", padx=4, ipady=4)

        tree_frame = tk.Frame(self.trans_frame, bg=COLORS["bg"])
        tree_frame.pack(fill="both", expand=True, padx=16, pady=(4, 12))

        cols = (
            "id",
            "date",
            "type",
            "category",
            "description",
            "amount",
            "currency",
        )
        self.tree = ttk.Treeview(
            tree_frame,
            columns=cols,
            show="headings",
            selectmode="browse",
            displaycolumns=(
                "date",
                "type",
                "category",
                "description",
                "amount",
                "currency",
            ),
        )

        widths = {
            "id": 40,
            "date": 100,
            "type": 90,
            "category": 120,
            "description": 220,
            "amount": 100,
            "currency": 70,
        }
        anchors = {
            "id": "center",
            "date": "center",
            "type": "center",
            "category": "center",
            "description": "center",
            "amount": "center",
            "currency": "center",
        }
        col_labels = {
            "id": "ID",
            "date": tr(self.lang, "col_date"),
            "type": tr(self.lang, "col_type"),
            "category": tr(self.lang, "col_category"),
            "description": tr(self.lang, "col_desc"),
            "amount": tr(self.lang, "col_amount"),
            "currency": tr(self.lang, "fld_currency"),
        }
        for c in cols:
            self.tree.heading(c, text=col_labels[c])
            self.tree.column(c, width=widths[c], anchor=anchors[c])

        self.tree.tag_configure("income", foreground=COLORS["income"])
        self.tree.tag_configure("expense", foreground=COLORS["expense"])
        self.tree.tag_configure("odd", background=COLORS["surface"])
        self.tree.tag_configure("even", background=COLORS["surface2"])

        vsb = ttk.Scrollbar(
            tree_frame, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        self.context_menu = tk.Menu(
            self.tree,
            tearoff=0,
            bg=COLORS["surface"],
            fg=COLORS["text"],
            activebackground=COLORS["accent"],
            activeforeground=COLORS["text"],
        )
        self.context_menu.add_command(label=tr(self.lang, "btn_edit"))
        self.context_menu.add_command(label=tr(self.lang, "btn_delete"))
        self.tree.bind("<Button-3>", self._show_context_menu)

        self._drag_data = {"item": None, "y": 0, "moved": False}
        self.tree.bind("<ButtonPress-1>", self._drag_start)
        self.tree.bind("<B1-Motion>", self._drag_motion)
        self.tree.bind("<ButtonRelease-1>", self._drag_stop)
        self._drag_callback = None

        self.lbl_drag_hint = tk.Label(
            self.trans_frame,
            text=tr(self.lang, "drag_hint"),
            bg=COLORS["bg"],
            fg=COLORS["text_dim"],
            font=FONTS["small"],
        )
        self.lbl_drag_hint.pack(pady=(0, 4))

    # Вкладка №3: статистика

    def _build_stats_tab(self):
        self.stats_frame = tk.Frame(self.notebook, bg=COLORS["bg"])
        self.notebook.add(self.stats_frame, text=tr(self.lang, "tab_stats"))

        top = tk.Frame(self.stats_frame, bg=COLORS["bg"])
        top.pack(fill="both", expand=True, padx=20, pady=10)

        exp_card = CardFrame(top)
        exp_card.pack(side="left", fill="both", expand=True, padx=(0, 8))
        self.stat_exp_title = tk.Label(
            exp_card,
            text=tr(self.lang, "by_category"),
            bg=COLORS["surface"],
            fg=COLORS["text"],
            font=FONTS["heading"],
        )
        self.stat_exp_title.pack(anchor="w", pady=(0, 8))
        self.stat_exp_canvas = tk.Canvas(
            exp_card, bg=COLORS["surface"], highlightthickness=0, height=250
        )
        self.stat_exp_canvas.pack(fill="both", expand=True)

        inc_card = CardFrame(top)
        inc_card.pack(side="right", fill="both", expand=True, padx=(8, 0))
        self.stat_inc_title = tk.Label(
            inc_card,
            text=tr(self.lang, "stat_income_cat"),
            bg=COLORS["surface"],
            fg=COLORS["text"],
            font=FONTS["heading"],
        )
        self.stat_inc_title.pack(anchor="w", pady=(0, 8))
        self.stat_inc_canvas = tk.Canvas(
            inc_card, bg=COLORS["surface"], highlightthickness=0, height=250
        )
        self.stat_inc_canvas.pack(fill="both", expand=True)

    def _show_context_menu(self, event):
        # Виклик контекстного меню правою кнопкою миші
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)

    # Drag & Drop
    def _drag_start(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self._drag_data["item"] = item
            self._drag_data["y"] = event.y
            self._drag_data["moved"] = False

    def _drag_motion(self, event):
        if not self._drag_data["item"]:
            return
        if abs(event.y - self._drag_data["y"]) < 5:
            return
        target = self.tree.identify_row(event.y)
        if target and target != self._drag_data["item"]:
            self.tree.move(self._drag_data["item"], "", self.tree.index(target))
            self._drag_data["moved"] = True

    def _drag_stop(self, event):
        if (
            self._drag_data["item"]
            and self._drag_data.get("moved")
            and self._drag_callback
        ):
            new_order = [int(iid) for iid in self.tree.get_children()]
            self._drag_callback(new_order)

        self._drag_data["item"] = None
        self._drag_data["moved"] = False

    def _on_export_csv(self):
        raise NotImplementedError("_on_export_csv must be set by Controller")

    def _on_change_file(self):
        raise NotImplementedError("_on_change_file must be set by Controller")

    def _on_toggle_lang(self):
        raise NotImplementedError("_on_toggle_lang must be set by Controller")

    def _on_about(self):
        messagebox.showinfo("About", tr(self.lang, "about_text"))


class TransactionDialog(tk.Toplevel):
    # Діалогове вікно для додавання/редагування транзакцій.
    CURRENCIES = ["UAH", "USD", "EUR", "GBP", "PLN"]

    def __init__(
        self,
        parent,
        lang: str,
        categories: dict,
        title: str = "",
        initial: dict = None,
    ):
        super().__init__(parent)
        self.lang = lang
        self.categories = categories
        self.result = None

        self.title(title or tr(lang, "dlg_add_title"))
        self.resizable(True, True)
        self.minsize(440, 530)
        self.configure(bg=COLORS["bg"])
        self.grab_set()

        self._build(initial or {})

        self.update_idletasks()
        w = max(self.winfo_reqwidth(), 440)
        h = max(self.winfo_reqheight() + 30, 530)
        pw = parent.winfo_rootx() + parent.winfo_width() // 2
        ph = parent.winfo_rooty() + parent.winfo_height() // 2
        self.geometry(f"{w}x{h}+{pw - w//2}+{ph - h//2}")

    def _build(self, init: dict):
        # Розробка діалогового вікна для додавання/редагування транзакцій
        pad = {"padx": 20, "pady": 6}
        # Тип транзакції (дохід / витрата)
        tk.Label(
            self,
            text=tr(self.lang, "fld_type"),
            bg=COLORS["bg"],
            fg=COLORS["text"],
            font=FONTS["body"],
        ).pack(anchor="w", **pad)
        self.type_var = tk.StringVar(value=init.get("type", "expense"))
        type_frame = tk.Frame(self, bg=COLORS["bg"])
        type_frame.pack(fill="x", **pad)
        for val, lbl_key, color in [
            ("income", "income_lbl", COLORS["income"]),
            ("expense", "expense_lbl", COLORS["expense"]),
        ]:
            rb = tk.Radiobutton(
                type_frame,
                text=tr(self.lang, lbl_key),
                variable=self.type_var,
                value=val,
                bg=COLORS["bg"],
                fg=color,
                selectcolor=COLORS["surface"],
                activebackground=COLORS["bg"],
                font=FONTS["body"],
                command=self._refresh_categories,
            )
            rb.pack(side="left", padx=(0, 16))
        # Сума
        tk.Label(
            self,
            text=tr(self.lang, "fld_amount"),
            bg=COLORS["bg"],
            fg=COLORS["text"],
            font=FONTS["body"],
        ).pack(anchor="w", **pad)
        self.amount_var = tk.StringVar(value=str(init.get("amount", "")))
        tk.Entry(
            self,
            textvariable=self.amount_var,
            bg=COLORS["surface2"],
            fg=COLORS["text"],
            insertbackground=COLORS["text"],
            relief="flat",
            font=FONTS["mono"],
            width=20,
        ).pack(anchor="w", **pad, ipady=4)
        # Категорія (динамічно залежить від типу)
        tk.Label(
            self,
            text=tr(self.lang, "fld_category"),
            bg=COLORS["bg"],
            fg=COLORS["text"],
            font=FONTS["body"],
        ).pack(anchor="w", **pad)
        self.cat_var = tk.StringVar(value=init.get("category", ""))
        self.cat_cb = ttk.Combobox(
            self, textvariable=self.cat_var, state="readonly", width=28
        )
        self.cat_cb.pack(anchor="w", **pad)
        self._refresh_categories()
        if init.get("category"):
            self.cat_var.set(init["category"])
        # Опис
        tk.Label(
            self,
            text=tr(self.lang, "fld_desc"),
            bg=COLORS["bg"],
            fg=COLORS["text"],
            font=FONTS["body"],
        ).pack(anchor="w", **pad)
        self.desc_var = tk.StringVar(value=init.get("description", ""))
        tk.Entry(
            self,
            textvariable=self.desc_var,
            bg=COLORS["surface2"],
            fg=COLORS["text"],
            insertbackground=COLORS["text"],
            relief="flat",
            font=FONTS["body"],
            width=36,
        ).pack(anchor="w", **pad, ipady=4)
        # Дата
        tk.Label(
            self,
            text=tr(self.lang, "fld_date"),
            bg=COLORS["bg"],
            fg=COLORS["text"],
            font=FONTS["body"],
        ).pack(anchor="w", **pad)
        self.date_var = tk.StringVar(
            value=init.get("date", date.today().isoformat())
        )
        tk.Entry(
            self,
            textvariable=self.date_var,
            bg=COLORS["surface2"],
            fg=COLORS["text"],
            insertbackground=COLORS["text"],
            relief="flat",
            font=FONTS["mono"],
            width=16,
        ).pack(anchor="w", **pad, ipady=4)
        # Валюта
        tk.Label(
            self,
            text=tr(self.lang, "fld_currency"),
            bg=COLORS["bg"],
            fg=COLORS["text"],
            font=FONTS["body"],
        ).pack(anchor="w", **pad)
        self.currency_var = tk.StringVar(value=init.get("currency", "UAH"))
        cur_cb = ttk.Combobox(
            self,
            textvariable=self.currency_var,
            values=self.CURRENCIES,
            state="readonly",
            width=10,
        )
        cur_cb.pack(anchor="w", **pad)
        # Кнопки Зберегти / Скасувати
        btn_frame = tk.Frame(self, bg=COLORS["bg"])
        btn_frame.pack(fill="x", padx=20, pady=(20, 24))
        StyledButton(
            btn_frame,
            text=tr(self.lang, "btn_save"),
            color=COLORS["accent"],
            command=self._on_save,
        ).pack(side="right", padx=4)
        StyledButton(
            btn_frame,
            text=tr(self.lang, "btn_cancel"),
            color=COLORS["surface2"],
            command=self.destroy,
        ).pack(side="right")

    def _refresh_categories(self):
        # Оновлення списку категорій у випадаючому вікні після обирання користувачем типу транзакції
        t = self.type_var.get()
        cats = self.categories.get(t, [])
        self.cat_cb["values"] = cats
        if cats and (not self.cat_var.get() or self.cat_var.get() not in cats):
            self.cat_var.set(cats[0])

    def _on_save(self):
        # Валідація чи користувач ввів правильні дані
        try:
            amount = float(self.amount_var.get().replace(",", "."))
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Error", tr(self.lang, "err_amount"), parent=self
            )
            return

        try:
            datetime.strptime(self.date_var.get(), "%Y-%m-%d")
        except ValueError:
            messagebox.showerror(
                "Error", tr(self.lang, "err_date"), parent=self
            )
            return

        self.result = {
            "type": self.type_var.get(),
            "amount": amount,
            "category": self.cat_var.get(),
            "description": self.desc_var.get().strip(),
            "date": self.date_var.get(),
            "currency": self.currency_var.get(),
        }
        self.destroy()
