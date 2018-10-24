import socket
import asyncio


HOST = '127.0.0.1'
PORT = 2018


def main():
    asyncio.run(start_listening())

async def start_listening():
    server = await asyncio.start_server(client_connected, HOST, PORT)
    addr = server.sockets[0].getsockname()
    print(f'Server started on {addr}')

    async with server:
        await server.serve_forever()


async def client_connected(reader, writer):
    data = await reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info('peername')
    print('Message received!')
    print(f'{message!r}, From: {addr}')


if __name__ == '__main__':
    main()
