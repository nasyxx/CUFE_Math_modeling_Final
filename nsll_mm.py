#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=C0103
# pylint: disable=R0913
"""
@Version: 1
@Author: Nasy, SX, LC, LX
@Date: Jun 12, 2016
@email: sy_n@me.com
@file: nsll_mm.py
@license: MIT

CUFE investment 14 Math Modeling Final Work by 纳赛阳，盛雪，刘畅 & 刘霞

**IMPORTANT**:
    BEFORE YOU USE THIS FILE, PLEASE MAKE SURE YOU HAVE THESE MODEL INSTALLED
    OR IT MAY NOT WORK:
        random, numpy, networkx, plotly, matplotlib, math

To complete recur the experments, just run `python3 nsll_mm.py` in your command
line tool like zsh.

This operation may take over 3000s.
"""
import random

import networkx as nx
import numpy as np
import plotly.offline as py


class nsll_nw():
    """
    This class is the main class of our Final Work.
    ---parameters
    @params n, k, p, i_0, r_0, seed
        n: nodes of the network. Default: 1000
        k: the average degree of the network. Default: 10
        p: the reconnection chance of the network. Default: 0.02947368
        i_0: the initial infected(I). Default: 4
        r_0: the initial rationals(R). Default: 1
        seed: the WS Small-World network seed
    ---attributes
    @attributes ws, s, infected, r
        ws: the WS Small-World network with n, k & p
        s: the susceptible nodes. Use method all_s_i_r() to initial it
        infected: the infected nodes
        r: the rationals nodes
        clustering: the clustering of the network
        betweenness: the centrality betweenness of the network
    ---methods
    @method s_to_i(self, p=3.9)
        This method simulates susceptible to infected one time
    @method s_i_to_r(self, p=5.2)
        This method simulates susceptible or infected to rationals one time
    @method all_s_i_r(self)
        This method rebuilds s, infected and r records
    @method draw_ws_network(self)
        This method draws the network of WeChat Moments with WS Small-World
    """

    def __init__(self, n=1000, k=10, p=0.02947368, i_0=4, r_0=1, seed='nsll'):
        """
        initial the class
        """
        self.ws = nx.watts_strogatz_graph(n, k, p, seed=seed)
        nx.set_node_attributes(self.ws, 'SIR', 'S')
        self.clustering = nx.clustering(self.ws)
        self.betweenness = nx.betweenness_centrality(self.ws)
        self.s = []
        self.r = random.sample(self.ws.nodes(), r_0)
        self.infected = random.sample(self.ws.nodes(), i_0)

        for n in self.infected:
            self.ws.node[n]['SIR'] = 'I'

        for n in self.r:
            self.ws.node[n]['SIR'] = 'R'

    def s_to_i(self, p=3.9):
        """
        @method s_to_i
        """
        for n in self.infected:
            for n2 in self.ws.neighbors(n):
                if self.ws.node[n2]['SIR'] == 'S':
                    if random.random() < (p *
                                          self.clustering[n] *
                                          self.betweenness[n]):
                        self.ws.node[n2]['SIR'] = 'I'

    def s_i_to_r(self, p=5.2):
        """
        @method s_i_to_r
        """
        for n in self.r:
            for n2 in self.ws.neighbors(n):
                if self.ws.node[n2]['SIR'] == 'S':
                    if random.random() < (p *
                                          self.clustering[n] *
                                          self.betweenness[n]):
                        self.ws.node[n2]['SIR'] = 'R'
                elif self.ws.node[n2]['SIR'] == 'I':
                    if random.random() < (p *
                                          self.clustering[n] *
                                          self.betweenness[n]):
                        self.ws.node[n2]['SIR'] = 'R'

    def all_s_i_r(self):
        """
        @method all_s_i_r
        """
        self.s = []
        self.infected = []
        self.r = []
        for n in self.ws.node:
            if self.ws.node[n]['SIR'] == 'S':
                self.s.append(n)
            elif self.ws.node[n]['SIR'] == 'I':
                self.infected.append(n)
            elif self.ws.node[n]['SIR'] == 'R':
                self.r.append(n)

        return {'s': self.s, 'i': self.infected, 'r': self.r}

    def draw_ws_network(self):
        """
        @method draw_ws_network

        You can simply use it any time you like

        The latest network you draw doesn't look like the the last one
        """
        ws = self.ws
        pos = nx.spring_layout(ws)
        # edges data
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
                line=dict(
                    width=0.5,
                )
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
            xaxis=dict(
                showgrid=False,
                zeroline=False,
                showticklabels=False
            ),
            yaxis=dict(
                showgrid=False,
                zeroline=False,
                showticklabels=False
            ),
        )

        fig = dict(
            data=[edge_trace, node_trace],
            layout=layout,
        )
        py.plot(fig, filename='ws_network.html')
        return


