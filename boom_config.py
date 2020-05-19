wa = wc
g = 0.01 * wc

time_limit = 1 * mks
dt = 0.5 * ns
t_drain = round(ns / dt)
nt = round(time_limit / dt)
t_list = []

lA_0 = g * 0.01

l_a_range = list(range(1, 1000 + 1, 1))

outpath = 'out'
