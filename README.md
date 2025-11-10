# Kafka Local Cluster

---

> **Внимание!**
>
> Этот проект — учебный и демонстрационный.
> Файл `.env` добавлен в репозиторий только для удобства локального тестирования.
> **В реальных (продакшн) проектах не рекомендуется хранить `.env` в git!**
> Используйте секреты, переменные окружения CI/CD или защищённые vault-хранилища.

---

---

## Описание

Проект для локального развертывания кластера Apache Kafka (3 брокера, KRaft mode, без ZooKeeper) с веб-интерфейсом Kafka UI и контейнером для Python-клиента. Автоматическое создание топиков отключено для лучшего контроля.

---

## Структура проекта

```
.
├── app/
│   ├── producer.py         # Асинхронный продюсер на aiokafka
│   ├── consumer.py         # Асинхронный консьюмер на aiokafka
│   ├── create_topic.py     # Асинхронное создание топика через aiokafka.admin
│   └── requirements.txt    # Зависимости Python-клиента aiokafka
├── .env                    # Переменные окружения для клиента (используется автоматически)
├── docker-compose.yml      # Описание всех сервисов и сетей кластера
├── run.sh                  # Скрипт автоматического запуска и проверки кластера
└── README.md               # Документация и инструкции
```

**Описание ключевых компонентов:**

- `app/` — директория с исходным кодом Python-клиента (aiokafka, современный стиль)
- `.env` — переменные окружения для клиента (топик, брокеры, партиции и т.д.)
- `docker-compose.yml` — конфигурация кластера Kafka, клиента и UI
- `run.sh` — автоматизация запуска, healthcheck, создание топика
- `README.md` — вся документация и инструкции по работе

**Сервисы в docker-compose.yml:**

- `kafka1`, `kafka2`, `kafka3` — брокеры Kafka (кластер, репликация, отказоустойчивость)
- `app` — контейнер с Python-клиентом для aiokafka
- `kafka-ui` — веб-интерфейс для управления и мониторинга

---

## Быстрый старт

### 1. Клонируйте репозиторий и перейдите в папку проекта

### 2. Сделайте скрипт запуска исполняемым

```bash
chmod +x run.sh
```

### 3. Запустите кластер и дождитесь готовности

```bash
./run.sh
```

Скрипт автоматически:

- пересоберёт и запустит все сервисы
- дождётся готовности всех брокеров (healthcheck)
- создаст тестовый топик (если реализовано в create_topic.py)
- выведет инструкции для тестирования

### 4. Откройте Kafka UI

- Перейдите в браузере: http://localhost:8080

### 5. Остановить/перезапустить кластер

```bash
docker compose down         # остановить и удалить контейнеры
docker compose down -v      # остановить и удалить контейнеры + volume
docker compose restart      # перезапустить все сервисы
docker compose build        # Собирает образы для всех сервисов, описанных в docker-compose.yml
```

---

## Работа с топиками через CLI

### Создать топик вручную

```bash
docker exec -it kafka1 bash
cd /opt/kafka/bin
./kafka-topics.sh --bootstrap-server localhost:9092 --create --topic my-topic --partitions 3 --replication-factor 3
```

### Посмотреть список топиков

```bash
./kafka-topics.sh --bootstrap-server localhost:9092 --list
```

---

## Отправка и чтение сообщений через CLI

### Отправить сообщение (продюсер)

```bash
./kafka-console-producer.sh --bootstrap-server localhost:9092 --topic my-topic
# Введите сообщение и нажмите Enter
```

### Прочитать сообщения (консюмер)

```bash
./kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic my-topic --from-beginning
```

### Сообщения с ключом

- Продюсер:
  ```bash
  ./kafka-console-producer.sh --bootstrap-server localhost:9092 --topic my-topic --property "parse.key=true" --property "key.separator=:"
  # Пример: mykey:myvalue
  ```
- Консюмер:
  ```bash
  ./kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic my-topic --from-beginning --property "print.key=true" --property "key.separator=:"
  ```

---

## Работа с Python-клиентом

1. **Войти в контейнер app:**
   ```bash
   docker exec -it app bash
   ```
2. **Установить дополнительные библиотеки (если нужно):**
   ```bash
   pip install kafka-python confluent-kafka
   ```
3. **Пример асинхронного продюсера/консюмера — см. документацию aiokafka**

---

## Рекомендации и best practices

- **Топики создавайте вручную** — автосоздание отключено для предотвращения появления лишних топиков.
- **Количество партиций** — выбирайте исходя из числа консюмеров и нагрузки (обычно 3–12 для теста, больше для продакшена).
- **Репликация** — для отказоустойчивости используйте replication-factor >= 2.
- **Документируйте назначение топиков и их параметры.**
- **Для продакшена** — добавьте аутентификацию, шифрование, мониторинг (Prometheus, Grafana).

---

## Healthcheck (опционально)

Healthcheck позволяет Docker автоматически проверять, что брокер Kafka внутри контейнера действительно работает и отвечает на запросы. Если брокер не отвечает, контейнер считается "нездоровым".

Добавлена секция healthcheck для брокеров в docker-compose.yml:

```yaml
healthcheck:
  test:
    [
      "CMD",
      "kafka-broker-api-versions.sh",
      "--bootstrap-server",
      "localhost:9092",
    ]
  interval: 30s
  timeout: 10s
  retries: 5
```

---

## Примеры Python-кода

## Примеры работы с Kafka (Python)

В папке `app/aiokafka/` находятся современные асинхронные примеры для работы с Kafka на базе библиотеки aiokafka:

- `producer.py` — асинхронный продюсер
- `consumer.py` — асинхронный консьюмер

**Как запускать примеры:**

В папке `app/` находятся современные асинхронные примеры для работы с Kafka на базе библиотеки aiokafka:

- `producer.py` — асинхронный продюсер
- `consumer.py` — асинхронный консьюмер
- `create_topic.py` — асинхронное создание топика через AIOKafkaAdminClient

**Как запускать примеры:**

```bash
# Создать топик:
---
# Отправить сообщение:

# Получить сообщение:
## TODO
```
