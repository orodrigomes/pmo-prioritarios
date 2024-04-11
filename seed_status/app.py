import streamlit as st
import pandas as pd
import numpy as np

from main import fetch_data_from_protocol

def process_time(x: str):
    date = pd.Timestamp(x).to_pydatetime()
    return date.strftime("%D %H:%M:%S")


st.title('Protocolos prioritários - Escritório de Projetos')

df = pd.DataFrame(data=[1,2,3],index=[4,5,6])

txt = st.text_area("Inserir protocolo")

protocol_numbers = txt.strip().split('\n')

wrong_protocol_numbers = []

if txt:

    dfs = []
    ds = []
    for protocol_number in set(protocol_numbers[-5:]):
        try:
            d1 = {}
            #Thu Apr 04 13:30:00 BRT 2024
            d1['protocolo'] = protocol_number
            clean_protocol_number = protocol_number.replace("-","").replace(".","")
            d = fetch_data_from_protocol(clean_protocol_number)
            d1.update(d)

            for key in ['Dias Sobrestado:','Dias Arquivo Corrente:']:
                if key in d:
                    d1.pop(key)
            ds.append(d1)
        except:
            print (f'wrong protocol number - {protocol_number}')
            wrong_protocol_numbers.append(protocol_number)

    df = pd.DataFrame(ds)
    df['Enviado em:'] = df['Enviado em:'].apply(process_time)
    st.dataframe(df)

if wrong_protocol_numbers:
    st.text(f"Protocolos com erro: {wrong_protocol_numbers}")
