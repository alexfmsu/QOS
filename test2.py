from QOS.QuantumSystem import QuantumSystem
from QOS.CavityChain import CavityChain
from QOS.Cavity import Cavity
from QOS.Atom import Atom
from QOS.ElectronShell import *
from QOS.Hamiltonian import *

a0 = Atom(
    wa={'0<->1': 1, '2<->1': 1, },
    g={'0<->1': 2, '2<->1': 1, },
    electron_shell=[(5, 0), (4, 'up')]
)
a1 = Atom(
    wa={'0<->1': 1, },
    g={'0<->1': 2},
    electron_shell=[(5, 0), (4, 'up')]
)
a2 = Atom(
    wa={'0<->1': 1, '1<->2': 1, },
    g={'0<->1': 2, '1<->2': 1, },
    electron_shell=[(5, 0), (4, 'up')]
)
a3 = Atom(
    wa={'0<->1': 1},
    # wa={'0<->1': 1, '1<->2': 1, },
    g={'0<->1': 2},
    # g={'0<->1': 2, '1<->2': 1, },
    electron_shell=[(5, 0), (4, 'up')]
)
# a0.info()

cv1 = Cavity(wc={'0<->1': 0.2}, atoms=[])
# cv1.wc_info()
# exit(0)
# cv1 = Cavity(wc={'0<->1': 0.2, '1<->2': 0.4}, atoms=[])
# cv2 = Cavity(wc={'0<->1': 0.6, '1<->2': 0.8}, atoms=[])
cv2 = Cavity(wc={'0<->1': 0.6}, atoms=[])
# cv2 = Cavity(wc={'0<->1': 0.6, '1<->2': 1, }, atoms=[])
# cv2 = Cavity(wc={'0<->1': 1}, wa=1, g=1, atoms=[])
# cv = Cavity(wc=1, n_photons=2, wa=1, atoms=[])

cv1.add_atom(a0)
# cv1.remove_atom(a0)
cv1.add_atom(a1)
cv1.set_atomic_states([1, 1])

# cv1.add_photon(type='0<->1')
cv2.add_photon(type='0<->1')
# cv2.add_photon(type='1<->2')
cv2.add_atom(a2)
cv2.add_atom(a3)
# cv2.add_atom(a0)


# cv1.info(mode='-v')
# a1.info()
# cv2.info(mode='-v')

cv_chain = CavityChain(capacity={'0<->1': 1}, cavities=[cv1, cv2])
cv_chain.connect(0, 1, 3)
# cv_chain = CavityChain(capacity={'0<->1': 1, '1<->2': 2}, cavities=[cv1])
# cv_chain = CavityChain(capacity={'1 <-> 0': 3, '2   <-> 1': 2}, cavities=[cv1, cv2])
# cv_chain = CavityChain(capacity={'1 <-> 0': 1, '2   <-> 1': 2}, cavities=[cv1, cv2])
cv_chain.print_state()
# cv1.print_state()
# exit(0)


# cv_chain.connect(2, 1, 3)
# cv_chain.connect(1, 2, 4)
# cv_chain.print_connections()
# cv_chain.info(mode='-v')
# exit(0)
qs = QuantumSystem(cavity_chain=cv_chain)


# qs.print_base_states()
# cv.remove_atom(a0)
# cv = Cavity(n_photons=2, atoms=[a0])
# cv.info()

# a1 = Atom()
# a1.info()

# H = Hamiltonian(cavity_chain=cv_chain)
# H.print_states()

# H.print()
# H.set_basis()
# H.print_states()
# e = ElectronShell()

# print(ElectronShell.level)
# print(ElectronShell.level['K']['1s'].max_electrons)
