# =====================================================================================================================
from QOS.Cavity.Atom import Atom
from QOS.Cavity.Cavity import Cavity
from QOS.Cavity.CavityChain import CavityChain
# =====================================================================================================================
from QOS.QuantumSystem import QuantumSystem
# =====================================================================================================================
from QOS.WaveFunction import WaveFunction
from QOS.DensityMatrix import DensityMatrix
# =====================================================================================================================
from QOS.Unitary import *
# =====================================================================================================================
from QOS.Constants import *
# =====================================================================================================================


# BEGIN=================================================== UTILS ======================================================
from utils.MkDir import *
from utils.Pickle import *
from utils.LoadPackage import load_pkg
# END===================================================== UTILS ======================================================


# BEGIN=================================================== MPI ========================================================
from lib.MPI.MPI import *
from lib.MPI.ParallelFor import *

mpirank = MPI_Comm_rank()
mpisize = MPI_Comm_size()
# END===================================================== MPI ========================================================


# BEGIN--------------------------------------------------- CONFIG -----------------------------------------------------
if len(sys.argv) < 2:
    print('Usage: python3 boom.py <config.py>')
    exit(0)

path = sys.argv[1]
if not os.path.isfile(path):
    print('file <', path, '> do not exist', sep='')
    exit(0)

config = load_pkg("config", path)

mkdir(config.outpath)

exit(0)

outpath += '/' + '_'.join([
    'boom',
    str(np.round(1 / t_drain, 1)) + 'ns',
    '1mks',
    str('0.01g'),
    str(l_a_range[0]),
    str(l_a_range[-1]),
])
mkdir(outpath)

# print(a)
print('nt =', nt)
print('t_drain =', t_drain)

print(outpath)

ro_err = 0.01
# END----------------------------------------------------- CONFIG -----------------------------------------------------


def operator_L(ro, lindblad):
    l = lindblad['l']
    L = lindblad['L']

    Lcross = L.conj()
    LcrossL = Lcross.data.dot(L.data)

    def b(ro):
        nonlocal L, Lcross, LcrossL, l

        # L1 = 0
        # L2 = 0
        # print("ro.data")
        # print(ro.data.todense())
        # print(np.shape(ro.data))
        # print()
        # print("L.data")
        # print(L.data.todense())
        # print()

        # L_ro = Matrix(m=ro.m, n=ro.n, dtype=np.complex128)
        # L_ro = np.matrix((np.shape(ro)[0], np.shape(ro)[0]))
        # L_ro = csc_matrix(L_ro)
        L1 = (L.data.dot(ro.data)).dot(Lcross.data)
        L1 = csc_matrix(L1)
        # print("L1.data")
        # print(L1.todense())
        # print(np.shape(L1))
        # print()

        # L2 = np.dot(ro.data, LcrossL)
        # print(L2.todense())
        L2 = np.dot(ro.data, LcrossL) + np.dot(LcrossL, ro.data)
        L2 = csc_matrix(L2)
        # print("L2.data")
        # print(L2.todense())
        # print(np.shape(L2))
        # print()
        # L2 = csc_matrix(L2)
        # print("L2.data")
        # print(L2.todense())
        # print()

        # # exit(0)
        # print(L1.todense())
        # print()
        # print()
        # print()
        # print(L2.todense())
        # print()
        # print()
        # print()

        # exit()
        L_ro = l * (L1 - 0.5 * L2)
        # L_ro = l * csc_matrix(L1 - 0.5 * L2, dtype=np.complex128)
        # print(type(L_ro), np.shape(L_ro))

        return L_ro

    return b
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
# сток фотона
a = [
    # |0⟩|-⟩|0⟩|+⟩  |0⟩|0⟩|1⟩|-⟩	|0⟩|1⟩|0⟩|-⟩	|1⟩|0⟩|0⟩|-⟩
    [			0, 		  	  0,			  0, 			  0],  # |0⟩|-⟩|0⟩|+⟩
    [			0, 		  	  0,			  0, 			  1],  # |0⟩|0⟩|1⟩|-⟩
    [			0, 		  	  0,			  0, 			  0],  # |0⟩|1⟩|0⟩|-⟩
    [			0, 		  	  0,			  0, 			  0],  # |1⟩|0⟩|0⟩|-⟩
]
# a = np.matrix(a)
a = csc_matrix(a, dtype=np.complex128)
a = Matrix(m=np.shape(a)[0], n=np.shape(a)[0], dtype=np.complex128, data=a)

# разрушение атома
A = [
    # |0⟩|-⟩|0⟩|+⟩  |0⟩|0⟩|1⟩|-⟩    |0⟩|1⟩|0⟩|-⟩    |1⟩|0⟩|0⟩|-⟩
    [			0, 		  	  0,			  1, 			  0],  # |0⟩|-⟩|0⟩|+⟩
    [			0, 		  	  0,			  0, 			  0],  # |0⟩|0⟩|1⟩|-⟩
    [			0, 		  	  0,			  0, 			  0],  # |0⟩|1⟩|0⟩|-⟩
    [			0, 		  	  0,			  0, 			  0],  # |1⟩|0⟩|0⟩|-⟩
]
# A = np.matrix(A)
A = csc_matrix(A, dtype=np.complex128)
A = Matrix(m=np.shape(A)[0], n=np.shape(A)[0], dtype=np.complex128, data=A)


