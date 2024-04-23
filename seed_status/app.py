import asyncio

import pandas as pd
import streamlit as st

from seed_status.mult_requests import fetch_protocols_async


def process_time(x: str):
    try:
        date = pd.Timestamp(x).to_pydatetime()
        return date.strftime("%d/%m/%y %H:%M:%S")
    except:
        return ""


st.title("Protocolos prioritários - Escritório de Projetos")

protocolo_input = st.text_area("Inserir protocolo")
protocol_numbers = protocolo_input.strip().split("\n")

wrong_protocol_numbers = []

if protocolo_input:
    ds = []
    all_protocol_numbers = []
    for protocol_number in set(protocol_numbers):
        # items = {}
        # items["protocolo"] = protocol_number
        clean_protocol_number = protocol_number.replace("-", "").replace(".", "")
        all_protocol_numbers.append(clean_protocol_number)
        # data_from_protocolo = fetch_data_from_protocol(clean_protocol_number)
        # items.update(data_from_protocolo)

    all_data = asyncio.run(fetch_protocols_async(all_protocol_numbers))
    # Do this on a DF level
    # for key in ["Dias Sobrestado:", "Dias Arquivo Corrente:"]:
    #     if key in data_from_protocolo:
    #         items.pop(key)
    # ds.append(items)
    #     except:
    #     print(f"wrong protocol number - {protocol_number}")
    #     wrong_protocol_numbers.append(protocol_number)
    print(f"all_data {all_data}")
    df = pd.DataFrame(all_data)
    if "Enviado em:" in df:
        df["Enviado em:"] = df["Enviado em:"].apply(process_time)

    st.dataframe(df)

if wrong_protocol_numbers:
    st.text(f"Protocolos com erro: {wrong_protocol_numbers}")
