# =================================================== DESCRIPTION =====================================================
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
# =================================================== DESCRIPTION =====================================================


# =================================================== EXAMPLES ========================================================
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
# =================================================== EXAMPLES ========================================================


# =====================================================================================================================
# system
from copy import deepcopy
from math import sqrt
# =====================================================================================================================
# QOS
from QOS.State import State
from QOS.BaseStates import BaseStates
from QOS.Hamiltonian import Hamiltonian
# =====================================================================================================================


class QuantumSystem:
    __slots__ = ['__basis', '__cavity_chain', '__init_state', '__H']
    # -----------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------------- INIT -------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------

    def __init__(self, cavity_chain):
        self.__cavity_chain = cavity_chain

        self.__init_state = State(cavity_chain=self.__cavity_chain)

        self.__basis = self.set_basis()

        n_base_states = len(self.__basis.states)

        self.__H = Hamiltonian(base_states=self.__basis, cavity_chain=self.__cavity_chain)
    # -----------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------------- GETTERS ----------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------
    def init_state(self):
        return self.__init_state
    # -----------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------------- SET_BASIS --------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------
    def set_basis(self):
        cv_chain = self.__cavity_chain
        cavities = list(cv_chain.cavities())

        self.__init_state = state = State(cavity_chain=cv_chain)

        notation = state.as_string()

        base_states = {}
        base_states_not_checked = {notation: state}

        while len(base_states_not_checked):
            keys = base_states_not_checked.keys()
            keys = list(keys)

            notation = keys[0]
            state = base_states_not_checked[notation]

            # mu
            for conn_k, conn_v in cv_chain.connections().items():
                ph_type = conn_v['ph_type']
                can = state.try_jump(cv_from=conn_v['cavity_ids'][0], cv_to=conn_v['cavity_ids'][1], ph_type=ph_type)

                if can is not None:
                    newcode = can['newcode']

                    if (newcode not in base_states) and (newcode not in base_states_not_checked):
                        new_state = deepcopy(state)

                        new_state.make_jump(cv_from=can['cv_from'], cv_to=can['cv_to'], ph_type=ph_type)

                        new_state.set_id()

                        base_states_not_checked[newcode] = new_state
                        amplitude = sqrt(cv_chain.cavity(can['cv_from']).wc(ph_type)['value']) * \
                            sqrt(cv_chain.cavity(can['cv_to']).wc(ph_type)['value'] + 1)
                        amplitude = {
                            'value': amplitude,
                        }
                        # print(amplitude)
                        # exit(0)
                        state.connect(state=new_state, amplitude=amplitude)

                        # hr(100)
                        # print('\tadd_state1:\t', newcode)
                        # # state.print()
                        # # new_state.print()
                        # hr(100)
                        # print()

            # g
            can_jump_cv = cv_chain.try_jump_cv()
            # print(can_jump_cv)

            if len(can_jump_cv):
                for jmp in can_jump_cv:
                    newcode = jmp['newcode']
                    if (newcode not in base_states) and (newcode not in base_states_not_checked):
                        new_state = deepcopy(state)

                        if jmp['ph']['action'] == 'add':
                            new_state.cavity(jmp['cavity']).add_photon(jmp['ph']['ph_type'])
                        else:
                            new_state.cavity(jmp['cavity']).remove_photon(jmp['ph']['ph_type'])

                        new_state.cavity(jmp['cavity']).atom(jmp['atom_i']).change_lvl(jmp['atom_lvl'])

                        new_state.set_id()

                        base_states_not_checked[newcode] = new_state
                        amplitude = jmp['amplitude']
                        # amplitude = {
                        #     'value': jmp['amplitude']
                        # }
                        state.connect(state=new_state, amplitude=amplitude)
                        # print(amplitude)
                        # exit(0)

                        # hr(100)
                        # print('\tadd_state1:\t', newcode)
                        # # state.print()
                        # # new_state.print()
                        # hr(100)
                        # print()

            del base_states_not_checked[notation]
            base_states[notation] = state

        Assert(len(base_states_not_checked) == 0, 'len(base_states_not_checked) != 0')
        # for k, v in base_states_not_checked.items():
        #     v.print()
        # for k, v in base_states.items():
        #     v.print()

        self.__basis = BaseStates(base_states)

        return self.__basis
    # -----------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------------- INFO -------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------
    def print_basis(self, mode='short'):
        self.__basis.print()
        print()

        # for k, v in self.__base_states.items():
        #     v.info('-v')

    def info(self):
        pass
    # -----------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------
