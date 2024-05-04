'''
- 2 tables - PROTOCOL_NUMBERS, PROTOCOL_STATUS
- Get all protocol from DB
- Get updated status
- Write updated status to DB (as new row)
'''
import asyncio
import os
import time

import pandas as pd
from dotenv import load_dotenv
from seed_status.app import process_time
from sqlmodel import create_engine

from seed_status.streamlit_utils import fetch_data_from_protocol

'''
Streamlit
- New input box (add protocol)
- New text box (already available e-protocols)
- New button (force refresh)
'''

'''
Jobs
- Deploy as lambda function
'''

'''
Streamlit
- Create chat using Langchain SQLAgent (see link in Obsidian) for chatting with data (e.g. latest protocols which
are in the same place for more than 100 days)
'''


from PROTOCOLOS import PROTOCOLOS


async def fetch_protocolo(protocol_number: str):
    try:
        clean_protocol_number = protocol_number.replace("-", "").replace(".", "")
        ds = fetch_data_from_protocol(clean_protocol_number)
        ds['clean_protocol_number'] = int(clean_protocol_number)
        return ds
    except Exception as e:
        print (f"Exception occured {protocol_number}", e)
        return {}


async def main():
    print('start')
    load_dotenv()
    L = await asyncio.gather(
        *[fetch_protocolo(i) for i in PROTOCOLOS]
    )
    df = pd.DataFrame(L)
    df.dropna(inplace=True)
    cols_numeric = ["Dias Sobrestado:", 'Total Dias em Trâmite:',"Dias Arquivo Corrente:" ]
    for col in cols_numeric:
        df[col] = pd.to_numeric(df[col])
    
    if "Enviado em:" in df:
        df["Enviado em:"] = df["Enviado em:"].apply(process_time)
    
    # ToDo - Use BaseSettings
    db_user, db_password, db_host = os.environ['DB_USER'], os.environ['DB_PASSWORD'], os.environ['DB_HOST']
    engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}/{db_user}")
    print(df.head())
    df.to_sql("protocolo_status", engine, if_exists="append")

    print('end')

def sync_main():
    asyncio.run(main())

# if __name__ == "__main__":
#    asyncio.run(main())

import schedule
schedule.every(1).hours.do(sync_main)

while True:
    schedule.run_pending()
    time.sleep(60)
