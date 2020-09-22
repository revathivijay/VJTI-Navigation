import pandas as pd
import numpy as np
import json
import csv

def create_nodes(input_file, output_file):
    """
    Function to create Nodes of the graph
    Input: input_file : ".csv" format file
        columns in the file:
            1. Node name (Will be blank for minor nodes)
            2. x_pos (x coordinate in grid)
            3. y_pos (y coordinate in grid)
            4. Type (Major/Minor) (not actually reqd)
            5. Floor (0,1,2,3)
            6. Building (If any building associated)
            7. Map number (To map coordinate)
    Returns json file of the format : {Node# : {Node details}}
    """
    ## for temporary storage of csv data
    data = {}

    ## read csv data into dictionary
    with open(input_file, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            id = row['Node number']
            data[id] = row
    ## dump dictionary data to json file
    with open(output_file, 'w') as json_file:
        json_file.write(json.dumps(data, indent=4))

## driver code
if __name__=='__main__':
    create_nodes('nodes.csv', 'nodes.json')
