import websockets
import asyncio
import json
import login
import queue

async def run(battle_list, elo):
    query_str = '|/cmd roomlist gen7randombattle, '+str(elo)
    server_str = 'ws://sim.smogon.com:8000/showdown/websocket'
    bef = set()

    async with websockets.connect(server_str) as wsp:
        await wsp.send(query_str)

        while True:
            message = str(await wsp.recv()).split('|')

            #LOGIN
            if message[1] == 'challstr':
                await login.challenge(message, wsp)
            #QUERY LOTTE ATTIVE
            elif message[1] == 'queryresponse':

                nex = set(json.loads(message[3])['rooms']) #da DICT a SET si perdono i VALUE 
                for i in nex.difference(bef):
                    battle_list.put(i)
                bef = nex.copy()

                await wsp.send(query_str)
                await asyncio.sleep(7)
            #DEBG
            else:
                print('Unexpected response:',message[1])