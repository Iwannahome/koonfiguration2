#!/bin/bash

echo "=== Демонстрация обработки ошибок ==="
echo ""

echo "1. Отсутствует обязательный аргумент --repository:"
python3 visualizer.py -p vim -o graph.png
echo ""

echo "2. Пустое имя пакета:"
python3 visualizer.py -p "" -r http://repo.com -o graph.png
echo ""

echo "3. Неверное расширение выходного файла:"
python3 visualizer.py -p vim -r http://repo.com -o output.txt
echo ""

echo "4. Корректный запуск:"
python3 visualizer.py -p vim -r http://archive.ubuntu.com/ubuntu -o graph.png

