import socket
import asyncio
import os
import secrets
from collections import deque


HOST = '127.0.0.1'
PORT = 2018

server, reader, writer = None, None, None
connected_clients = []
message_queue = []


def main():
    loop = asyncio.get_event_loop()

    start_server_task = loop.create_task(start_listening())
    task1 = loop.create_task(message_worker())
    task2 = loop.create_task(connected_clients_worker(1))
    task3 = loop.create_task(connected_clients_worker(2))

    all_tasks = asyncio.gather(start_server_task, task1, task2, task3)
    loop.run_until_complete(all_tasks)
    #asyncio.run(start_listening(), debug=True)


async def start_listening():
    global server
    server = await asyncio.start_server(client_connected, HOST, PORT)
    addr = server.sockets[0].getsockname()
    print(f'Server started on {addr} with PID {os.getpid()}')

    async with server:
        await server.serve_forever()


async def client_connected(reader, writer):
    addr = writer.get_extra_info('peername')
    global connected_clients
    connected_clients.append(writer)
    print(f'Connected clients {len(connected_clients)}.')
    print(f'Client connected with address {addr}')
    print('Sending msg.')
    writer.write('Thanks for connecting.'.encode())

    data = None
    while data is not b'':
        data = await reader.read(100)
        message = data.decode()
        print(f'Message received! {message}, From {addr}')
    
    print('Client disconnected.')
    connected_clients.remove(writer)
    writer.close()


async def connected_clients_worker(worker):
    global message_queue
    while True:
        if len(connected_clients) >= 1:
            data = secrets.token_hex(4)
            message_queue.append(f'{worker} {data}.')
            print(f'messages {len(message_queue)} worker {worker}')
        await asyncio.sleep(5)


async def message_worker():
    global message_queue
    while True:
        if len(connected_clients) >= 1 and len(message_queue) >= 1:
            for message in message_queue:
                for writer in connected_clients:
                    print(f'Message sent from worker {message}')
                    writer.write(message.encode())
                    await asyncio.sleep(0.01)
            message_queue = []
        await asyncio.sleep(1)


if __name__ == '__main__':
    main()
