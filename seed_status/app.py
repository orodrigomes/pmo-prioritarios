import datetime

import pandas as pd
import streamlit as st

st.set_page_config(layout="wide")
from streamlit_utils import fetch_data_from_protocol


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

if protocolo_input:
    ds = []
    for protocol_number in set(protocol_numbers):
        try:
            items = {}
            # Thu Apr 04 13:30:00 BRT 2024
            items["protocolo"] = protocol_number
            clean_protocol_number = protocol_number.replace("-", "").replace(".", "")
            data_from_protocolo = fetch_data_from_protocol(clean_protocol_number)
            items.update(data_from_protocolo)

            for key in ["Dias Sobrestado:", "Dias Arquivo Corrente:"]:
                if key in data_from_protocolo:
                    items.pop(key)
            ds.append(items)
        except:
            print(f"wrong protocol number - {protocol_number}")
            wrong_protocol_numbers.append(protocol_number)

    df = pd.DataFrame(ds)
    if "Enviado em:" in df:
        df["Enviado em:"] = df["Enviado em:"].apply(process_time)
        df['dias_parado'] = df["Enviado em:"].apply(
            lambda x: (datetime.datetime.now() - x).days)


    def extract_nucleo(x, sep, index):
        try:
            return x.split(sep)[index]
        except:
            return None


    df['N1- Órgao'] = df['Onde está:'].apply(lambda x: extract_nucleo(x, "-", 0))
    df['N2 - Diretoria'] = df['Onde está:'].apply(lambda x: extract_nucleo(x, "/", 1))
    df['N3 - Núcleo/Grupo'] = df['Onde está:'].apply(lambda x: extract_nucleo(x, "/", 2))
    df['N4 - Coordenação'] = df['Onde está:'].apply(lambda x: extract_nucleo(x, "/", 3))

    df.rename(columns={'Onde está:': 'Onde está', 'Motivo:': 'Motivo',
                       'Enviado em:': 'Enviado em',
                       'Total Dias em Trâmite:': 'Dias em trâmite'}, inplace=True)

    df.sort_values(by="protocolo", ascending=True, inplace=True)

    st.dataframe(df.style.applymap(color_vowel, subset=["dias_parado"]), hide_index=True)

if wrong_protocol_numbers:
    st.text(f"Protocolos com erro: {wrong_protocol_numbers}")
