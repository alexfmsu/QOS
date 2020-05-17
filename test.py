from QOS.QuantumSystem import QuantumSystem
from QOS.State import State
from QOS.Cavity.CavityChain import CavityChain
from QOS.Cavity.Cavity import Cavity
from QOS.Cavity.Atom import Atom
# from QOS.Constants import *
# from QOS.ElectronShell import *
# from QOS.Hamiltonian import *

a0 = Atom(
    wa={'1': wc},
    # wa={'1': wc, '2': wc * 2, },
    g={'0<->1': wc * 1e-2},
    # g={'0<->1': wc * 1e-2, '2<->1': wc * 1e-2, },
    # electron_shell=[(5, 0), (4, 'up')]
)
a1 = Atom(
    wa={'1': 1},
    # wa={'1': 1, '2': 1},
    g={'0<->1': 2},
    # electron_shell=[(5, 0), (4, 'up')]
)
# a2 = Atom(
#     wa={'1': 1, '2': 1, },
#     g={'0<->1': 2, '1<->2': 1, },
#     # electron_shell=[(5, 0), (4, 'up')]
# )
# a3 = Atom(
#     wa={'1': 1, '2': 1, },
#     g={'0<->1': 2, '1<->2': 1, },
#     # electron_shell=[(5, 0), (4, 'up')]
# )

cv1 = Cavity(wc={'0<->1': wc}, atoms=[])
# cv1 = Cavity(wc={'0<->1': 0.2, '1<->2': 0.6}, atoms=[a0])
cv1.add_photon(type='0<->1')
cv1.add_atom(a1)
# cv1.remove_atom(a1)
cv1.remove_atom_by_id(0)
# cv1.add_photon(type='1<->2')

# cv2 = Cavity(wc={'0<->1': wc}, atoms=[a1])

cv1.info()
# cv2.add_photon(type='0<->1')
# cv2 = Cavity(wc={'1<->2': 0.4}, atoms=[])
# cv2.add_photon(type='1<->2', count=2)
# cv2.add_atom(a2)
# a2.up(1)

# cv_chain = CavityChain(cavities=[cv1, cv2], capacity={'0<->1': 3})
# cv_chain.connect(0, 1, wc * 1e-2)

# qs = QuantumSystem(cavity_chain=cv_chain)
# qs.print_basis()

# init_state = qs.init_state()

# init_state *= 1 / sqrt(2)
# init_state.print()

# init_state.print_amplitudes(mode='braket')
# init_state.print_amplitudes(mode='array')

# # # # a0.info()

# # cv1 = Cavity(wc={'0<->1': 0.2}, atoms=[])
# # cv1.info()

# # cv1.add_photon(type='0<->1')
# # cv1.add_atom(a0)

# # cv_chain = CavityChain(capacity={'1 <-> 0': 3}, cavities=[cv1])

# qs = QuantumSystem(cavity_chain=cv_chain)

# qs.print_base_states()
#
# acv1.add_at(type='0<->1')


# acv1.info()
# acv2.info()
