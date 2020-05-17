from QOS.Cavity.Atom import *
# from QOS.Cavity.CavityChain import *
# from QOS.QuantumSystem import QuantumSystem
# from QOS.State import State

a0 = Atom(
    wa={'1': wc},
    g={'0<->1': wc * 1e-2},
)
a1 = Atom(
    wa={'1': wc},
    g={'0<->1': wc * 1e-2},
)
a0.info()
# exit(0)
# cv = Cavity(wc={'0<->1': wc}, atoms=[a0, a1])
# cv.add_photon(type='0<->1', count=2)

# cv_chain = CavityChain(cavities=[cv], capacity={'0<->1': 2})
# cv_chain.info()

# qs = QuantumSystem(cavity_chain=cv_chain)
# qs.print_basis()

# H = qs.H()

# H.print()
