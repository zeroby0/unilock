import time
import asyncio
import http.client


listeners = [
    # Delete this line and
    # add IPs of your listeners here.
    '100.117.214.72',
]


async def make_get_request(host, path, retry_count=5):

    if retry_count == 0:
        print("EXCEPTION: Number or retries exceeded.")
        return

    # If port is not defined, use
    # default port 49050
    if ':' not in host:
        host = host + ':49050'

    conn = http.client.HTTPConnection(host)

    try:
        conn.request('GET', path)
    except ConnectionError:
        print("Connection error. Will retry after 100 ms.")

        time.sleep(0.01)
        return await make_get_request(host, path, retry_count-1)
    
    response = conn.getresponse()
    content = response.read().decode('utf-8')
    print(content)


async def main():

    while True:
        line = input()  # Read a line from stdin

        if "{'LockedHint': <false>}" in line:
            print("Unlock")

            tasks = [make_get_request(
                listener, '/unlock') for listener in listeners]

            await asyncio.gather(*tasks)

            continue

        if "{'LockedHint': <true>}" in line:
            print("Lock")

            tasks = [make_get_request(
                listener, '/lock') for listener in listeners]

            await asyncio.gather(*tasks)

            continue


asyncio.run(main())
