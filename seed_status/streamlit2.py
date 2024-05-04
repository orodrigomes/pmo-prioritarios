import os

import pandas as pd
import streamlit as st

st.set_page_config(layout="wide")
from dotenv import load_dotenv
from sqlmodel import create_engine

load_dotenv()

##################################################
st.title("Protocolos from DB")

# Initialize connection.
db_user, db_password, db_host = os.environ['DB_USER'], os.environ['DB_PASSWORD'], os.environ['DB_HOST']
engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}/{db_user}")

# Perform query.
with engine.connect() as conn:
    df = pd.read_sql('SELECT * FROM protocolo_status;', conn)
    df['from'] = df['']

st.dataframe(df)
