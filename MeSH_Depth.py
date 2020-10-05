'''
This builds a dataframe and a hierarchical tree from MeSH terms. Functions to support finding distance between nodes
'''

import pandas as pd
from treelib import Node, Tree
import numpy as np

# Top level terms entered manually because they are not included in headings xlsx
top_terms = ['Anatomy', 'Organisms', 'Diseases', 'Chemicals and Drugs', 'Analytical, Diagnostic and Therapeutic Techniques, and Equipment',
             'Psychiatry and Psychology', 'Phenomena and Processes', 'Disciplines and Occupations',
             'Anthropology, Education, Sociology, and Social Phenomena', 'Technology, Industry, and Agriculture', 'Humanities',
             'Information Science', 'Named Groups', 'Health Care', 'Publication Characteristics', 'Geographicals']

locations = ['A', 'B', 'C', 'D', 'E', 'F', 'G',
             'H', 'I', 'J', 'K', 'L', 'M', 'N', 'V', 'Z']
top_locations = [[loc] for loc in locations]

top_df = pd.DataFrame({
    "Location": top_locations,
    "Term": top_terms
})

headings_df = pd.read_csv('MeSH_headings.csv')

# function for stratifying location strings


def parse_location(location):
    top_char = [str(location)[0]]
    loc_list = str(location).lstrip('ABCDEFGHIJKLMNVZ')
    loc_list = loc_list.split('.')
    return top_char + loc_list


headings_df['Location'] = headings_df['Location'].apply(
    parse_location)  # apply to df

# add headings to df of top level headings and reset index
mesh_df = top_df.append(headings_df)


# depth as measured as num of edges from the top
mesh_df['Depth'] = mesh_df['Location'].apply(lambda location: len(location))
mesh_df = mesh_df.sort_values('Depth').reset_index()
del mesh_df['index']

# convert to np array for speed, test with first 100 entries
mesh_np = mesh_df.to_numpy()

tree = Tree()  # make tree object
tree.create_node("Root", "root")  # make a root node

# loop through entries to make nodes
for row in mesh_np:
    location = row[0]
    term = row[1]
    node_id = '.'.join(location)  # node id is concatenated string of locations

    # if directly under root node, use specific parent node settings
    if len(location) == 1:
        tree.create_node(term, node_id, parent='root')
    else:
        # parent node id is node_id minus current current location level
        parent = '.'.join(location[:-1])
        tree.create_node(term, node_id, parent=parent)

# use nodes to calculate complexity of each node's subtree

# function to find number of nodes in subtree given a node location (includes original node)


def subtree_complexity(entry):
    loc = '.'.join(list(entry))
    return len(tree.subtree(loc).nodes)


mesh_df['Complexity'] = mesh_df['Location'].apply(
    subtree_complexity)  # write complexity values to a new column
