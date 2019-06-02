import websockets
import asyncio
import json
import login
import queue
import time
import io

async def run(battle_list):
    server_str = 'ws://sim.smogon.com:8000/showdown/websocket'
    await asyncio.sleep(12) #Partenza ritardata

    async with websockets.connect(server_str) as wsc:

        id_battle = battle_list.get(True)
        await wsc.send('|/join '+id_battle)

        while True:
            message = str(await wsc.recv()).replace('\n','').split('|')

            #LOGIN
            if message[1] == 'challstr':
                await login.challenge(message, wsc)
            #BATTLE LOG
            if message[1] == 'init' and message[2] == 'battle':
                finished = False
                for i in range(25):
                    if (message[-i] in ['win', 'tie']) and (message[-i-1] == ''):
                        finished = True
                        f = io.open('battles/'+id_battle+'.txt','a',encoding='utf8')
                        for e in message:
                            f.write(e+'|')
                        f.close()
                if not finished:
                    battle_list.put(id_battle)

            #Change Battle-Room
            if message[1] == 'noinit' or message[1]=='init':
                await wsc.send('|/leave '+str(id_battle))
                await asyncio.sleep(2)
                id_battle = battle_list.get()
                await wsc.send('|/join '+str(id_battle))
                await asyncio.sleep(2)