# BEGIN--------------------------------------------------- CAVITIES ---------------------------------------------------
atom = Atom(
    wa={'1': wc},
    g={'0<->1': g},
)

cv = Cavity(
    wc={'0<->1': wc},
    atoms=[atom],
    sink=[
        {
            'capacity': 1,
            'type': 'photon',
            'lvl': 0,
        },
        {
            'capacity': 1,
            'type': 'atom',
            'lvl': 0,
        },
    ]
)

cv.add_photon(type='0<->1')

cv_chain = CavityChain(capacity={'1 <-> 0': 1}, cavities=[cv])
# END----------------------------------------------------- CAVITIES ---------------------------------------------------


# BEGIN--------------------------------------------------- QUANTUM SYSTEM ---------------------------------------------
qs = QuantumSystem(cavity_chain=cv_chain)
# qs.print_basis()
# END----------------------------------------------------- QUANTUM SYSTEM ---------------------------------------------


# BEGIN--------------------------------------------------- HAMILTONIAN ------------------------------------------------
H = qs.H()
# H.print()
# exit(0)
# END----------------------------------------------------- HAMILTONIAN ------------------------------------------------


# BEGIN--------------------------------------------------- UNITARY ----------------------------------------------------
U = Unitary(H=H, dt=dt)
# U.print()

U_conj = U.conj()
# END----------------------------------------------------- UNITARY ----------------------------------------------------


# BEGIN--------------------------------------------------- WAVEFUNCTION -----------------------------------------------
base_states = H.base_states()

w0 = WaveFunction(
    states=H.base_states(),
    init_state=base_states[2].state()
)

# w0.print()
# END----------------------------------------------------- WAVEFUNCTION -----------------------------------------------


# BEGIN--------------------------------------------------- DENSITY MATRIX ---------------------------------------------
ro_0 = DensityMatrix(w0)
# ro_0.print()
# END----------------------------------------------------- DENSITY MATRIX ---------------------------------------------


sink_a_list = []
sink_A_list = []


for l_a_coeff in l_a_range:
    print(l_a_coeff)

    ro_t = deepcopy(ro_0)

    L_out_A = operator_L(ro_t, {
        'L': A,
        'l': lA_0
    })
    L_out_a = operator_L(ro_t, {
        'L': a,
        'l': lA_0 * l_a_coeff
    })

    sink_a_tmp = []
    sink_A_tmp = []

    t = 0
    cnt = 0

    while cnt <= nt:
        # while t <= time_limit:
        diag_abs = ro_t.diag_abs()
        # print(np.round(diag_abs, 3))

        trace = ro_t.abs_trace()
        # print(trace)

        Assert(abs(1 - trace) <= ro_err, 'ro is not normed')

        sink_A = diag_abs[0]
        # sink_a = diag_abs[1]
        if cnt % t_drain == 0:
            sink_A_tmp.append(sink_A)

            if l_a_coeff == l_a_range[0]:
                t_list.append(round(t / dt / t_drain))
        # print('sink_a:', np.round(sink_a, 3), ', sink_A:', np.round(sink_A, 3), sep='')

        ro_t.evolve(
            U=U,
            U_conj=U_conj,
            dt=dt,
            L=L_out_a(ro_t) + L_out_A(ro_t),
            renormalize=True
        )
        t += dt
        cnt += 1

    # print(t_list)
    # exit(0)
    sink_A_list.append(sink_A_tmp)

pickle_dump(t_list, outpath + '/' + 't.pkl')
pickle_dump(l_a_range, outpath + '/' + 'l.pkl')
pickle_dump(sink_A_list, outpath + '/' + 'sink_A.pkl')

# =====================================================================================================================
# =====================================================================================================================
# from lib.Matrix import *

# H = [
#     # |0⟩|0⟩|-⟩|1⟩    |0⟩|1⟩|-⟩|0⟩    |0⟩|-⟩|+⟩|0⟩    |1⟩|0⟩|-⟩|0⟩
#     [         0,            0,              0,              0],  # |0⟩|0⟩|-⟩|1⟩
#     [         0,           wa,              0,              g],  # |0⟩|1⟩|-⟩|0⟩
#     [         0,            0,              0,              0],  # |0⟩|-⟩|+⟩|0⟩
#     [         0,            g,              0,             wc],  # |1⟩|0⟩|-⟩|0⟩
# ]
# H = csc_matrix(H, dtype=np.complex128)

# w0 = [
#     [0],
#     [1],
#     [0],
#     [0]
# ]
# w0 = csc_matrix(w0, dtype=np.complex128)
# =====================================================================================================================
# =====================================================================================================================
