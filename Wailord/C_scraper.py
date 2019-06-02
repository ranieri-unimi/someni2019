import os
import io
import fnmatch

data_base = 'results/'+input('Dove vuoi appendere? ')+'.psv'
db = open(data_base, 'a')

for lf in fnmatch.filter(os.listdir('battles/'), '*.txt'):
    log_name = 'battles/'+lf

    file = io.open(log_name, mode="r", encoding="utf-8")
    battle_log = file.read().split('|')
    file.close()
    
    one_team = set() #battle_log[11] è ONE
    two_team = set() #battle_log[15] è TWO
    tie = False

    for i in range(len(battle_log)):
        if battle_log[i][:5] == 'p1a: ':
            one_team.add(battle_log[i][5:])
        if battle_log[i][:5]== 'p2a: ':
            two_team.add(battle_log[i][5:])
        if battle_log[i] == 'win':
            one_has_won = (battle_log[i+1] == battle_log[11])
        if (battle_log[i] == 'tie') or ('lost due to inactivity' in str(battle_log[i])):
            tie = True
        if battle_log[i] == 'turn':
            turns = battle_log[i+1]

    p1 = list(one_team)
    p2 = list(two_team)
    if not tie:
        for i in range(len(p1)-1):
            for j in range(i+1,len(p1)):
                db.write('{}|{}|{}|{}\n'.format(p1[i], p1[j], one_has_won,turns))
    
        for i in range(len(p2)-1):
            for j in range(i+1,len(p2)):
                db.write('{}|{}|{}|{}\n'.format(p2[i], p2[j], not one_has_won,turns))

        print('# Removing '+ lf)
        os.remove(log_name)
        
    

db.close()
print('## DONE ##')