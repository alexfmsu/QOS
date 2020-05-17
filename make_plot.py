from utils.Pickle import *
from utils.PlotBuilder3D import *
# import numpy as np

if len(sys.argv) < 2:
    print('Usage: python3 make_plot.py <path>')
    exit(0)

path = sys.argv[1]
if not os.path.isdir(path):
    print('directory <', path, '> not exist', sep='')
    exit(0)

print('path:', path)
# exit(0)
# x_data = [5, 6, 7]
# y_data = [8, 9]
# z_data = [
#     [10, 20, 30],
#     [40, 50, 60],
# ]
# z_data = [
#     [1, 1, 1],
#     [10, 10, 10],
# ]
y_data = pickle_load(path + '/' + 'l.pkl')
x_data = pickle_load(path + '/' + 't.pkl')
z_data = pickle_load(path + '/' + 'sink_A.pkl')

y_data = np.array(y_data, dtype=float)
x_data = np.array(x_data, dtype=float)
# x_data = list(x_data)
z_data = list(z_data)

# y_data[0] = 0
print(x_data)
print(y_data)
# print(z_data)
# z = np.round(z_data, 3)
for i in range(len(z_data)):
    # z_data[i] = list(np.round(z_data[i], 0))
    z_data[i] = np.array(np.round(z_data[i], 3), dtype=float)
    # z_data[i] = list(np.round(z_data[i], 3))
# x_data = [i / 1000 for i in x_data]

# for elem in z_data:
#     print(elem)
# x_data = list(range(31))
# y_data = list(range(21))
# z_data = [0] * 21

# for i in range(21):
#     z_data[i] = [100] * 31

# print(y_data)
# exit(0)
# y_data = sink_A = pickle_load('boom/sink_A.pkl')
# z_data = list(range(100))
# z_data = dt = pickle_load('boom/dt.pkl')

# for d in z_data:
#     print(np.round(d, 3))
# print(z_data[0])
# print(np.shape(z_data))
# exit(0)
# print(dt)

plot_builder = PlotBuilderData3D({
    'title': '',

    # 'width': 1100,
    # 'height': 800,

    'width': 1000,
    'height': 700,

    'x': {
        'title': 't, mks',
        'data': x_data,
        'ticktext': x_data,
        # 'ticktext': list(np.array(x_data) / 1000),
        'range': [0, max(x_data)],
        'tick0': 0,
        'dtick': 200,
        'nticks': 5,
        'scale': 1,
    },
    'y': {
        'title': 'γ<sub>ph out</sub>/γ<sub>ex</sub>',
        'data': y_data,
        'ticktext': y_data,
        'range': [0, max(y_data)],
        'tick0': 0,
        'dtick': 0.1,
        'nticks': 5,
        'scale': 1,
    },
    'z': {
        'data': z_data,
        'title': 'P',
        'range': [0, 1],
        'scale': 1,
    },
    'ticks': {
        'title': {
            'size': 20,
        },
        'family': 'Lato',
        'color': '#222',
        'size': 14,
    },

    'html': '3d.html',

    'to_file': False,

    'online': False,

    'showlegend': False,
})

plot_builder.make_plot(online=True)
