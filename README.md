# 🖼️ Background Remover API

REST API для удаления фона с изображений на основе нейронных сетей. Построен на **FastAPI**, использует модели из **HuggingFace Transformers**, разворачивается через **Docker**.

## Стек технологий

- **Python 3.11**
- **FastAPI** + **Uvicorn** — веб-сервер
- **PyTorch** + **Transformers** + **Torchvision** — нейросетевой инференс
- **Pillow** — обработка изображений
- **Kornia** + **Einops** + **Timm** — вспомогательные CV-библиотеки
- **Docker** / **Docker Compose** — контейнеризация

## Быстрый старт

### Через Docker Compose (рекомендуется)

```bash
git clone https://github.com/AlexCh-info/test_case_triumf.git
cd test_case_triumf
docker compose up --build
```

API будет доступен по адресу: `http://localhost:8000`

> При первом запуске Docker автоматически скачает веса модели с HuggingFace. Это может занять несколько минут. Веса кешируются в Docker volume `hf_cache` и при следующих запусках загружаются мгновенно.

### Локально (без Docker)

```bash
git clone https://github.com/AlexCh-info/test_case_triumf.git
cd test_case_triumf
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Использование

После запуска документация доступна по адресам:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Пример запроса (curl)

```bash
curl -X POST "http://localhost:8000/remove-bg" \
  -F "file=@your_image.jpg" \
  --output result.png
```

В ответ вернётся PNG с прозрачным фоном.

## Структура проекта

```
test_case_triumf/
├── app/
│   └── main.py          # Точка входа FastAPI, роуты
├── Dockerfile            # Образ на python:3.11-slim
├── compose.yaml          # Docker Compose конфигурация
├── requirements.txt      # Зависимости Python
└── README.md
```

## Конфигурация

| Параметр | Значение по умолчанию | Описание |
|---|---|---|
| Порт | `8000` | HTTP-порт сервиса |
| Лимит RAM | `4 GB` | Ограничение памяти контейнера |
| Кеш моделей | Docker volume `hf_cache` | Персистентное хранилище весов |

Для изменения порта отредактируйте `compose.yaml`:
```yaml
ports:
  - "YOUR_PORT:8000"
```

## Требования к системе

- Docker 20.10+ и Docker Compose v2
- Минимум 4 ГБ оперативной памяти
- ~2 ГБ свободного места на диске (для весов модели)
- GPU опционален — сервис работает и на CPU

## Лицензия

Unlicense — см. файл [LICENSE](LICENSE).
