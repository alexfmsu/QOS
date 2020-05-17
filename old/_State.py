# =====================================================================================================================
# utils
from utils.flat_list import flat_list
# =====================================================================================================================
import copy
import numpy as np


class State:

    @staticmethod
    def array_notation(raw_notation):
        return flat_list(raw_notation)

    @staticmethod
    def string_notation(raw_notation):
        return ''.join(map(str, State.array_notation(raw_notation)))

    @staticmethod
    def flat_list2(nestedList):
        atoms_flag = False
        tensor_flag = False

        s = ''
        flatList = []

        for elem in nestedList:
            if isinstance(elem, list):
                if atoms_flag:
                    s += '|'
                s += State.flat_list2(elem)

                if atoms_flag:
                    s += '〉'

                atoms_flag = False
                tensor_flag = True

            elif isinstance(elem, dict):
                s += '|'

                for v in elem.values():
                    s += str(v)
                s += '〉'

                atoms_flag = True

            else:
                s += str(elem)

        return s

    __ID = 0

    # __slots__ = [
    #     '__id',
    #     '__cavity_chain', '__cavities', '__n_cavities',
    #     '__state', '__braket', '__string', '__array',
    #     '__jumps',
    #     '__amplitudes',
    #     '__capacity',
    #     'amplitude',
    #     'n_base_states'
    # ]

    # -----------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------------- INIT -------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------

    def __init__(self, cavity_chain):
        self.set_id()

        self.__cavity_chain = copy.deepcopy(cavity_chain)
        self.__capacity = self.__cavity_chain.capacity()
        self.__cavities = self.__cavity_chain.cavities()
        self.__n_cavities = len(self.__cavities)

        self.__state = cavity_chain.get_state()

        self.__array = flat_list(self.__state)
        # self.__string = ''.join(map(str, self.__array))
        self.__string = State.string_notation(self.__state)

        self.__braket = State.flat_list2(self.__state)

        self.__jumps = []

        self.__amplitudes = {}
    # -----------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------------- SETTERS ----------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------
    def set_id(self):
        self.__id = State.__ID
        State.__ID += 1
    # -----------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------

    def state(self):
        return self.__cavity_chain.get_state()
        # return self.__state
    # -----------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------------- GETTERS ----------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------

    def id(self):
        return self.__id

    def cavity(self, cavity_id):
        return self.__cavities[cavity_id]

    def n_cavities(self):
        return self.__n_cavities

    def jumps(self):
        return self.__jumps

    def get_state(self):
        self.update_notation()
        return self.__state
    # -----------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------

    def try_jump(self, cv_from, cv_to, ph_type):
        # cv_from -> cv_to
        # print(self.__capacity)
        # print(self.cavity(cv_from).photons(ph_type), self.cavity(cv_to).photons(ph_type))
        if self.cavity(cv_from).photons(ph_type) > 0 and self.cavity(cv_to).photons(ph_type) + 1 <= self.__capacity[ph_type]['value']:
            state = self.state()
            # print(state)
            state[cv_from][0][ph_type] -= 1
            state[cv_to][0][ph_type] += 1
            # print(state)
            # print(self.state())
            # print(State.string_notation(state))
            newcode = State.string_notation(state)
            # exit(0)
            return {
                'cv_from': cv_from,
                'cv_to': cv_to,
                'newcode': newcode,
            }
        elif self.cavity(cv_to).photons(ph_type) > 0 and self.cavity(cv_from).photons(ph_type) + 1 <= self.__capacity[ph_type]['value']:
            state = self.state()

            state[cv_to][0][ph_type] -= 1
            state[cv_from][0][ph_type] += 1

            newcode = State.string_notation(state)

            return {
                'cv_from': cv_to,
                'cv_to': cv_from,
                'newcode': newcode
            }

        return None

    def connect(self, state, amplitude):
        self.__jumps.append({'state': state, 'amplitude': amplitude})
        state.__jumps.append({'state': self, 'amplitude': amplitude})

    def as_string(self):
        return self.__string

    def as_braket(self):
        return self.__braket

    def as_array(self):
        return self.__array

    def update_notation(self):
        self.__state = self.__cavity_chain.get_state()

        self.__array = flat_list(self.__state)
        self.__string = State.string_notation(self.__state)
        self.__braket = State.flat_list2(self.__state)

        # self.__string = ''.join(map(str, self.__array))

    def set_amplitudes(self, k):
        for k_ in range(k):
            self.__amplitudes[k_] = 0j

    def print_amplitudes(self, title='Amplitudes:', mode='short'):
        print(title, color='green')

        if mode == 'short':
            n_amps = self.n_base_states
            n_digits = len(str(n_amps))
            print_format = ''.join(['%', str(n_digits), 'd'])

            for k, v in self.amplitude.items():
                print(k, ': ', np.round(v, 3), sep='')
        elif mode == 'braket':
            for k, v in self.amplitude.items():
                self.print(mode='braket', end='')
                print(': ', np.round(v, 3), sep='')
        elif mode == 'array':
            print(list(self.amplitude.values()), sep='')
        elif mode == '-v':
            for k, v in self.amplitude.items():
                self.print(end='')
                print(': ', np.round(v, 3), sep='')

        print()

    def __mul__(self, coeff):
        for k in self.amplitude.keys():
            self.amplitude[k] *= coeff

        return self

    def make_jump(self, cv_from, cv_to, ph_type):
        self.__cavity_chain.make_jump(cv_from, cv_to, ph_type)

    # -----------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------------- INFO -------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------
    def json_data(self, mode=None):
        self.get_state()
        # self.update_notation()
        json_data = {}

        if mode == '-v':
            json_data['id'] = self.__id

            json_data['as_braket'] = self.as_braket()
            json_data['as_array'] = str(self.as_array())
            json_data['as_string'] = str(self.as_string())

            json_data['jumps'] = []

            for i in self.jumps():
                json_data['jumps'].append({
                    'to': i['state'].__id,
                    'as_braket': i['state'].as_braket(),
                    'as_array': str(i['state'].as_array()),
                    'as_string': i['state'].as_string(),
                    'amplitude': i['amplitude'],
                })

            json_data['n_jumps'] = len(self.jumps())
        else:
            json_data['jumps'] = []

            for i in self.jumps():
                json_data['jumps'].append(
                    self.__string +
                    '-> ' +
                    i['state'].as_string()
                    # i['state'].as_string() +
                    # ' (' + to_Hz(i['amplitude']) + ')'
                )

        return json_data

    def print(self, mode='short', end='\n'):
        if mode == 'short':
            l = []

            for cv_state in self.get_state():
                cv_state[0] = {str(cv_state[0][ph_k]) + str(sub(ph_k.replace('<->', '')))
                               for ph_k in sorted(cv_state[0].keys())}
                # cv[0] = {str(ph_v) + str(sub(ph_k.replace('<->', ''))) for ph_k, ph_v in cv[0].items()}

                cv_state = str(tuple(cv_state))
                cv_state = cv_state.replace('\'', '')
                cv_state = cv_state.replace('{', '')
                cv_state = cv_state.replace('}', '')

                l.append(cv_state)

            print(' ⊗  '.join(l), end=end)
        elif mode == 'braket':
            print(self.as_braket(), end=end)

    def info(self, mode=None):
        if mode == '-v':
            json_data = {'State_' + str(self.__id): self.json_data(mode)}
        else:
            json_data = {self.__string: self.json_data(mode)}

        json_formatted_str = json.dumps(json_data, indent=4, ensure_ascii=False)

        colorful_json = highlight(json_formatted_str, lexers.JsonLexer(), formatters.TerminalFormatter())

        print(colorful_json)
    # -----------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------
# =====================================================================================================================
# def info(self):
#     self.__cavity_chain.info()
# =====================================================================================================================
