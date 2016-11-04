import os
import random
import csv

ssns = []

def parse_generator(first, last, lid, tid):

    ssn = first[0] + last[0]
    for i in range(0,9):
        ssn += str(random.randint(0,9))
    ssn = "'"+ssn+"'"
    ssns.append(ssn)
    salary = str(random.randint(1000000,30000000))

    return 'INSERT INTO Pay_Born_Emp VALUES('+ssn+",'"+tid+"',"+lid+','+salary+','+"'"+first+ ' ' + last+"'"+');'

def player_generator(first, last, lid, tid,id):
    ssn = ssns[id]
    return 'INSERT INTO Player VALUES('+ssn+','+str(random.randint(1,8))+',filler,age);'

def perf_generator(first, last, lid, tid,id):
    ssn = ssns[id]
    points = random.randint(1,35)
    assists = random.randint(1,12)
    rebounds = random.randint(0,6)
    three_points = random.randint(0,4)*3
    return 'INSERT INTO Performance VALUES('+ssn+",'16-17',"+str(points)+','+str(assists)+','+str(rebounds)+','+str(three_points)+');'

with open('Add_to_Player.csv','rU') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print parse_generator(row['first'],row['last'],row['lid'],row['tid'])

with open('Add_to_Player.csv', 'rU') as csvfile:
    reader = csv.DictReader(csvfile)
    i = 0
    for row in reader:
        print player_generator(row['first'],row['last'],row['lid'],row['tid'],i)
        i = i + 1

with open('Add_to_Player.csv', 'rU') as csvfile:
    reader = csv.DictReader(csvfile)
    i = 0
    for row in reader:
        print perf_generator(row['first'],row['last'],row['lid'],row['tid'],i)
        i = i + 1