from QOS.Cavity.CavityChain import *
from QOS.QuantumSystem import QuantumSystem
from QOS.State import State

a0 = Atom(
    wa={'1': wc},
    g={'0<->1': wc * 1e-2},
)
a1 = Atom(
    wa={'1': 1},
    g={'0<->1': 2},
)
a0.info()

cv1 = Cavity(wc={'0<->1': wc}, atoms=[a0])
cv1.add_photon(type='0<->1', count=2)


cv0 = Cavity(wc={'0<->1': wc}, atoms=[])

cv2 = Cavity(wc={'0<->1': wc}, atoms=[a1])

cv_chain = CavityChain(cavities=[cv1, cv0, cv2], capacity={'0<->1': 2})

cv_chain.connect(0, 1, wc * 1e-2, ph_type='0<->1')
cv_chain.connect(1, 2, wc * 1e-2, ph_type='0<->1')

cv_chain.info()

qs = QuantumSystem(cavity_chain=cv_chain)
qs.print_basis()

H = qs.H()  # Hamiltonian

# H.print()

init_state = qs.init_state()

init_state *= 1 / sqrt(2)
init_state.print()

init_state.print_amplitudes(mode='braket')
init_state.print_amplitudes(mode='array')

# =====================================================================================================================
# from QOS.Cavity.CavityChain import CavityChain, Cavity, Atom

# from QOS.Cavity.CavityChain import CavityChain
# from QOS.Cavity.Cavity import Cavity
# from QOS.Cavity.Atom import Atom
# =====================================================================================================================
