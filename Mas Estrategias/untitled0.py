# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 12:23:55 2023

@author: fvfentanes
"""

import asyncio
import websockets

async def message():
    async with websockets.connect("ws://localhost:1234") as socket:
        msg = input("Write your message to the server: ")
        await socket.send(msg)
        print(await socket.recv())

asyncio.get_event_loop().run_until_complete(message())