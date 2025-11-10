#!/bin/bash

echo "✅ Запуск Kafka кластера..."
docker compose down -v
docker compose up -d



echo "⏳ Проверка статуса брокеров Kafka..."
unhealthy=0
for broker in kafka1 kafka2 kafka3; do
  status=$(docker inspect -f '{{.State.Health.Status}}' $broker 2>/dev/null)
  if [ "$status" != "healthy" ]; then
    unhealthy=1
    echo "➡️  $broker: $status"
  fi
done
if [ $unhealthy -eq 1 ]; then
  echo "⏳ Кластер запускается, ожидайте..."
else
  echo "✅ Все брокеры healthy, продолжаем работу."
fi


echo "🔍 Проверка kafka-client..."

# Имя контейнера клиента (проверьте, что совпадает с docker-compose.yml)
client_container="app"
status=$(docker inspect -f '{{.State.Status}}' "$client_container" 2>/dev/null)
if [ -z "$status" ]; then
  echo "❌ Контейнер клиента ($client_container) не найден! Проверьте docker ps -a или docker-compose.yml."
else
  echo "  $client_container: $status"
  if [ "$status" = "running" ]; then
    echo "✅ $client_container готов"
  else
    echo "⚠️  $client_container не в статусе running, проверьте контейнер!"
  fi
fi

echo "📊 Текущее использование ресурсов контейнеров:"
docker stats --no-stream



echo "✅ Кластер готов к работе!"
echo ""
echo "Для тестирования запустите в разных терминалах:"
echo "  Consumer: docker exec -it $client_container python consumer.py"
echo "  Producer: docker exec -it $client_container python producer.py"
echo ""
echo "Для остановки: docker compose down"
echo "Для полной очистки: docker compose down -v"
echo ""
echo "Веб-интерфейс Kafka UI: http://localhost:8080/"