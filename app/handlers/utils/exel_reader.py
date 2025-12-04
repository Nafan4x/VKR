import asyncio
import os

import pandas as pd

from app.config import config


async def get_number_by_name(fio: str) -> str | None:
    file_path = f'{config.RESOURCE_PATH}/exel'
    files = os.listdir(file_path)
    if files:  # если список не пустой
        filepath = os.path.join(file_path, files[0])
    df = await asyncio.to_thread(pd.read_excel, filepath)

    row = df.loc[df['ФИО'] == fio]

    if row.empty:
        return None

    return str(row.iloc[0]['Номер ЭПБ'])

if __name__ == '__main__':
    print(asyncio.run(get_number_by_name('Агеев 1 Сергеевич')))