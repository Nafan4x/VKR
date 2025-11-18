import sqlite3


def update_message(text, callback_text):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE message SET text = ? WHERE callback_text = ?', (text, callback_text))
    conn.commit()
    conn.close()


if __name__ == '__main__':
    text = """
🤖 <i>Это ваш персональный помощник</i>

📋 <b>Что я умею:</b>
• Помогать с задачами
• Отвечать на вопросы
• Предоставлять информацию"""

    update_message(text, 'main_page')