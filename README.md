# pepega-register-client

Клиент для регистрации аккаунтов на IRC-сети **irc.pepega.top**.

---

## Что делает

1. Отправляет логин и пароль на `https://api.pepega.top:8443/register`.
2. Сервер создаёт пользователя, регистрирует аккаунт в Ergo и настраивает bouncer.
3. Клиент получает готовый TOML-конфиг для Halloy.
4. Конфиг можно скопировать в буфер обмена или сохранить в файл.

---

## Скачать

Готовые сборки лежат в разделе [**Releases**]:

| ОС      | Файл                  |
|---------|-----------------------|
| Windows | `pepega-register.exe` |
| Linux   | `pepega-register`     |

---

## Как использовать

### Windows

1. Скачай `pepega-register.exe` из последнего релиза.
2. Запусти двойным кликом. Если SmartScreen предупреждает — нажми
   **«Подробнее»** → **«Выполнить в любом случае»**.
3. Введи логин и пароль, нажми **«Регистрация»**.
4. Когда появится зелёное сообщение — нажми **«Сохранить как файл…»**.
5. Сохрани конфиг как `%APPDATA%\halloy\config.toml` (папку `halloy`
   в `%APPDATA%` нужно создать, если её нет).
6. Запусти Halloy — он подключится к сети автоматически.

### Linux

# Скачать бинарник из релиза
# Выдать ему права на запуск
chmod +x pepega-register
# И запустить
./pepega-register

После регистрации сохрани конфиг в `~/.config/halloy/config.toml`
(папку `halloy` создать, если её нет).

---

## Как выглядит конфиг

```toml
[servers.pepega]
nickname = "твой_логин"
server = "irc.pepega.top"
port = 6690
tls = true

[servers.pepega.sasl.plain]
username = "твой_логин"
password = "твой_пароль"
```

Этот файл — обычный конфиг Halloy. Если ты уже пользуешься Halloy
и у тебя есть другие сети — просто добавь секцию `[servers.pepega]`
к своему существующему конфигу.

---

## Требования

- Логин: от 2 до 32 символов, латиница, цифры, `_ - [ ] \ ^ { } | \``,
  начинается с буквы.
- Пароль: от 6 до 64 символов, без пробелов.
- Один IP может создать не больше 3 аккаунтов в час.

---

## Частые вопросы

**Программа не подключается к серверу.**
Проверь, что `api.pepega.top:8443` доступен из твоей сети. Иногда корпоративные
файрволы или провайдеры блокируют нестандартные порты.

**Я забыл пароль.**
Пароль нигде не хранится в открытом виде. Если потерял — обратись
к администратору сети для сброса.

**Halloy не подключается после сохранения конфига.**
Проверь путь: файл должен лежать ровно в `config.toml` в папке Halloy,
а не быть вложенным в подпапку. Формат — TOML, не JSON.

---

## Для разработчиков

### Сборка из исходников

```bash
git clone https://github.com/Debil22/pepega-register-client.git
cd pepega-register-client

python -m venv venv
source venv/bin/activate     # Linux
# venv\Scripts\activate.bat  # Windows

pip install -r requirements.txt
python client.py
```

### Сборка бинарников

```bash
pyinstaller --onefile --windowed --collect-data customtkinter \
    --name pepega-register client.py
```

Готовый файл — в `dist/`.

### Автоматические релизы

Workflow `.github/workflows/release.yml` собирает бинарники для Windows
и Linux при пуше тега вида `v*`:

```bash
git tag v1.0.1
git push origin v1.0.1
```

