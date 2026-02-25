import io
import asyncio
from datetime import datetime
from typing import List, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text    


async def create_table_txt(users_data: List[dict]) -> io.BytesIO:
    """
    Асинхронно создает txt файл с таблицей пользователей
    Args:
        users_data: список словарей с данными пользователей
    Returns:
        io.BytesIO: файл в памяти для отправки в Telegram
    """
    # Используем loop.run_in_executor для асинхронной записи
    loop = asyncio.get_event_loop()

    def _write_table():
        """Синхронная функция записи таблицы"""
        memory_file = io.BytesIO()
        # Заголовок
        memory_file.write(f"{'=' * 80}\n".encode('utf-8'))
        memory_file.write(f"{'ТАБЛИЦА ПОЛЬЗОВАТЕЛЕЙ':^80}\n".encode('utf-8'))
        memory_file.write(f"{'=' * 80}\n".encode('utf-8'))
        memory_file.write(f"Дата выгрузки: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n".encode('utf-8'))
        memory_file.write(f"Всего пользователей: {len(users_data)}\n".encode('utf-8'))

        memory_file.write(f"{'=' * 80}\n\n".encode('utf-8'))

        if users_data:
            # Определяем заголовки колонок
            headers = list(users_data[0].keys())
            # Вычисляем ширину колонок
            col_widths = {}
            for header in headers:
                max_width = len(header)
                for user in users_data:
                    value = str(user.get(header, 'N/A'))
                    max_width = max(max_width, len(value))
                col_widths[header] = min(max_width, 30)  # Ограничиваем ширину

            # Создаем разделитель
            separator = '+' + '+'.join(['-' * (col_widths[h] + 2) for h in headers]) + '+\n'

            # Записываем заголовки
            memory_file.write(separator.encode('utf-8'))
            header_line = '|'
            for header in headers:
                header_line += f" {header:<{col_widths[header]}} |"
            memory_file.write((header_line + '\n').encode('utf-8'))
            memory_file.write(separator.encode('utf-8'))

            # Записываем данные
            for user in users_data:
                line = '|'
                for header in headers:
                    value = str(user.get(header, 'N/A'))
                    line += f" {value:<{col_widths[header]}} |"
                memory_file.write((line + '\n').encode('utf-8'))

            memory_file.write(separator.encode('utf-8'))
        else:
            memory_file.write("Нет данных о пользователях\n".encode('utf-8'))

        memory_file.write(f"\n{'=' * 80}\n".encode('utf-8'))
        memory_file.write(f"{'КОНЕЦ ФАЙЛА':^80}\n".encode('utf-8'))
        memory_file.write(f"{'=' * 80}\n".encode('utf-8'))

        memory_file.seek(0)
        return memory_file

    # Асинхронно выполняем запись в файл
    memory_file = await loop.run_in_executor(None, _write_table)
    return memory_file
