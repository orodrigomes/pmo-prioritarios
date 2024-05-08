import asyncio

import requests
import streamlit as st
from bs4 import BeautifulSoup


@st.cache_data(ttl=3600)
def fetch_data_from_protocol(protocol_number: str):
    print(f"""Fetching data for {protocol_number}""")
    r = requests.get(
        f"https://www.eprotocolo.pr.gov.br/spiweb/consultarProtocoloDigital.do?action=pesquisar&numeroProtocolo={protocol_number}",
        verify=False,
    )
    if r.status_code != 200:
        return {}
    soup = BeautifulSoup(r.content, "html.parser")
    # Find the specific <td> tag with class "form_label" and text "Onde está:"
    container_div = soup.find("div", {"id": "UltimoAndamento_menos"})
    table = container_div.find("table", class_="form_tabela")
    all_tds = table.find_all("td")

    # organize tags into dict
    d = {}
    for tag in all_tds:
        if tag.attrs["class"] == ["form_label"]:
            label = tag.text
        if tag.attrs["class"] == ["form_value"]:
            d[label] = tag.text
            label = None
    # d['datetime_'] = datetime.datetime.utcnow()
    st.session_state[protocol_number] = True
    return d


async def fetch_protocolo(protocol_number: str):
    try:
        clean_protocol_number = protocol_number.replace("-", "").replace(".", "")
        ds = fetch_data_from_protocol(clean_protocol_number)
        ds['protocolo'] = protocol_number
        return ds
    except Exception as e:
        print(f"Exception occured {protocol_number}", e)
        return {}


async def fetch_all_protocols(protocol_numbers: list[str]):
    print('start')
    L = await asyncio.gather(
        *[fetch_protocolo(i) for i in protocol_numbers]
    )
    return L


def sync_main(protocol_numbers):
    return asyncio.run(fetch_all_protocols(protocol_numbers))
