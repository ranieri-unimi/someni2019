import asyncio
import A_produttore as produttore
import B_consumatore as consumatore
import queue
import datetime
import time
global battle_list

battle_list = queue.Queue()

async def status():
    await asyncio.sleep(23)
    low, hig = battle_list.qsize(), battle_list.qsize()
    while True:
        x = battle_list.qsize()
        if x not in range(low, hig+1):
            print(low,':',hig,' ',datetime.datetime.now().strftime('%H:%M'))
        low = min(low, x)
        hig = max(hig, x)
        await asyncio.sleep(13)


elo = input('ELO? ')
processi = [
    asyncio.ensure_future(produttore.run(battle_list, elo)),
    asyncio.ensure_future(consumatore.run(battle_list)),
    asyncio.ensure_future(consumatore.run(battle_list)),
    asyncio.ensure_future(status())
    ]
x = asyncio.gather(*processi)
y = asyncio.get_event_loop()
y.run_until_complete(x)
