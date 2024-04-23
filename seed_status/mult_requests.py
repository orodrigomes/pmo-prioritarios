import asyncio
import time

from joblib import Memory

location = "./cachedir"
memory = Memory(location, verbose=0)
import httpx

from seed_status.streamlit_utils import extract_response_dict

start_time = time.time()

protocolos = [
    "15.806.973-3",
    "21.036.047-6",
    "21.039.950-0",
    "21.045.230-3",
    "21.059.664-0",
    "21.088.294-4",
    "21.171.445-0",
    "21.177.376-6",
    "21.450.060-4",
]

cachedir = "./"
memory = Memory(cachedir, verbose=0)


# @streamlit.cache_data(ttl=3600, persist=True)
@memory.cache
async def fetch_data_from_protocol_site(client, url, protocol_number: int):
    print(f"fetching data for {protocol_number}")

    resp = await client.get(url)
    content = resp.content
    try:
        return extract_response_dict(content, protocol_number)
    except:
        print(f"problem with protocol {protocol_number}")
        return {}


async def fetch_protocols_async(protocol_numbers: list[int]):
    async with httpx.AsyncClient(verify=False) as client:
        tasks = []
        for protocol_number in protocol_numbers:
            url = f"https://www.eprotocolo.pr.gov.br/spiweb/consultarProtocoloDigital.do?action=pesquisar&numeroProtocolo={protocol_number}"
            tasks.append(
                asyncio.ensure_future(
                    fetch_data_from_protocol_site(client, url, protocol_number)
                )
            )

        all_data = await asyncio.gather(*tasks)
        return [i for i in all_data]

# asyncio.run(fetch_protocols_async())
# print("--- %s seconds ---" % (time.time() - start_time))
