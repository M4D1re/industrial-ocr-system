# Industrial OCR Recorder

## Обзор

Industrial OCR Recorder — desktop-приложение для автоматического съёма показаний с экранов промышленного оборудования с использованием USB и RTSP камер.

Система получает видеопоток с подключенных камер, обрабатывает выделенные ROI (Region Of Interest) области через OCR, сохраняет показания в SQLite и экспортирует завершённые сессии в переносимые `.session.zip` архивы.

Приложение разработано как production-style industrial recorder для Windows 10/11.

---

# Основные возможности

## Поддержка камер

* USB камеры
* RTSP IP камеры
* Multi-camera архитектура
* Параллельная работа нескольких камер
* Включение/отключение камер во время работы
* Автоматическое обнаружение USB камер
* Ручное добавление RTSP камер
* Обработка переподключения камер
* Мониторинг FPS камер

---

## Система ROI

* Создание ROI мышью
* Отображение ROI поверх видео
* Независимые ROI для каждой камеры
* До 10 ROI на одну камеру
* Включение/отключение ROI
* Удаление ROI
* Сохранение ROI в базе данных

---

# OCR Pipeline

* Интеграция PaddleOCR
* Предобработка изображений
* Преобразование в grayscale
* Шумоподавление
* Thresholding
* Усиление контраста
* Масштабирование ROI
* Оценка confidence OCR
* Извлечение числовых значений
* Поддержка decimal numbers
* Поддержка отрицательных чисел
* Генерация debug изображений

---

## Сессии записи

* Start Session
* Stop Session
* Хранение readings с session_id
* SQLite база данных
* Экспорт завершённых сессий в `.session.zip`

---

## Система экспорта

Каждая завершённая сессия экспортируется в:

```text
session_<id>.session.zip
```

Содержимое архива:

```text
session.db
metadata.json
debug_images/
```

---

## Runtime возможности

* Неблокирующий UI
* OCR в background threads
* Multi-threaded acquisition
* Цветные runtime логи
* Мониторинг OCR статусов
* Панель текущих readings
* Управление сессиями

---

# Технологический стек

## Core

* Python 3.12+

## GUI

* PySide6
* Qt for Python

## Computer Vision

* OpenCV

## OCR

* PaddleOCR

## Database

* SQLite

## Packaging

* PyInstaller

---

# Архитектура системы

```text
Камеры
    ↓
Frame Acquisition
    ↓
ROI Extraction
    ↓
OCR Pipeline
    ↓
SQLite Readings Storage
    ↓
Session Export
```

---

# Структура проекта

```text
industrial_ocr_system/
│
├── app/
│   ├── analytics/
│   ├── config/
│   ├── database/
│   ├── models/
│   ├── ocr/
│   ├── resources/
│   ├── services/
│   ├── ui/
│   ├── utils/
│   └── vision/
│
├── data/
│   ├── app.db
│   └── debug/
│
├── docs/
├── scripts/
├── tests/
│
├── main.py
├── requirements.txt
├── pyproject.toml
└── README.md
```

---

# Установка

## Требования

* Windows 10 или Windows 11
* Python 3.12+
* Git
* PyCharm Community или Professional

---

## Клонирование репозитория

```bash
git clone <repository_url>
cd industrial_ocr_system
```

---

## Создание виртуального окружения

```bash
python -m venv .venv
```

---

## Активация виртуального окружения

### PowerShell

```bash
.venv\Scripts\activate
```

---

## Установка зависимостей

```bash
pip install -r requirements.txt
```

---

# Запуск приложения

## Запуск программы

```bash
python main.py
```

---

# Первый запуск

При старте приложения:

* USB камеры автоматически обнаруживаются
* Все камеры отключены по умолчанию
* Видеопоток автоматически не запускается

В центральной области отображается:

```text
Активные камеры отсутствуют.
Выберите камеру и нажмите Enable selected camera.
```

---

# Управление камерами

## Включение камеры

1. Выберите камеру в Camera Panel
2. Нажмите:

```text
Enable selected camera
```

После этого видеопоток будет запущен.

---

## Отключение камеры

1. Выберите камеру
2. Нажмите:

```text
Disable selected camera
```

Поток камеры остановится.

Другие камеры продолжат работать.

---

## Добавление RTSP камеры

1. Нажмите:

```text
Add Camera
```

2. Выберите:

```text
RTSP
```

3. Введите RTSP URL:

```text
rtsp://login:password@192.168.1.100:554/stream
```

4. Нажмите:

```text
Test connection
```

5. Сохраните камеру.

---

# Работа с ROI

## Создание ROI

1. Включите камеру
2. Выделите область мышью поверх видео
3. ROI будет создан автоматически
4. ROI появится в ROI Panel

---

## Отключение ROI

1. Выберите ROI в ROI Panel
2. Нажмите:

