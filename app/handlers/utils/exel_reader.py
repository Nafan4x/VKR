import asyncio

import pandas as pd


async def get_number_by_name(fio: str) -> str | None:
    filepath = 'resources/files/Список из 1с студенты.xls'
    df = await asyncio.to_thread(pd.read_excel, filepath)

    row = df.loc[df['ФИО'] == fio]

    if row.empty:
        return None

    return str(row.iloc[0]['Номер ЭПБ'])

if __name__ == '__main__':
    print(asyncio.run(get_number_by_name('Агеев 1 Сергеевич')))