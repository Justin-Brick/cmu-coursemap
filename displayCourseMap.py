# https://plot.ly/python/tree-plots/
import igraph
from igraph import Graph, EdgeSeq
import json

# get courses list
with open('courseAPI.json') as json_file:
    data = json.load(json_file)
    
# get edge list
with open("edges.json") as json_file:
    edge_list_raw = json.load(json_file)
edges_list = []
for edge in edge_list_raw:
    edges_list.append(tuple(edge))

# store data
course_data = data.pop("courses")
course_names = list(course_data.keys())
#edges_list = [("15-122", "15-150"), ("15-150", "15-210"), ("15-112", "15-122"), ("15-110", "15-122")]

# user-defined variables
depth = 2 # how far to explore in the course map
toSearch = "15-251" # the course to search for

''' TRIMMING THE DATA '''
focus = set([toSearch]) # the final list of vertices, trimmed
focus_edges = set([]) # the final list of edges, trimmed

# trim edge list
forwardSearch = [toSearch]
backwardSearch = [toSearch]

for i in range(depth):
    forwardAdjacencies = []
    backwardAdjacencies = []
    for (c1, c2) in edges_list:
        if (c1 in forwardSearch):
            focus_edges.add((c1, c2))
            forwardAdjacencies.append(c2)
            focus.add(c1)
            focus.add(c2)
        if (c2 in backwardSearch):
            focus_edges.add((c1, c2))
            backwardAdjacencies.append(c1)
            focus.add(c1)
            focus.add(c2)
    forwardSearch += list(set(forwardAdjacencies) - set(forwardSearch))
    backwardSearch += list(set(backwardAdjacencies) - set(backwardSearch))

# revert to lists
focus = list(focus)
focus_edges = list(focus_edges)

''' GENERATE THE GRAPH AND PLOT '''
nr_vertices = len(focus)
v_label = focus
G = Graph()
G.add_vertices(focus)
G.add_edges(focus_edges)
lay = G.layout('rt')

position = {k: lay[k] for k in range(nr_vertices)}
Y = [lay[k][1] for k in range(nr_vertices)]
M = max(Y)

es = EdgeSeq(G) # sequence of edges
E = [e.tuple for e in es] # list of edges

L = len(position)
Xn = [position[k][0] for k in range(L)]
Yn = [2*M-position[k][1] for k in range(L)]
Xe = []
Ye = []
for edge in E:
    Xe+=[position[edge[0]][0],position[edge[1]][0], None]
    Ye+=[2*M-position[edge[0]][1],2*M-position[edge[1]][1], None]

labels = focus

import plotly.graph_objects as go
fig = go.Figure()
fig.add_trace(go.Scatter(x=Xe,
                   y=Ye,
                   mode='lines',
                   line=dict(color='rgb(210,210,210)', width=1),
                   hoverinfo='none'
                   ))
fig.add_trace(go.Scatter(x=Xn,
                  y=Yn,
                  mode='markers',
                  name='bla',
                  marker=dict(symbol='circle-dot',
                                size=50,
                                color='#6175c1',    #'#DB4551',
                                line=dict(color='rgb(50,50,50)', width=1)
                                ),
                  text=labels,
                  hoverinfo='text',
                  opacity=0.8
                  ))

def make_annotations(pos, text, font_size=10, font_color='rgb(250,250,250)'):
    L=len(pos)
    if len(text)!=L:
        raise ValueError('The lists pos and text must have the same len')
    annotations = []
    for k in range(L):
        annotations.append(
            dict(
                text=labels[k], # or replace labels with a different list for the text within the circle
                x=pos[k][0], y=2*M-position[k][1],
                xref='x1', yref='y1',
                font=dict(color=font_color, size=font_size),
                showarrow=False)
        )
    return annotations


axis = dict(showline=False, # hide axis line, grid, ticklabels and  title
            zeroline=False,
            showgrid=False,
            showticklabels=False,
            )

fig.update_layout(title= 'Tree with Reingold-Tilford Layout',
              annotations=make_annotations(position, v_label),
              font_size=12,
              showlegend=False,
              xaxis=axis,
              yaxis=axis,
              margin=dict(l=40, r=40, b=85, t=100),
              hovermode='closest',
              plot_bgcolor='rgb(248,248,248)'
              )
fig.show()
