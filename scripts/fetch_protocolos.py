import datetime

import pandas as pd
from sqlmodel import create_engine

from seed_status.app import build_dataframe_from_protocolos
from seed_status.settings import Settings

TABLENAME = "protocolo_status"


def build_engine():
    settings = Settings()
    engine = create_engine(
        f'postgresql+psycopg2://{settings.db_user}:{settings.db_password}@{settings.db_host}/{settings.db_user}')
    return engine


def write_df_to_db(df: pd.DataFrame):
    engine = build_engine()
    df.to_sql(TABLENAME, con=engine, if_exists="append", index=False)


def read_protocolos_from_db():
    engine = build_engine()
    protocolos_id_df = pd.read_sql_table("protocolos_id", engine)
    numeros_protocolo = protocolos_id_df['numero_protocolo'].tolist()
    return [str(i) for i in numeros_protocolo]


def main():
    print('start')
    protocol_numbers = read_protocolos_from_db()
    # protocol_numbers = ["221924738", "222105471", "220496163", "221541154", "220534537"]
    df = build_dataframe_from_protocolos(protocol_numbers)
    # df = pd.DataFrame.from_records({'a': 1}, index=[0])
    df['datetime_utc'] = datetime.datetime.utcnow()
    print(df)
    write_df_to_db(df)
    print('end')


if __name__ == "__main__":
    main()
