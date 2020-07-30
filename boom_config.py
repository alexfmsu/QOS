from QOS.Constants import *

g = 0.01 * wc # g/hwc = 0.01 << 1 (RWA)

time_limit = 1 * mks # время эволюции: 1 мкс

dt = 0.25 * ns # шаг по времени: 0.25 нс

la_0 = g * 1.0
lA_0 = g * 1.0

# l_a_range = list(range(20))
# l_a_range = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0]
l_a_range = [1.0, 1.5, 2.0]

# l_a = la_0 * l_a_range = g * l_a_range       	# gamma_ph_out
#                              			# т.е. значения gamma_ph_out / gamma_ex лежат в наборе
#                              			# [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0] 

# l_A = lA_0 = g               # gamma_ex

ro_err = 0.01
