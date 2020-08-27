import csv

def create_nodes(input_file):

    adj_list = {}

    with open(input_file, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            try:
                adj_list[row['Node ']].add(row['Adjacents'])
            except KeyError:
                adj_list[row['Node ']] = {row['Adjacents']}
            try:
                adj_list[row['Adjacents']].add(row['Node '])
            except KeyError:
                adj_list[row['Adjacents']] = {row['Node ']}

    return adj_list
