import networkx as nx
import io
import json

#Dizionario dei tipi in inglese
type_dict = {
    'Normal':False,
    'Fighting':False,
    'Flying':False,
    'Poison':False,
    'Ground':False,
    'Rock':False,
    'Bug':False,
    'Ghost':False,
    'Steel':False,
    'Fire':False,
    'Water':False,
    'Grass':False,
    'Electric':False,
    'Psychic':False,
    'Ice':False,
    'Dragon':False,
    'Dark':False,
    'Fairy':False
    }

#Aggiusta l'array strippato e stringato
def stringify(arr):
    for i in range(len(arr)):
        arr[i] = str(arr[i]).strip()
    return arr

#Imposta il File GEPHI con il control-char selezionato
def choosen_weight(edge, x):
    if x == 'v':
        return edge['won']
    elif x == 'p':
        return edge['won']/edge['count']
    elif x == 't':
        return edge['turns']
    elif x == 'c':
        return edge['count']
    else:
        return 1.0


print('# Initializing files...')

#OPEN
db = open('results/'+input('Quale PSV converto? ')+'.psv', 'r')
lista_linee = db.readlines()
db.close()

#Create NODES
coopokemon = nx.Graph()
for pokemon in json.loads(io.open('externals/pokedex-abs.json', mode="r", encoding="utf-8").read()):
    #ATT: Type
    attributi = type_dict.copy()
    for ty in pokemon['type']:
        attributi[ty] = True
    #ATT: Stats
    attributi.update(pokemon['base'])

    #Crea nodo
    coopokemon.add_node(pokemon['name']['english'], **attributi)


#Create EDGES
for linea in lista_linee:
    r = stringify(linea.split('|'))
    if coopokemon.has_edge(r[0],r[1]):
        if r[2] == 'True':
            dict = 'won'
        else:
            dict = 'los'
        coopokemon[r[0]][r[1]][dict] += 1
        coopokemon[r[0]][r[1]]['turns'] += int(r[3])
    else:
        if r[2] == 'True':
            coopokemon.add_edge(r[0],r[1],won=1,los=0, turns=int(r[3]))
        else:
            coopokemon.add_edge(r[0],r[1],won=0,los=1, turns=int(r[3]))

#Add other lables to EDGES
for e in list(coopokemon.edges):
    coopokemon.edges[e]['count'] = coopokemon.edges[e]['won']+coopokemon.edges[e]['los']
    coopokemon.edges[e]['rate'] = int(100*coopokemon.edges[e]['won']/coopokemon.edges[e]['count'])

    coopokemon.edges[e]['weight'] = pow(choosen_weight(coopokemon.edges[e], 't'), 1)

#WRITE
nx.write_gexf(coopokemon, 'gephi/'+input('Nome del GEXF? ')+'.gexf')

print('## DONE ##')