```text
Disable selected ROI
```

Отключённый ROI:

* остаётся в базе данных
* не участвует в OCR
* отображается серым цветом

---

## Включение ROI

1. Выберите ROI
2. Нажмите:

```text
Enable selected ROI
```

---

## Удаление ROI

1. Выберите ROI
2. Нажмите:

```text
Delete selected ROI
```

---

# Работа с сессиями

## Start Session

Нажмите:

```text
Start Session
```

Будет создана новая recording session.

Все OCR readings будут привязаны к этой сессии.

---

## Start Auto OCR

Нажмите:

```text
Start Auto OCR
```

Система начнёт:

* обрабатывать все enabled камеры
* обрабатывать все enabled ROI
* сохранять OCR readings в базу данных

---

## Настройка интервала опроса

Поля в toolbar:

```text
Hours
Minutes
Seconds
```

используются для настройки интервала OCR polling.

---

## Stop Session

Нажмите:

```text
Stop Session
```

Приложение:

1. остановит recording session
2. запросит подтверждение
3. предложит путь сохранения
4. создаст `.session.zip` архив

---

# Формат экспорта сессии

## Структура архива

```text
session_1.session.zip
│
├── session.db
├── metadata.json
└── debug_images/
```

---

## Пример metadata.json

```json
{
    "format": "industrial_ocr_session",
    "format_version": 1,
    "exported_at": "2026-05-10T10:00:00",
    "session": {
        "id": 1,
        "name": "Recording Session",
        "status": "completed"
    },
    "readings_count": 1540
}
```

---

# Структура базы данных

## Основные таблицы

### cameras

Хранит конфигурации камер.

### roi_regions

Хранит координаты и настройки ROI.

### sessions

Хранит recording sessions.

### readings

Хранит OCR readings.

### events

Зарезервирована для будущей event persistence.

### settings

Хранит настройки приложения.

---

# OCR Pipeline

```text
Frame
    ↓
ROI Crop
    ↓
Grayscale
    ↓
Denoise
    ↓
Threshold
    ↓
Contrast Enhancement
    ↓
Resize
    ↓
PaddleOCR
    ↓
Postprocessing
    ↓
Database Save
```

---

# Панель Logs

Runtime логи используют цветовые уровни.

## INFO

Нейтральная системная информация.

## SUCCESS

Успешные OCR операции.

## WARNING

Некритичные предупреждения.

## ERROR

Критические ошибки OCR или runtime.

---

# Панель OCR Status

Отображает:

* состояние сессии
* состояние Auto OCR
* состояние OCR worker
* количество активных камер
* последний OCR result

---

# Очистка базы данных

## Clear Session Data

Удаляет:

* sessions
* readings
* events

Сохраняет:

* камеры
* ROI regions

---

## Factory Reset DB

Полностью сбрасывает базу данных.

Удаляет:

* камеры
* ROI regions
* sessions
* readings
* events

Также сбрасываются SQLite auto-increment индексы.

---

# Модель потоков

Приложение использует background threads для предотвращения блокировки UI.

## Main UI Thread

Отвечает за:

* рендеринг GUI
* обработку действий пользователя
* отображение видеопотока

## Camera Threads

Отвечают за:

* получение кадров
* reconnect logic
* обновление FPS

## OCR Worker Threads

Отвечают за:

* обработку ROI
* выполнение OCR
* preprocessing pipeline
* генерацию debug images

---

# Производительность

* UI thread никогда не блокируется OCR
* Камеры работают независимо
* Сбой одной камеры не останавливает остальные
* Disabled ROI полностью пропускаются
* Disabled камеры не используют ресурсы acquisition subsystem

---

# Troubleshooting

## Камера не запускается

Проверьте:

* камера включена
* камера не используется другим приложением
* RTSP URL корректен

---

## OCR возвращает пустые результаты

Возможные причины:

* ROI выделен некорректно
* низкий контраст изображения
* нечитаемый дисплей оборудования
* слишком низкий OCR confidence

Проверьте debug изображения в:

```text
data/debug/
```

---

## Приложение зависает

Возможные причины:

* слишком маленький OCR interval
* слишком большое количество ROI
* нестабильный RTSP поток

Рекомендуется:

* увеличить polling interval
* уменьшить количество камер
* уменьшить количество ROI

---

# Сборка executable

## PyInstaller Build

```bash
pyinstaller main.spec
```

Сгенерированный executable:

```text
dist/IndustrialOCRRecorder.exe
```

---

# Планируемые компоненты

## Industrial OCR Analyzer

Отдельное приложение для:

* графиков
* статистики
* trend analysis
* PDF reports
* Excel export
* anomaly detection

Analyzer будет читать экспортированные `.session.zip` архивы.

---

# Лицензия

Промышленный проект.
