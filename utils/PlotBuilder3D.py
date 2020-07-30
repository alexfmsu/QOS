# ---------------------------------------------------------------------------------------------------------------------
# scientific
# import pandas as pd
import numpy as np
# ---------------------------------------------------------------------------------------------------------------------
# plotly
import plotly.graph_objs as go
import plotly
# ---------------------------------------------------------------------------------------------------------------------
# PyQuantum.Tools
from utils._assert import *
# ---------------------------------------------------------------------------------------------------------------------
# warnings
import warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)
# ---------------------------------------------------------------------------------------------------------------------


class PlotBuilderData3D:

    def __init__(self, args):
        required_args = [
            'title',
            'width', 'height',
            'x', 'y', 'z',
            'ticks',
        ]

        for i in required_args:
            Assert(i in args, i + ' not in args')

        self.width = args['width']
        self.width = int(self.width)
        Assert(self.width > 0 and self.width <= 1200, str(self.width) + ' not in (0, 1200]')

        self.height = args['height']
        self.height = int(self.height)
        Assert(self.height > 0 and self.height <= 800, str(self.height) + ' not in (0, 800]')

        # title
        self.title = args['title']

        # x, y, z
        self.x = args['x']
        self.y = args['y']
        self.z = args['z']

        # self.x_ticktext = self.x['data']
        self.x_tickvals = self.x['data']

        # self.y_ticktext = self.y['data']
        self.y_tickvals = self.y['data']

        self.t_coeff = 1

        self.ticks = args['ticks']

        self.to_file = None
        if 'to_file' in args:
            self.to_file = args['to_file']

        self.showlegend = None
        if 'showlegend' in args:
            self.showlegend = args['showlegend']

        for arg in ['title', 'data']:
            Assert(arg in self.x, '\'' + arg + '\' not in \'y\'')
            Assert(arg in self.y, '\'' + arg + '\' not in \'y\'')
            Assert(arg in self.z, '\'' + arg + '\' not in \'y\'')

        if 'scale' not in self.x:
            self.x['scale'] = 1
        if 'scale' not in self.y:
            self.y['scale'] = 1
        if 'scale' not in self.z:
            self.z['scale'] = 1

    def prepare(self):
        # -------------------------- X --------------------------
        self.x['tickvals'] = self.x['data']
        # self.x['ticktext'] = [''] * len(self.x['ticktext'])

        # if 'dtick' in self.x:
        #     t0 = 0
        #     x_dtick = self.x['dtick']

        #     while t0 < self.x['range'][1]:
        #         print('t:', self.x['tickvals'][t0])
        #         self.x['ticktext'][t0] = self.x['tickvals'][t0]

        #         t0 += x_dtick
        if 'nticks' in self.x:
            x_nticks = self.x['nticks']

            x_step = len(self.x['data']) // x_nticks

            x_ticktext = [''] * len(self.x['ticktext'])

            for i in range(0, len(self.x['tickvals']), x_step):
                x_ticktext[i] = self.x['ticktext'][i]

            self.x['ticktext'] = x_ticktext
        else:
            print('no x_nticks')
            exit(0)
        # -------------------------- X --------------------------

        # -------------------------- Y --------------------------
        self.y['tickvals'] = self.y['data']
        # print(self.y['ticktext'])
        # if 'dtick' in self.y:
        # pass
        # t0 = 0
        # y_dtick = self.y['dtick']

        # while t0 < self.y['range'][1]:
        #     print(t0)
        #     self.y['ticktext'][t0] = 1

        #     t0 += y_dtick
        if 'nticks' in self.y:
            y_nticks = self.y['nticks']
            y_step = len(self.y['data']) // y_nticks

            y_ticktext = [''] * len(self.y['ticktext'])

            # print('data:', self.y['data'])
            # exit(0)
            if self.y['ticktext'][0] != 0:
                y_ticktext[0] = self.y['ticktext'][0]
                print(y_ticktext)
                # exit(0)
                for i in range(len(self.y['tickvals'])):
                    if self.y['tickvals'][i] == y_step:
                        i0 = i
                        break
                for i in range(i0, len(self.y['tickvals']), y_step):
                    y_ticktext[i] = self.y['ticktext'][i]
            else:
                for i in range(y_step, len(self.y['tickvals']), y_step):
                    y_ticktext[i] = self.y['ticktext'][i]

            self.y['ticktext'] = y_ticktext
        else:
            print('no y_nticks')
            exit(0)
        # -------------------------- Y --------------------------

        print('x_tickvals: ', '[', self.x['tickvals'][0], ' ... ', self.x['tickvals'][-1], ']', sep='')
        print('x_ticktext:', '[', end='')
        for elem in self.x['ticktext']:
            if elem != '':
                print(elem, end=', ')
        print('\b\b]')

        print('y_tickvals: ', '[', self.y['tickvals'][0], ' ... ', self.y['tickvals'][-1], ']', sep='')
        print('y_ticktext:', '[', end='')
        for elem in self.y['ticktext']:
            if elem != '':
                print(elem, end=', ')
        print('\b\b]')

        # print(y_step)
        # print(self.z['data'])
        # exit(0)
        # ------------------------------
        # print('x_tickvals:', x_tickvals)
        # print('x_ticktext:', x_ticktext)
        # ------------------------------------------------

        # ------------------------------------------------

        data = [
            # go.Surface(
            #     showlegend=False,
            #     showscale=False,
            #     lighting=dict(diffuse=0.5, specular=.2, fresnel=0.2),
            #     z=z_data,
            #     # colorscale='Portland',
            #     # colorscale='Viridis',
            # )
            # ['aggrnyl', 'agsunset', 'algae', 'amp', 'armyrose', 'balance',
            #  'blackbody', 'bluered', 'blues', 'blugrn', 'bluyl', 'brbg',
            #  'brwnyl', 'bugn', 'bupu', 'burg', 'burgyl', 'cividis', 'curl',
            #  'darkmint', 'deep', 'delta', 'dense', 'earth', 'edge', 'electric',
            #  'emrld', 'fall', 'geyser', 'gnbu', 'gray', 'greens', 'greys',
            #  'haline', 'hot', 'hsv', 'ice', 'icefire', 'inferno', 'jet',
            #  'magenta', 'magma', 'matter', 'mint', 'mrybm', 'mygbm', 'oranges',
            #  'orrd', 'oryel', 'peach', 'phase', 'picnic', 'pinkyl', 'piyg',
            #  'plasma', 'plotly3', 'portland', 'prgn', 'pubu', 'pubugn', 'puor',
            #  'purd', 'purp', 'purples', 'purpor', 'rainbow', 'rdbu', 'rdgy',
            #  'rdpu', 'rdylbu', 'rdylgn', 'redor', 'reds', 'solar', 'spectral',
            #  'speed', 'sunset', 'sunsetdark', 'teal', 'tealgrn', 'tealrose',
            #  'tempo', 'temps', 'thermal', 'tropic', 'turbid', 'twilight',
            #  'viridis', 'ylgn', 'ylgnbu', 'ylorbr', 'ylorrd']
            go.Surface(
                z=self.z['data'],
                colorscale='portland',

                contours=go.surface.Contours(
                    z=go.surface.contours.Z(
                        show=True,
                        usecolormap=True,
                        # highlightcolor='#42f462',
                        project=dict(z=True),
                    )
                )
            )
        ]

        scale = 1

        # print(self.y['tickvals'])
        # print(self.y['range'])
        # print(len(self.x['tickvals']))
        # print(len(self.y['tickvals']))
        # exit(0)

        layout = go.Layout(
            # needed
            # ---------------
            title='<b>' + self.title + '</b>',
            # ---------------

            # -----------------
            width=self.width,
            height=self.height,
            # -----------------

            titlefont=dict(
                family='Lato',
                color='#222',
                size=20,
            ),
            xaxis=dict(
                title=r'$\sqrt{(n_\text{c}(t|{T_\text{early}}))}$'
            ),
            # margin=go.Margin(
            #     l=0,
            #     r=0,
            #     b=0,
            #     t=35,
            #     pad=50,
            # ),

            # zaxis=dict(
            #     tickangle=90
            # ),

            # --------------
            # autosize=False,
            # autosize=True,
            # --------------

            plot_bgcolor='#AAA',
            # paper_bgcolor='#AAA',

            scene=go.layout.Scene(
                camera=dict(
                    up=dict(x=0, y=0, z=1),
                    center=dict(x=0, y=0, z=0.2),
                    eye=dict(x=3.75, y=3.75, z=3.75)
                ),
                xaxis={
                    # title
                    # -----------------------------------
                    'title': self.x['title'],

                    'titlefont': dict(
                        family=self.ticks['family'],
                        color=self.ticks['color'],
                        size=self.ticks['title']['size'],
                    ),
                    # -----------------------------------

                    # ---------------------
                    # ---------------------

                    'linewidth': 2,

                    'showgrid': False,
                    'showline': False,

                    # -----------------------------------
                    # 'tickmode': 'auto',
                    # 'tickmode': 'linear',

                    # 'tick0': self.x['tick0'],
                    # 'dtick': self.x['dtick'],

                    'tickvals': self.x['tickvals'],
                    'ticktext': self.x['ticktext'],

                    'tickfont': dict(
                        family=self.ticks['family'],
                        color=self.ticks['color'],
                        size=self.ticks['size'],
                    ),

                    'tickangle': 0,
                    # -----------------------------------

                    # 'nticks': 5,
                    # 'orientation': 'h',
                    # 'autorange': True,
                    # 'ticktext': self.x_tickvals,
                    # 'autotick': True,
                    # 'showline':True,
                    # 'ticks': 'outside',
                    # 'showticklabels': True,
                    # 'tickangle': 45,
                    # 'linecolor': 'black',
                    # 'linewidth': 2,
                    # 'range': self.x['range'],
                },
                yaxis={
                    # -----------------------------------
                    'title': self.y['title'],

                    'titlefont': dict(
                        family=self.ticks['family'],
                        color=self.ticks['color'],
                        size=self.ticks['title']['size'],
                    ),
                    # -----------------------------------

                    'showgrid': False,
                    'showline': False,
                    # ------------------------------
                    # 'tickmode': 'linear',
                    # 'tickmode': 'array',

                    # 'tick0': self.y['tick0'],
                    # 'dtick': 50,

                    # 'tickvals': self.y['tickvals'],
                    'tickvals': self.y['tickvals'],
                    'ticktext': self.y['ticktext'],
                    # 'ticktext': self.y['ticktext'],

                    'tickfont': dict(
                        family=self.ticks['family'],
                        color=self.ticks['color'],
                        size=self.ticks['size'],
                    ),

                    'tickangle': 0,
                    # ------------------------------

                    'linewidth': 2,

                    # 'autorange': True,
                    # 'autotick': True,
                    # 'tickmode': 'auto',
                    # 'nticks': 5,
                    # 'linecolor': 'black',
                    # 'range': self.y['range'],
                },
                zaxis={
                    # -----------------------------------
                    'title': self.z['title'],

                    'titlefont': dict(
                        family=self.ticks['family'],
                        color=self.ticks['color'],
                        size=self.ticks['title']['size'],
                    ),
                    # -----------------------------------

                    # ------------------------------
                    'tickfont': dict(
                        family=self.ticks['family'],
                        color=self.ticks['color'],
                        size=self.ticks['size'],
                    ),

                    'tickangle': 0,
                    # ------------------------------

                    'showgrid': False,
                    'showline': False,

                    'linewidth': 2,


                    # 'autorange': True,

                    # 'nticks': 5,
                    # 'usecolormap': True,
                    # 'highlightcolor': '#42f462',
                    # 'dtick': -20,
                    # 'tickangle': 45,
                    # 'linecolor': 'black',
                    # 'range': self.z['range'],
                    # 'transform': {'rotate': '0'}
                },
                aspectratio={
                    'x': self.x['scale'],
                    'y': self.y['scale'],
                    'z': self.z['scale'],
                },
            ),
            showlegend=False
            # showlegend=self.showlegend
        )

        self.fig = go.Figure(data=data, layout=layout)

        if self.to_file:
            py.image.save_as(self.fig, filename=self.to_file)
            return

        return

    # -----------------------------------------------------------------------------------------------------------------
    def make_plot(self, online=False, path='', filename='plot3d.html'):
        self.prepare()

        # ---------------------
        print('Making plot...')
        # ---------------------

        if online:
            plotly.offline.plot(self.fig, filename=path + filename)
        else:
            plotly.offline.init_notebook_mode()

            plotly.offline.iplot(self.fig)
    # -----------------------------------------------------------------------------------------------------------------