# =====================================================================================================================
    # def set_basis(self):
    #     cv_chain = self.__cavity_chain
    #     cavities = list(cv_chain.cavities())
    #     self.__init_state = state = State(cavity_chain=cv_chain)

    #     notation = state.as_string()

    #     base_states = {}
    #     base_states_not_checked = {notation: state}

    #     while len(base_states_not_checked):
    #         keys = base_states_not_checked.keys()
    #         keys = list(keys)

    #         notation = keys[0]
    #         state = base_states_not_checked[notation]

    #         new_state = deepcopy(state)
    #         new_state_cpy = deepcopy(new_state)

    #         # print('STATE: ', end='')
    #         # state.print()
    #         # print('NEW_STATE: ', end='')
    #         # new_state.print()
    #         # print()

    #         # print(self.__cavity_chain.connections())
    #         for conn_k, conn_v in self.__cavity_chain.connections().items():
    #             ph_type = conn_v['ph_type']
    #             # print(ph_type)
    #             can = state.try_jump(cv_from=conn_v['cavity_ids'][0], cv_to=conn_v['cavity_ids'][1], ph_type=ph_type)

    #             if can is not None:
    #                 new_state.make_jump(cv_from=can['cv_from'], cv_to=can['cv_to'], ph_type=ph_type)
    #                 # new_state.print()

    #                 newcode = State.string_notation(new_state.get_state())

    #                 if (newcode not in base_states) and (newcode not in base_states_not_checked):
    #                     new_state.set_id()

    #                     base_states_not_checked[newcode] = new_state
    #                     amplitude = 1
    #                     state.connect(state=new_state, amplitude=amplitude)

    #                     print('\tadd_state1:\t', newcode, '\t', end='')
    #                     new_state.print()
    #                     print()

    #                     new_state = state
    #                 else:
    #                     new_state = deepcopy(state)
    #         # print('state:')
    #         # state.print()
    #         # print('new_state:')
    #         # new_state.print()

    #         # print(cv_chain.cavities().keys())
    #         # exit(0)
    #         for cv_k, cv_v in cv_chain.cavities().items():
    #             photons = state.get_state()[cv_k][0]
    #             atoms = state.get_state()[cv_k][1]

    #             wc = cv_v.wc()

    #             for ph_type, ph_cnt in photons.items():
    #                 for k_atom, v_atom in enumerate(atoms):
    #                     lvl = state.get_state()[cv_k][1][k_atom]
    #                     n_levels = cv_v.atom(k_atom).n_levels()

    #                     lvl_from = wc[ph_type]['levels'][0]
    #                     lvl_to = wc[ph_type]['levels'][1]

    #                     new_state_ok = False

    #                     # from cavity -> to atom
    #                     # new_state = None

    #                     if photons[ph_type] > 0:
    #                         # upper atom level
    #                         if lvl == lvl_from:
    #                             ph_count = state.get_state()[cv_k][0][ph_type]

    #                             new_state.cavity(cv_k).remove_photon(type=ph_type)
    #                             new_state.cavity(cv_k).atom(k_atom).up(lvl_to)

    #                             # new_state = deepcopy(state)
    #                             # print('\tstate2:\t', end='')
    #                             # state.print()
    #                             # print('\tnew_state2:\t', end='')
    #                             # new_state.print()
    #                             # print()

    #                             amplitude = {
    #                                 'type': 'g' + sub(lvl_from) + sub(lvl_to),
    #                                 'value': sqrt(ph_count) * cv_v.atom(k_atom).g(ph_type)['value'],
    #                             }
    #                             new_state_ok = True

    #                     else:
    #                         # lower atom level
    #                         if lvl == lvl_to:
    #                             ph_count = state.get_state()[cv_k][0][ph_type]

    #                             # new_state = deepcopy(state)

    #                             amplitude = sqrt(ph_count + 1) * cv_v.atom(k_atom).g(ph_type)['value']

    #                             new_state.cavity(cv_k).add_photon(type=ph_type)
    #                             new_state.cavity(cv_k).atom(k_atom).down(lvl_from)

    #                             # print('\tstate2:\t', end='')
    #                             # state.print()
    #                             # print('\tnew_state2:\t', end='')
    #                             # new_state.print()
    #                             # print()

    #                             amplitude = {
    #                                 'type': 'g' + sub(lvl_from) + sub(lvl_to),
    #                                 'value': cv_v.atom(k_atom).g(ph_type)['value'],
    #                             }
    #                             new_state_ok = True

    #                     if new_state_ok:
    #                         newcode = State.string_notation(new_state.get_state())

    #                         if (newcode not in base_states) and (newcode not in base_states_not_checked):
    #                             new_state.set_id()

    #                             base_states_not_checked[newcode] = new_state
    #                             amplitude = 1
    #                             state.connect(state=new_state, amplitude=amplitude)

    #                             # print('\tadd_state1:\t', newcode, '\t', end='')
    #                             # new_state.print()
    #                             # print()

    #                             new_state = state
    #                         else:
    #                             new_state = deepcopy(state)

    #         del base_states_not_checked[notation]
    #         base_states[notation] = state

    #     for k, v in base_states_not_checked.items():
    #         print(k, ": ", end='')
    #         v.print()
    #     return
# =====================================================================================================================
