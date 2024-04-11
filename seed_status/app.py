import pandas as pd
import streamlit as st

from streamlit_utils import fetch_data_from_protocol


def process_time(x: str):
    date = pd.Timestamp(x).to_pydatetime()
    return date.strftime("%D %H:%M:%S")


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
    df["Enviado em:"] = df["Enviado em:"].apply(process_time)
    st.dataframe(df)

if wrong_protocol_numbers:
    st.text(f"Protocolos com erro: {wrong_protocol_numbers}")
