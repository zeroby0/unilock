import asyncio
import http.client

listeners = [
    {
        'host': '100.117.214.72:49050',
    }
]


async def make_get_request(host, path):
    conn = http.client.HTTPConnection(host)
    conn.request('GET', path)
    response = conn.getresponse()
    content = response.read().decode('utf-8')
    print(content)


async def main():

    while True:
        line = input()  # Read a line from stdin

        if "{'LockedHint': <false>}" in line:
            print("Unlock")

            tasks = [make_get_request(
                listener['host'], '/unlock') for listener in listeners]

            await asyncio.gather(*tasks)

            continue

        if "{'LockedHint': <true>}" in line:
            print("Lock")

            tasks = [make_get_request(listener['host'], '/lock')
                     for listener in listeners]

            await asyncio.gather(*tasks)

            continue

        # Process the line or perform any desired operations
        # For example, you can print the line or store it in a list
        print("Received line:", line)


asyncio.run(main())
