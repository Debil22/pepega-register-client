"""
Клиент регистрации на IRC pepega.top.
Обращается к https://api.pepega.top:8443/register и получает конфиг Halloy.

Зависимости:
    pip install customtkinter httpx
"""

import httpx
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog, messagebox

API_URL = "https://api.pepega.top:8443/register"
REQUEST_TIMEOUT = 60

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

BG_COLOR = "#1a1a1a"
FG_COLOR = "#242424"
ACCENT = "#1f6aa5"
ACCENT_HOVER = "#155a8a"
OK_COLOR = "#88ff88"
WARN_COLOR = "#ffff88"
ERR_COLOR = "#ff6666"


class RegisterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Регистрация IRC · pepega.top")
        self.geometry("460x500")
        self.resizable(False, False)
        self.configure(fg_color=BG_COLOR)

        self._last_config: str = ""
        self._busy = False

        self._build_ui()

    def _build_ui(self) -> None:
        ctk.CTkLabel(
            self, text="Регистрация на irc.pepega.top",
            font=("Arial", 20, "bold"), text_color="#ffffff",
        ).pack(pady=(28, 4))

        ctk.CTkLabel(
            self, text="Создаст аккаунт и вернёт конфиг для Halloy.",
            font=("Arial", 12), text_color="#999999",
        ).pack(pady=(0, 20))

        ctk.CTkLabel(
            self, text="Введите логин",
            font=("Arial", 13), text_color="#dddddd", anchor="w",
        ).pack(fill="x", padx=60)
        self.login_entry = ctk.CTkEntry(
            self, width=340, height=38, font=("Arial", 13),
            fg_color=FG_COLOR, border_color="#333333",
        )
        self.login_entry.pack(pady=(4, 14))

        ctk.CTkLabel(
            self, text="Введите пароль",
            font=("Arial", 13), text_color="#dddddd", anchor="w",
        ).pack(fill="x", padx=60)
        self.password_entry = ctk.CTkEntry(
            self, width=340, height=38, font=("Arial", 13), show="•",
            fg_color=FG_COLOR, border_color="#333333",
        )
        self.password_entry.pack(pady=(4, 8))

        self.show_pass_var = tk.BooleanVar(value=False)
        ctk.CTkCheckBox(
            self, text="Показать пароль", variable=self.show_pass_var,
            command=self._toggle_password, font=("Arial", 12),
            text_color="#aaaaaa", fg_color=ACCENT, hover_color=ACCENT_HOVER,
            border_color="#444444",
        ).pack(anchor="w", padx=60, pady=(0, 16))

        self.register_btn = ctk.CTkButton(
            self, text="Регистрация", command=self.on_register,
            width=340, height=44, font=("Arial", 14, "bold"),
            fg_color=ACCENT, hover_color=ACCENT_HOVER,
        )
        self.register_btn.pack(pady=(4, 14))

        self.status_label = ctk.CTkLabel(
            self, text="", font=("Arial", 12), text_color=OK_COLOR,
            wraplength=380, justify="center",
        )
        self.status_label.pack(pady=(0, 10))

        self.copy_btn = ctk.CTkButton(
            self, text="Скопировать конфиг в буфер", command=self.copy_config,
            width=340, height=36, font=("Arial", 12),
            fg_color="#3a3a3a", hover_color="#4a4a4a", state="disabled",
        )
        self.copy_btn.pack(pady=(0, 8))

        self.save_btn = ctk.CTkButton(
            self, text="Сохранить как файл…", command=self.save_config,
            width=340, height=36, font=("Arial", 12),
            fg_color="#3a3a3a", hover_color="#4a4a4a", state="disabled",
        )
        self.save_btn.pack(pady=(0, 20))

        self.login_entry.bind("<Return>", lambda e: self.on_register())
        self.password_entry.bind("<Return>", lambda e: self.on_register())

    def _toggle_password(self) -> None:
        self.password_entry.configure(show="" if self.show_pass_var.get() else "•")

    def _set_status(self, text: str, color: str = OK_COLOR) -> None:
        self.status_label.configure(text=text, text_color=color)
        self.update_idletasks()

    def _set_busy(self, busy: bool) -> None:
        self._busy = busy
        state = "disabled" if busy else "normal"
        self.register_btn.configure(state=state)
        self.login_entry.configure(state=state)
        self.password_entry.configure(state=state)

    def on_register(self) -> None:
        if self._busy:
            return

        login = self.login_entry.get().strip()
        password = self.password_entry.get().strip()

        if not login or not password:
            self._set_status("Заполните логин и пароль", ERR_COLOR)
            return
        if len(login) < 2 or len(login) > 32:
            self._set_status("Логин должен быть от 2 до 32 символов", ERR_COLOR)
            return
        if len(password) < 6:
            self._set_status("Пароль должен быть минимум 6 символов", ERR_COLOR)
            return

        self._set_busy(True)
        self.copy_btn.configure(state="disabled")
        self.save_btn.configure(state="disabled")
        self._set_status("Отправка запроса на сервер…", WARN_COLOR)

        try:
            with httpx.Client(timeout=REQUEST_TIMEOUT) as client:
                r = client.post(API_URL, json={"login": login, "password": password})

            if r.status_code == 200:
                data = r.json()
                self._last_config = data["config"]
                self.copy_btn.configure(state="normal")
                self.save_btn.configure(state="normal")
                self._set_status(
                    f"Готово! Аккаунт «{login}» создан.\n"
                    f"Скопируйте конфиг и вставьте в Halloy.",
                    OK_COLOR,
                )
            elif r.status_code == 429:
                self._set_status("Слишком много попыток. Попробуйте через час.", ERR_COLOR)
            elif r.status_code == 400:
                detail = r.json().get("detail", r.text)
                self._set_status(f"Проверьте данные: {detail}", ERR_COLOR)
            elif r.status_code == 500:
                detail = r.json().get("detail", r.text)
                self._set_status(f"Ошибка сервера: {detail}", ERR_COLOR)
            else:
                try:
                    detail = r.json().get("detail", r.text)
                except Exception:
                    detail = r.text
                self._set_status(f"Ошибка {r.status_code}: {detail}", ERR_COLOR)

        except httpx.ConnectError:
            self._set_status("Не удалось подключиться к api.pepega.top:8443", ERR_COLOR)
        except httpx.TimeoutException:
            self._set_status("Сервер не ответил вовремя", ERR_COLOR)
        except Exception as e:
            self._set_status(f"Ошибка: {e}", ERR_COLOR)
        finally:
            self._set_busy(False)

    def copy_config(self) -> None:
        if not self._last_config:
            return
        self.clipboard_clear()
        self.clipboard_append(self._last_config)
        self.update()
        self._set_status("Конфиг скопирован в буфер обмена", OK_COLOR)

    def save_config(self) -> None:
        if not self._last_config:
            return
        login = self.login_entry.get().strip() or "user"
        path = filedialog.asksaveasfilename(
            defaultextension=".toml",
            initialfile=f"halloy_{login}.toml",
            filetypes=[("TOML файлы", "*.toml"), ("Все файлы", "*.*")],
        )
        if not path:
            return
        with open(path, "w", encoding="utf-8") as f:
            f.write(self._last_config)
        self._set_status(f"Сохранено: {path}", OK_COLOR)


def main() -> None:
    app = RegisterApp()
    app.mainloop()


if __name__ == "__main__":
    main()