def find_p():
    """
    This function is used to find out the 'p' in the WS Small-World we needed.

    You have to run this function first and then find out the 'p' in the plot.

    All of the orginal data we used in the article are set to default.
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
        # average
        a_l[i] = (l_ws[0] + l_ws[1] + l_ws[2] + l_ws[3] + l_ws[4]) / 5
        l_max[i] = max(l_ws) - a_l[i]
        l_min[i] = a_l[i] - min(l_ws)
        l_max[i] = max(l_ws)
        l_min[i] = min(l_ws)
        i += 1

    # Draw Figure
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
                title='平均路径长度',
            ),
        ),
    )
    py.plot(fig, filename='find_p.html')
    return


def draw_sir_prop(a=3.9, b=5.2, text='s_i_r_prop.html', ao=True):
    """
    This function draws the susceptible, infected and rationals proportion
    """
    nsll = nsll_nw()
    s = []
    infected = []
    r = []
    # pylint: disable=W0612
    for __ in range(250):
        nsll.s_to_i(a)
        nsll.s_i_to_r(b)
        sir = nsll.all_s_i_r()
        s.append(len(sir['s']))
        infected.append(len(sir['i']))
        r.append(len(sir['r']))
    # pylint: enable=W0612
    fig = dict(
        data=[
            dict(
                type='scatter',
                y=s,
                x=np.linspace(0, 500, 501),
                mode='lines+markers',
                name='susceptible',
            ),
            dict(
                type='scatter',
                x=np.linspace(0, 500, 501),
                y=infected,
                mode='lines+markers',
                name='infected',
            ),
            dict(
                type='scatter',
                x=np.linspace(0, 500, 501),
                y=r,
                mode='lines+markers',
                name='rationals'
            )
        ],
        layout=dict(font=dict(size=24)),
    )
    py.plot(fig, filename=text, auto_open=ao)


def draw_i_a():
    """
    This function draws I_max of the experment 1

    The A_alpha at beginning is 1.9, at stopping is 5.1. Steps is 0.05
    """
    i_max = []
    for i in np.linspace(1.9, 5.1, 65):
        nsll = nsll_nw()
        s = []
        infected = []
        r = []
        # pylint: disable=W0612
        for __ in range(250):
            nsll.s_to_i(i)
            nsll.s_i_to_r()
            sir = nsll.all_s_i_r()
            s.append(len(sir['s']))
            infected.append(len(sir['i']))
            r.append(len(sir['r']))
        # pylint: enable=W0612

        print(i)
        i_max.append(max(infected))

    z = np.polyfit(np.linspace(1.9, 5.1, 65), i_max, 1)
    f = np.poly1d(z)
    fig = dict(
        data=[
            dict(
                x=np.linspace(1.9, 5.1, 65),
                y=i_max,
                name='I',
                mode='markers',
            ),
            dict(
                x=np.linspace(1.9, 5.1, 65),
                y=f(np.linspace(1.9, 5.1, 65)),
                name='fit',
                mode='lines',
            )
        ],
        layout=dict(
            font=dict(
                size=24
            )
        ),
    )
    py.plot(fig, filename='i_a.html')


def draw_i_b():
    """
    This function draws I_max of the experment 2

    The A_beta at beginning is 5.2, at stopping is 8.4. Steps is 0.05.
    """
    i_max = []
    for i in np.linspace(5.2, 8.4, 65):
        nsll = nsll_nw()
        s = []
        infected = []
        r = []
        # pylint: disable=W0612
        for __ in range(250):
            nsll.s_to_i()
            nsll.s_i_to_r(i)
            sir = nsll.all_s_i_r()
            s.append(len(sir['s']))
            infected.append(len(sir['i']))
            r.append(len(sir['r']))
        # pylint: enable=W0612
        print(i)
        i_max.append(max(infected))
    z = np.polyfit(np.linspace(5.2, 8.4, 65), i_max, 1)
    f = np.poly1d(z)
    fig = dict(
        data=[
            dict(
                x=np.linspace(5.2, 8.4, 65),
                y=i_max,
                name='I',
                mode='markers',
            ),
            dict(
                x=np.linspace(5.2, 8.4, 65),
                y=f(np.linspace(5.2, 8.4, 65)),
                name='fit',
                mode='lines',
            )
        ],
        layout=dict(font=dict(size=24)),
    )
    py.plot(fig, filename='i_b.html')

if __name__ == '__main__':
    print('需要3000s左右整个模拟才能完成，请耐心等待')
    # get p
    find_p()
    # draw WS Small-World network
    nsll_nw().draw_ws_network()
    # draw susceptible, infected and rationals proportion
    draw_sir_prop(3.9, 5.2)
    # experment 1
    for i_1 in np.linspace(1.9, 5.1, 17):
        draw_sir_prop(i_1, 5.2, text='1_' + str(i_1) + '.html', ao=False)
    draw_i_a()
    # experment 2
    for i_2 in np.linspace(5.2, 8.4, 17):
        draw_sir_prop(3.9, i_2, text='2_' + str(i_2) + '.html', ao=False)
    draw_i_b()
