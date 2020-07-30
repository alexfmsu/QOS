# =====================================================================================================================
# system
import os
# =====================================================================================================================
# PyQuantum.Tools
from utils.MkDir import *
from lib.MPI.MPI import *
# =====================================================================================================================


def parallel_for(func, path, prefix, var=None):
    pwd = os.getcwd() # saved pwd

    mpirank = MPI_Comm_rank()
    # print('var', var)
    # if var is not None:
    #     i = var[mpirank]
    # else:
    #     i = mpirank
    path_i = str(path) + '/node_' + str(mpirank) + '/'
    # path_i = str(path) + '/' + str(prefix) + str(i) + '/'
    # print(path_i)
    mkdir(path_i)

    os.chdir(path_i)

    # print(a)
    # print('p=', os.getcwd(), flush=True)

    func()

    os.chdir(pwd)
