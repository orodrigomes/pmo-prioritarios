import requests
from bs4 import BeautifulSoup


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

    return d
