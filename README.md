# Heatlink

### Структура файла с данными

```.env```
```
# Telegram Bot Token
BOT_TOKEN           = "1234567890:ABCdefGHIjklmNOPqrstUvwxYZ"

# MQTT Broker (на VPS)
MQTT_HOST           = "our_vps_ip_or_domain"
MQTT_PORT           = "1883"
MQTT_USER           = "your_mqtt_user"
MQTT_PASSWORD       = "your_mqtt_password"

# WiFi для ESP32
WIFI_SSID           = YourWiFiSSID
WIFI_PASSWORD       = YourWiFiPassword

# Дополнительно: идентификатор устройства
DEVICE_ID           = esp32_heater_01
```


### Структура проекта
```
├── .github/                      # папка для GitHub Actions (CI/CD)
│   └── workflows/
│       ├── deploy-bot.yml        # автоматический деплой бота на VPS
│       └── build-firmware.yml    # опционально: сборка прошивки
├── firmware/                     # код ESP32
│   ├── include/                  # заголовочные файлы
│   ├── src/                      # исходники
│   │   └── main.cpp
│   ├── lib/                      # локальные библиотеки (если нужны)
│   ├── platformio.ini            # если используешь PlatformIO (рекомендую)
│   └── README.md                 # описание прошивки
├── bot/                          # Telegram-бот на Python
|   ├── src/
|   │   ├── __init__.py
|   │   ├── __main__.py           # точка входа (python -m src)
|   │   ├── bot.py                # создание экземпляров Bot и Dispatcher
|   │   ├── config.py             # загрузка настроек из окружения
|   │   ├── handlers/             # все обработчики
|   │   │   ├── __init__.py
|   │   │   ├── start.py          # /start, /help
|   │   │   ├── status.py         # /status
|   │   │   ├── control.py        # команды управления (set_temp и т.п.)
|   │   │   └── webapp.py         # для Telegram Web App
|   │   ├── keyboards/            # клавиатуры (inline, reply)
|   │   │   ├── __init__.py
|   │   │   └── main_menu.py
|   │   ├── middlewares/          # middleware
|   │   │   ├── __init__.py
|   │   │   └── mqtt.py           # middleware, добавляющее MQTT клиент в данные
|   │   ├── mqtt_client.py        # класс для работы с MQTT (asyncio)
|   │   └── utils/                # вспомогательные функции
|   │       ├── __init__.py
|   │       └── logger.py
├── requirements.txt
├── Dockerfile
└── .env (игнорируется)
│   │   ├── __init__.py
│   │   ├── bot.py                # основной файл
│   │   ├── handlers/             # обработчики команд
│   │   ├── mqtt_client.py        # взаимодействие с MQTT
│   │   └── config.py             # конфигурация (чтение из .env)
│   ├── requirements.txt          # зависимости Python
│   ├── Dockerfile                # для контейнеризации (удобно на VPS)
│   ├── docker-compose.yml        # если будут доп. сервисы (например, MQTT брокер)
│   └── .env.example              # пример переменных окружения
├── web/                          # Telegram Web App (статический сайт)
│   ├── index.html
│   ├── style.css
│   ├── script.js                 # логика взаимодействия с Telegram WebApp и API (если нужно)
│   └── assets/                   # картинки и т.п.
├── scripts/                      # вспомогательные скрипты
│   ├── setup-mqtt.sh             # например, настройка брокера на VPS
│   └── ...
├── docs/                         # документация проекта
│   └── architecture.md           # описание архитектуры, протоколов
├── .gitignore
├── .editorconfig                 # единый стиль кода
└── README.md                     # общее описание проекта
```


## Развитие проекта:
1. Подготовить проект под работу на сервере
2. Написать бота
3. Подготовить сервер
4. Сделать автодеплой на сервер
5. Актуализировать проект на esp32
6. Написать Web морду для управления через web_app на телеграме.