import datetime

import pandas as pd
import streamlit as st

st.set_page_config(layout="wide")
from streamlit_utils import sync_main


def process_time(x: str):
    date = pd.Timestamp(x).to_pydatetime()
    # return date.strftime("%d/%m/%y %H:%M:%S")
    return date


def color_vowel(value):
    return f"background-color: green;" if value < 3 else None


st.title("Protocolos prioritários - Escritório de Projetos")

protocolo_input = st.text_area("Inserir protocolo")
protocol_numbers = protocolo_input.strip().split("\n")

wrong_protocol_numbers = []


def safe_to_int(x):
    if pd.isna(x):
        return 0
    days_diff = (datetime.datetime.now() - x).days
    return int(days_diff)


if protocolo_input:
    ds = []
    start = datetime.datetime.now()
    L = sync_main(list(set(protocol_numbers)))
    st.write(f'elapsed {((datetime.datetime.now() - start).seconds)} sec')
    df = pd.DataFrame(L)
    df.dropna(inplace=True)
    df.drop(columns=["Dias Sobrestado:", "Dias Arquivo Corrente:", "Motivo:"], errors='ignore', inplace=True)

    if "Enviado em:" in df:
        df["Enviado em:"] = df["Enviado em:"].apply(process_time)
        df['dias_parado'] = df["Enviado em:"].apply(lambda x: safe_to_int(x))


    def extract_nucleo(x, sep, index):
        try:
            return x.split(sep)[index]
        except:
            return None


    df['N1- Órgao'] = df['Onde está:'].apply(lambda x: extract_nucleo(x, "-", 0))
    df['N2 - Diretoria'] = df['Onde está:'].apply(lambda x: extract_nucleo(x, "/", 1))
    df['N3 - Núcleo/Grupo'] = df['Onde está:'].apply(lambda x: extract_nucleo(x, "/", 2))
    df['N4 - Coordenação'] = df['Onde está:'].apply(lambda x: extract_nucleo(x, "/", 3))

    df.rename(columns={'Onde está:': 'Onde está',
                       'Enviado em:': 'Enviado em',
                       'Total Dias em Trâmite:': 'Dias em trâmite'}, inplace=True)

    df.sort_values(by="protocolo", ascending=True, inplace=True)

    column_order = ["protocolo", "Dias em trâmite"]
    column_order += [i for i in df.columns if i not in column_order and i != 'dias_parado']
    column_order += ['dias_parado']
    st.dataframe(df.style.applymap(color_vowel, subset=["dias_parado"]), hide_index=True,
                 column_order=column_order)

    st.write(
        f"Protocolos com erro - {[i for i in list(set(protocol_numbers)) if i not in df['protocolo'].unique().tolist()]}")

if wrong_protocol_numbers:
    st.text(f"Protocolos com erro: {wrong_protocol_numbers}")
