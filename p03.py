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
import random

import networkx as nx
import numpy as np
import plotly.offline as py


class Netw:
    """
    network class
    """

    def __init__(self, n=1000, k=10, p=0.02947368):
        self.n = n
        self.k = k
        self.p = p
        self.ws = nx.watts_strogatz_graph(self.n, self.k, self.p, seed='nsll')
        nx.set_node_attributes(self.ws, 'SIR', 'S')
        self.clustering = nx.clustering(self.ws)
        self.betweenness = nx.betweenness_centrality(self.ws)
        p_r_0 = 0.001
        r_0 = int(self.n * p_r_0)
        if r_0 < 1:
            r_0 = 1
        random.seed('nsll')
        self.r = random.sample(self.ws.nodes(), r_0)

        i_0 = 4
        if i_0 < r_0:
            i_0 += 1
        random.seed('nsll')
        self.infected = random.sample(self.ws.nodes(), i_0)
        for n in self.infected:
            self.ws.node[n]['SIR'] = 'I'
        for n in self.r:
            self.ws.node[n]['SIR'] = 'R'
        self.s = self.n - len(self.infected) - len(self.r)
        print(self.r)
        print(self.infected)

    def s_to_i(self, p=3.9):
        """
        s_to_i_to_r function
        """

        for n in self.infected:
            for n2 in self.ws.neighbors(n):
                if self.ws.node[n2]['SIR'] == 'S':
                    if random.random() < p * self.clustering[n] * self.betweenness[n]:
                        self.ws.node[n2]['SIR'] = 'I'

    def s_i_to_r(self, p=5.2):
        """
        s_i_to_r function
        """

        for n in self.r:
            for n2 in self.ws.neighbors(n):
                if self.ws.node[n2]['SIR'] == 'S':
                    if random.random() < p * self.clustering[n] * self.betweenness[n]:
                        self.ws.node[n2]['SIR'] = 'R'
                elif self.ws.node[n2]['SIR'] == 'I':
                    if random.random() < p * self.clustering[n] * self.betweenness[n]:
                        self.ws.node[n2]['SIR'] = 'R'

    def all_s_i_r(self):
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


def main():
    """
    main function
    """
    netw_1 = Netw()
    s = []
    infected = []
    r = []

    # netw_11 = Netw(p=0.02945)
    # s1 = []
    # infected1 = []
    # r1 = []
    # netw_12 = Netw(p=0.02946)
    # s2 = []
    # infected2 = []
    # r2 = []

    # i_max = []
    # for i in np.linspace(5.2, 8.4, 65):
    #     netw_1 = Netw()
    #     s = []
    #     infected = []
    #     r = []
    #     for __ in range(250):
    #         netw_1.s_to_i()
    #         netw_1.s_i_to_r(i)
    #         sir = netw_1.all_s_i_r()
    #         s.append(len(sir['s']))
    #         infected.append(len(sir['i']))
    #         r.append(len(sir['r']))
    #     print(i)
    #     i_max.append(max(infected))

    for __ in range(250):
        netw_1.s_to_i(3.9)
        netw_1.s_i_to_r(5.2)
        sir = netw_1.all_s_i_r()
        s.append(len(sir['s']))
        infected.append(len(sir['i']))
        r.append(len(sir['r']))

    # for i in range(250):
    #     netw_11.s_to_i()
    #     netw_11.s_i_to_r()
    #     sir = netw_11.all_s_i_r()
    #     s1.append(len(sir['s']))
    #     infected1.append(len(sir['i']))
    #     r1.append(len(sir['r']))
    # for i in range(250):
    #     netw_12.s_to_i()
    #     netw_12.s_i_to_r()
    #     sir = netw_12.all_s_i_r()
    #     s2.append(len(sir['s']))
    #     infected2.append(len(sir['i']))
    #     r2.append(len(sir['r']))

    # print([s, infected, r])

    # z = np.polyfit(np.linspace(5.2, 8.4, 65), i_max, 1)
    # f = np.poly1d(z)
    # yhat = f(np.linspace(5.2, 8.4, 65))
    # ybar = np.sum(i_max) / len(i_max)
    # ssreg = np.sum((yhat - ybar)**2)
    # sstot = np.sum((i_max - ybar)**2)
    # print(ssreg / sstot)
    # fig = dict(
    #     data=[
    #         dict(
    #             x=np.linspace(5.2, 8.4, 65),
    #             y=i_max,
    #             name='I',
    #             mode='markers',
    #         ),
    #         dict(
    #             x=np.linspace(5.2, 8.4, 65),
    #             y=f(np.linspace(5.2, 8.4, 65)),
    #             name='fit',
    #             mode='lines',
    #         )
    #     ],
    #     layout=dict(font=dict(size=24)),
    # )
    # py.plot(fig, filename='06.html')

    fig = dict(
        data=[
            dict(
                y=s,
                x=np.linspace(0, 500, 501),
                mode='markers',
                # line=dict(shape='spline'),
            ),
            dict(
                x=np.linspace(0, 500, 501),
                y=infected,
                mode='markers',
                # line=dict(shape='spline'),
            ),
            dict(
                x=np.linspace(0, 500, 501),
                y=r,
                mode='markers',
                # line=dict(shape='spline'),
            )
        ]
    )
    py.plot(fig, filename='04.html')

    #
    # fig = dict(
    #     data=[
    #         dict(
    #             y=np.array(infected) + np.array(r),
    #             x=np.linspace(0, 500, 501),
    #             mode='lines+markers',
    #             name='实验',
    #             marker=dict(
    #                 symbol='x',
    #                 # size=20,
    #             ),
    #             line=dict(shape='spline', color='black'),
    #         ),
    #         dict(
    #             x=np.linspace(0, 500, 501),
    #             y=np.array(infected1) + np.array(r1),
    #             mode='lines+markers',
    #             name='实际数据1',
    #             marker=dict(
    #                 symbol='o',
    #                 # size=20,
    #             ),
    #             line=dict(shape='spline', color='black'),
    #         ),
    #         dict(
    #             x=np.linspace(0, 500, 501),
    #             y=np.array(infected2) + np.array(r2),
    #             mode='lines+markers',
    #             name='实际数据2',
    #             marker=dict(
    #                 symbol='.',
    #                 # size=20,
    #             ),
    #             line=dict(shape='spline', color='black'),
    #         )
    #     ],
    #     layout=dict(
    #         font=dict(size=24),
    #     ),
    # )
    #
    # py.plot(fig, filename='05.html')

if __name__ == '__main__':
    main()
