import socket
import asyncio
import os
import secrets
from collections import deque
import json
import logging
import pickle
from pathlib import Path
from config import Config as config


# TODO
"""
1. Send the saved relay status on client connection. DONE
2. Move settings into config.py Config class.
"""

logging.basicConfig(
    format=config.log_format,
    level=config.log_level) # logging.DEBUG
logger = logging.getLogger(__name__)


server, reader, writer = None, None, None
connected_clients = []
message_queue = []


def save_relay_status(new_status):
    if not config.save_path.parent.exists():
        os.mkdir(config.save_path.parent)
        logger.info(f'Created {config.save_path.parent}')
    with open(config.save_path, 'w+b') as saved_status:
            pickle.dump(new_status, saved_status)
            logger.info(f'Updated {config.save_path.name} with {new_status}.')


def get_relay_status():
    try:
        with open(config.save_path, 'rb') as status:
            return pickle.load(status)
    except FileNotFoundError as error:
        default_status = [False for status in range(8)]
        save_relay_status(default_status)
        return default_status


def main():
    loop = asyncio.get_event_loop()

    start_server_task = loop.create_task(start_listening())
    task1 = loop.create_task(message_worker())
    #task2 = loop.create_task(connected_clients_worker(1))
    #task3 = loop.create_task(connected_clients_worker(2))

    all_tasks = asyncio.gather(start_server_task, task1)
    loop.run_until_complete(all_tasks)
    #asyncio.run(start_listening(), debug=True)


async def start_listening():
    global server
    server = await asyncio.start_server(client_connected, config.host, config.port)
    addr = server.sockets[0].getsockname()
    logger.info(f'Server started on {addr[0]}:{addr[1]} with PID {os.getpid()}')
    async with server:
        await server.serve_forever()


async def client_connected(reader, writer):
    addr = writer.get_extra_info('peername')
    global connected_clients
    connected_clients.append(writer)
    logger.info(f'Connected clients {len(connected_clients)}.')
    logger.info(f'Client connected from {addr[0]}:{addr[1]}')
    logger.info('Sending msg.')
    writer.write('Thanks for connecting.'.encode())
    writer.write(str(get_relay_status()).encode())

    data = None
    while data is not b'':
        data = await reader.read(4096)
        logger.info(f'*** {len(data)} bytes received from {addr[0]}:{addr[1]} ***')
        process_data(data)
    
    logger.info(f'Client {addr[0]}:{addr[1]} disconnected.')
    connected_clients.remove(writer)
    writer.close()


def process_data(data):
    #logger.debug(f'Processing {len(data)} bytes.')
    #logger.debug(f'The data: {data.decode()}')
    data_len = len(data)
    processed_len = 0
    fixed_len = 2

    while processed_len < data_len:
        header_len = int.from_bytes(data[processed_len: processed_len + fixed_len], byteorder='big')
        logger.debug(f'Processed header length: {header_len}')

        header_start = processed_len + fixed_len
        header_end = processed_len + fixed_len + header_len
        header = unpack_data(data[header_start:header_end])
        logger.debug(f'Processed header: {header}')

        message_start = processed_len + fixed_len + header_len
        message_end = processed_len + fixed_len + header_len + header['message_length']
        # Check the first 2 bytes for the length of the message header.
        message = unpack_data(data[message_start:message_end])
        logger.debug(f'Processed message: {message}')

        processed_len += fixed_len + header_len + header['message_length']
        logger.debug(f'Processed {processed_len}/{data_len} bytes. Message: {message}')


def unpack_data(data):
    json_header = data.decode()
    return json.loads(json_header)


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
