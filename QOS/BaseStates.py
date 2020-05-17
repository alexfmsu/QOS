import re
from QOS.State import State


class BaseStates:

    # -----------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------------- INIT -------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------
    def __init__(self, states):
        self.states = {}
        for k, v in enumerate(sorted(states)):
            self.states[k] = states[v]
            self.states[k].n_base_states = len(states)

            self.states[k].amplitude = {}

            for _ in range(len(states)):
                self.states[k].amplitude[_] = 0j

            self.states[k].amplitude[k] = 1

            # print(self.states[k].amplitude.keys())

        State.BASE_STATES = self.states
    # -----------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------------- GETTERS ----------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------
    def key_by_id(self, id):
        for k, v in self.states.items():
            if v.id() == id:
                key = k
                break

        return key

    # -----------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------------- PRINT ------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------
    def print(self, mode='short'):
        print('Basis:', color="green")

        n_states = len(self.states)
        n_digits = len(str(n_states))
        print_format = ''.join(['%', str(n_digits), 'd'])

        if mode == 'string':
            for k, v in self.states.items():
                print(print_format % k, ': ', v.as_string(), sep='')
        elif mode == 'array':
            for k, v in self.states.items():
                print(print_format % k, ': ', v.as_array(), sep='')
        elif mode == 'braket':
            for k, v in self.states.items():
                print(print_format % k, ': ', v.as_braket(), sep='')
        elif mode == 'raw':
            for k, v in self.states.items():
                print(print_format % k, ': ', v.state, sep='')
        elif mode == 'short':
            # print(self.states)
            for k, v in self.states.items():
                print(print_format % k, ': ', sep='', end='')
                v.print('short')
    # -----------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------
# =====================================================================================================================
# # -----------------------------------------------------------------------------------------------------------------
# # ---------------------------------------------------- PRINT ------------------------------------------------------
# # -----------------------------------------------------------------------------------------------------------------
# def print(self, mode='short'):
#     print('Basis:', color="green")

#     n_states = len(self.states)
#     n_digits = len(str(n_states))
#     print_format = ''.join(['%', str(n_digits), 'd'])

#     if mode == 'string':
#         for k, v in self.states.items():
#             print(print_format % k, ': ', v.as_string(), sep='')
#     elif mode == 'array':
#         for k, v in self.states.items():
#             print(print_format % k, ': ', v.as_array(), sep='')
#     elif mode == 'braket':
#         for k, v in self.states.items():
#             print(print_format % k, ': ', v.as_braket(), sep='')
#     elif mode == 'raw':
#         for k, v in self.states.items():
#             print(print_format % k, ': ', v.state, sep='')
#     elif mode == 'short':
#         # print(self.states)
#         for k, v in self.states.items():
#             l = []
#             # print(v.get_state())
#             for cv in v.get_state():
#                     # print(cv)
#                 cv[0] = {str(cv[0][ph_k]) + str(sub(ph_k.replace('<->', ''))) for ph_k in sorted(cv[0].keys())}
#                 # cv[0] = {str(ph_v) + str(sub(ph_k.replace('<->', ''))) for ph_k, ph_v in cv[0].items()}
#                 cv = str(tuple(cv))
#                 cv = cv.replace('\'', '')
#                 cv = cv.replace('{', '')
#                 cv = cv.replace('}', '')

#                 l.append(cv)

#             print(print_format % k, ': ', ' ⊗  '.join(l), sep='')
# # -----------------------------------------------------------------------------------------------------------------
# # -----------------------------------------------------------------------------------------------------------------
# =====================================================================================================================
