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
import numpy as np
import plotly.offline as py


def main():
    """
    main function
    """
    p = np.linspace(0.02, 0.04, num=20)
    l_max = [0] * 20
    l_min = [0] * 20
    a_l = [0] * 20
    i = 0
    for p_i in p:
        ws = l_ws = [0] * 5
        ws[0] = nx.watts_strogatz_graph(1000, 10, p_i, seed='nsll')
        ws[1] = nx.watts_strogatz_graph(1000, 10, p_i, seed='nsll1')
        ws[2] = nx.watts_strogatz_graph(1000, 10, p_i, seed='nsll2')
        ws[3] = nx.watts_strogatz_graph(1000, 10, p_i, seed='nsll3')
        ws[4] = nx.watts_strogatz_graph(1000, 10, p_i, seed='nsll4')
        l_ws[0] = nx.average_shortest_path_length(ws[0])
        l_ws[1] = nx.average_shortest_path_length(ws[1])
        l_ws[2] = nx.average_shortest_path_length(ws[2])
        l_ws[3] = nx.average_shortest_path_length(ws[3])
        l_ws[4] = nx.average_shortest_path_length(ws[4])

        a_l[i] = (l_ws[0] + l_ws[1] + l_ws[2] + l_ws[3] + l_ws[4]) / 5
        l_max[i] = max(l_ws) - a_l[i]
        l_min[i] = a_l[i] - min(l_ws)
        l_max[i] = max(l_ws)
        l_min[i] = min(l_ws)
        i += 1
    # print(a_l)
    # print(l_max)
    # print(l_min)
    fig = dict(
        data=[
            dict(
                type='scatter',
                x=p,
                y=l_max,
                mode='lines',
                line=dict(
                    shape='spline',
                    width=0,
                ),
                name='max',
                showlegend=False,
            ),
            dict(
                type='scatter',
                x=p,
                y=a_l,
                mode='lines',
                line=dict(
                    shape='spline',
                ),
                name='平均路径长度',
                fill='tonexty',
                fillcolor='rgba(0,176,246,0.2)',
                # error_y=dict(
                #     type='data',
                #     symmetric=False,
                #     array=l_max,
                #     arrayminus=l_min,
                # ),
            ),
            dict(
                type='scatter',
                x=p,
                y=l_min,
                mode='lines',
                line=dict(
                    shape='spline',
                    width=0,
                ),
                name='error area',
                fill='tonexty',
                fillcolor='rgba(0,176,246,0.2)',
            ),
        ],
        layout=dict(
            font=dict(
                size=24,
            ),
            xaxis=dict(
                title='p',
            ),
            yaxis=dict(
                title='平均路径长度'
            ),
        ),
    )
    py.plot(fig, filename='03.html')


if __name__ == '__main__':
    main()
