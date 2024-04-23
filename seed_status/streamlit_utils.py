from bs4 import BeautifulSoup


def extract_response_dict(content: bytes, protocol_number: int):
    soup = BeautifulSoup(content, "html.parser")
    # Find the specific <td> tag with class "form_label" and text "Onde está:"
    container_div = soup.find("div", {"id": "UltimoAndamento_menos"})
    table = container_div.find("table", class_="form_tabela")
    all_tds = table.find_all("td")

    # organize tags into dict
    d = {}
    d["protocol_number"] = protocol_number
    for tag in all_tds:
        if tag.attrs["class"] == ["form_label"]:
            label = tag.text
        if tag.attrs["class"] == ["form_value"]:
            d[label] = tag.text
            label = None

    return d
