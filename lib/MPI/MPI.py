# =====================================================================================================================
# system
import os
from math import ceil
# =====================================================================================================================
# mpi4py
from mpi4py import MPI

MPI_COMM_WORLD = MPI.COMM_WORLD
# =====================================================================================================================
# PyQuantum.Tools
from utils.Pickle import *
from utils._print import print
# =====================================================================================================================


# =====================================================================================================================
# ---------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------- MPI_Comm_rank ----------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
def MPI_Comm_rank():
    return MPI_COMM_WORLD.Get_rank()
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------- MPI_Comm_size ----------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
def MPI_Comm_size():
    return MPI_COMM_WORLD.Get_size()
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------- MPI_Abort --------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
def MPI_Abort(err_msg, filename=None, to_print=True):
    if not hasattr(MPI_Abort, '_mpirank'):
        MPI_Abort._mpirank = mpirank = MPI_Comm_rank()
    # print('mpirank:', MPI_Abort._mpirank)

    MPI_Barrier()

    if mpirank == 0:
        if to_print:
            print(err_msg)

        if filename is not None:
            f = open(filename, 'w')
            f.write(err_msg)
            f.close()

    MPI_Barrier()

    MPI_COMM_WORLD.Abort()
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------- MPI_Barrier ------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
def MPI_Barrier():
    MPI_COMM_WORLD.barrier()
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------- N_BATCHES --------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
def n_batches(l):
    n = len(l)

    mpirank = MPI_Comm_rank()
    mpisize = MPI_Comm_size()

    n_batches = int(n / mpisize)

    n1 = mpirank * n_batches
    n2 = n1+n_batches

    if n % mpisize != 0:
        if mpirank < n % mpisize:
            n1 += mpirank
            n2 += mpirank+1
        else:
            pass
            n1 += n % mpisize
            n2 += n % mpisize

    # return '[' + str(n1) + ',' + str(n2) + ']'
    return l[n1:n2]
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------- GATHER_FILE ------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
def gather_file(path, filename):
    if not hasattr(gather_file, '_mpirank'):
        gather_file._mpirank = mpirank = MPI_Comm_rank()

    MPI_Barrier()

    pwd = os.getcwd()

    if mpirank == 0:
        # os.chdir('..')
        # print(os.getcwd())
        os.chdir('..')
        # print(os.getcwd())
        data = []
        for node_i in range(MPI_Comm_size()):
            # print('123')
            data_i = pickle_load('node_' + str(node_i) + '/' + filename)
            # print(data_i)
            data += data_i

        pickle_dump(data, filename)

        os.chdir(pwd)

    MPI_Barrier()
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------- NODE_PRINT -------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
def node_print(msg, rank, filename=None, to_print=True):
    if not hasattr(MPI_Abort, '_mpirank'):
        node_print._mpirank = mpirank = MPI_Comm_rank()

    MPI_Barrier()

    if mpirank == rank:
        if filename is not None:
            f = open(filename, 'w')
            f.write(msg)
            f.close()

        if to_print:
            print(msg)

    MPI_Barrier()
# ---------------------------------------------------------------------------------------------------------------------
# =====================================================================================================================
