import websockets
import requests
import json

async def challenge_l(message, websocket):
    risposta = requests.post("https://play.pokemonshowdown.com/action.php?",
             data={
                'act': 'login',
                'name': 'Someni',
                'pass': 'SoMany',
                'challstr': message[2] + '%7C' + message[3]
             })
    await websocket.send('|/trn Someni,0,'+json.loads(risposta.text[1:])['assertion'])
    await websocket.send('|/avatar elesa-gen5bw2')

async def challenge(message, websocket):
    risposta = requests.post("https://play.pokemonshowdown.com/action.php?",
             data={
                'act': 'upkeep',
                'challstr': message[2] + '%7C' + message[3]
             })
    #await websocket.send('|/trn Someni,0,'+json.loads(risposta.text[1:])['assertion'])
    await websocket.send('|/avatar elesa-gen5bw2')