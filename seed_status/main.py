import requests
import pandas as pd
import sqlalchemy
from bs4 import BeautifulSoup

def fetch_data_from_protocol(protocol_number: str):
    print(f'''Fetching data for {protocol_number}''')
    r = requests.get(f'https://www.eprotocolo.pr.gov.br/spiweb/consultarProtocoloDigital.do?action=pesquisar&numeroProtocolo={protocol_number}',
                     verify=False)
    print(r.status_code)
    # UltimoAndamento_menos > div > table
    soup = BeautifulSoup(r.content, 'html.parser')
    # Find the specific <td> tag with class "form_label" and text "Onde está:"
    container_div = soup.find('div',{"id":'UltimoAndamento_menos'})
    print(container_div)
    table = container_div.find('table', class_='form_tabela')
    all_tds = table.find_all('td')

    # organize tags into dict
    d = {}
    for tag in all_tds:
        if tag.attrs['class'] == ["form_label"]:
            label = tag.text
        if tag.attrs['class'] == ["form_value"]:
            d[label] = tag.text
            label = None

    return d


if __name__ == "__main__":
    protocol_number = '208159500'
    d = fetch_data_from_protocol(protocol_number)
    df = pd.DataFrame.from_records(d, index=range(1))

    engine = sqlalchemy.create_engine('postgresql+psycopg2://nfuyvugl:RtrBNryTfIAaElHY5Odd5SIHLGxXQ3jw@flora.db.elephantsql.com/nfuyvugl')
    df.to_sql(name='projetos',con=engine, if_exists='append')
    print (d)