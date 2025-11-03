#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Инструмент визуализации графа зависимостей для менеджера пакетов Ubuntu (apt)
Этап 1: Минимальный прототип с конфигурацией
"""

import argparse
import sys


def create_parser():
    """
    Создаёт и настраивает парсер аргументов командной строки.
    
    Returns:
        argparse.ArgumentParser: Настроенный парсер аргументов
    """
    # Создаём объект парсера с описанием программы
    parser = argparse.ArgumentParser(
        description='Инструмент визуализации графа зависимостей для apt пакетов',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  %(prog)s -p vim -r http://archive.ubuntu.com/ubuntu -o graph.png
  %(prog)s --package firefox --repository /path/to/test/repo --test-mode --output diagram.png
        """
    )
    
    # Добавляем обязательные аргументы
    # 1. Имя анализируемого пакета
    parser.add_argument(
        '-p', '--package',
        type=str,
        required=True,
        help='Имя анализируемого пакета (например: vim, firefox, nginx)'
    )
    
    # 2. URL-адрес репозитория или путь к файлу тестового репозитория
    parser.add_argument(
        '-r', '--repository',
        type=str,
        required=True,
        help='URL-адрес репозитория или путь к файлу тестового репозитория'
    )
    
    # 3. Режим работы с тестовым репозиторием (опциональный флаг)
    parser.add_argument(
        '-t', '--test-mode',
        action='store_true',  # Если флаг указан, значение True, иначе False
        default=False,
        help='Режим работы с тестовым репозиторием (по умолчанию: выключен)'
    )
    
    # 4. Имя сгенерированного файла с изображением графа
    parser.add_argument(
        '-o', '--output',
        type=str,
        required=True,
        help='Имя сгенерированного файла с изображением графа (например: graph.png)'
    )
    
    return parser


def validate_arguments(args):
    """
    Валидирует аргументы командной строки и выполняет дополнительные проверки.
    
    Args:
        args: Объект с разобранными аргументами
        
    Raises:
        ValueError: Если аргументы не прошли валидацию
    """
    errors = []
    
    # Проверка имени пакета
    if not args.package or len(args.package.strip()) == 0:
        errors.append("Имя пакета не может быть пустым")
    
    # Проверка репозитория
    if not args.repository or len(args.repository.strip()) == 0:
        errors.append("URL или путь к репозиторию не может быть пустым")
    
    # Проверка расширения выходного файла
    valid_extensions = ['.png', '.svg', '.jpg', '.jpeg']
    if not any(args.output.lower().endswith(ext) for ext in valid_extensions):
        errors.append(
            f"Имя выходного файла должно иметь одно из расширений: {', '.join(valid_extensions)}"
        )
    
    # Если есть ошибки, выбрасываем исключение
    if errors:
        raise ValueError("\n".join(errors))


def print_configuration(args):
    """
    Выводит все настроенные параметры в формате ключ-значение.
    
    Args:
        args: Объект с разобранными аргументами
    """
    print("=" * 60)
    print("КОНФИГУРАЦИЯ ПРИЛОЖЕНИЯ")
    print("=" * 60)
    print(f"{'Параметр':<30} | {'Значение'}")
    print("-" * 60)
    print(f"{'Имя пакета':<30} | {args.package}")
    print(f"{'Репозиторий':<30} | {args.repository}")
    print(f"{'Режим тестирования':<30} | {'Включён' if args.test_mode else 'Выключен'}")
    print(f"{'Выходной файл':<30} | {args.output}")
    print("=" * 60)


def main():
    """
    Главная функция программы.
    """
    try:
        # Создаём парсер
        parser = create_parser()
        
        # Разбираем аргументы командной строки
        args = parser.parse_args()
        
        # Валидируем аргументы
        validate_arguments(args)
        
        # Выводим конфигурацию
        print_configuration(args)
        
        # Успешное завершение
        print("\n✓ Этап 1: Конфигурация успешно обработана!")
        return 0
        
    except ValueError as e:
        # Обработка ошибок валидации
        print(f"\n✗ ОШИБКА ВАЛИДАЦИИ:", file=sys.stderr)
        print(f"{e}", file=sys.stderr)
        return 1
        
    except Exception as e:
        # Обработка прочих ошибок
        print(f"\n✗ НЕПРЕДВИДЕННАЯ ОШИБКА:", file=sys.stderr)
        print(f"{e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
