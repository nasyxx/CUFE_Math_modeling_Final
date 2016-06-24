#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=C0103

"""
@Version: 1
@Author: Nasy, SX, LC, LX
@Date: Jun 12, 2016
@email: sy_n@me.com
@file: p01.py
@license: MIT

CUFE investment 14 Math Modeling
"""
import networkx as nx
import plotly.offline as py


def main():
    """
    main function
    """
    # watts-strogatz small world
    ws = nx.watts_strogatz_graph(1000, 10, 0.02947368, seed='nsll')
    pos = nx.spring_layout(ws)
    print(nx.average_shortest_path_length(ws))
    print(nx.info(ws))
    # get the position of the node near center(0.5, 0.5)
    # dmin = 1
    # ncenter = 0
    # for n in pos:
    #     x, y = pos[n]
    #     d = (x - 0.5)**2 + (y - 0.5)**2
    #     if d < dmin:
    #         ncenter = n
    #         dmin = d
    # p_nc = nx.single_source_shortest_path_length(ws, ncenter)
    # plot data p
    # edge data
    edge_trace = dict(
        type='scatter',
        x=[],
        y=[],
        line=dict(
            width=0.1,
            color='#333',
        ),
        hoverinfo='none',
        mode='lines',
    )

    for edge in ws.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace['x'] += [x0, x1, None]
        edge_trace['y'] += [y0, y1, None]

    # node data
    node_trace = dict(
        type='scatter',
        x=[],
        y=[],
        mode='markers',
        hoverinfo='none',
        marker=dict(
            size=2,
            line=dict(width=0.5)
        ),
    )

    for node in ws.nodes():
        x_node, y_node = pos[node]
        node_trace['x'].append(x_node)
        node_trace['y'].append(y_node)

    # layout
    layout = dict(
        title='朋友圈 WS network',
        showlegend=False,
        width=900,
        height=950,
        hovermode='closest',
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    )
    fig = dict(
        data=[edge_trace, node_trace],
        layout=layout,
    )
    py.plot(fig, filename='01.html')

if __name__ == '__main__':
    main()
