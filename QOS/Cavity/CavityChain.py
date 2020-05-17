# =================================================== DESCRIPTION =====================================================
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
# =================================================== DESCRIPTION =====================================================


# =================================================== EXAMPLES ========================================================
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
# =================================================== EXAMPLES ========================================================


# =================================================== TODO ============================================================
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
# =================================================== TODO ============================================================


# =====================================================================================================================
# QOS
from QOS.Cavity.Cavity import *
# =====================================================================================================================
# utils
from utils.ParseJumps import *
# =====================================================================================================================


class CavityChain:

    # -----------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------------- INIT -------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------
    def __init__(self, cavities, capacity):
        self.__capacity = parse_jumps(capacity)

        self.__cavities = {}

        self.__n_cavities = 0

        for i in range(len(cavities)):
            self.__cavities[i] = cavities[i]
            self.__n_cavities += 1

        self.__connections = {}
    # -----------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------

    def n_cavities(self):
        return self.__n_cavities

    def connect(self, cavity_id1, cavity_id2, amplitude, ph_type):
        cvs = sorted([cavity_id1, cavity_id2])

        self.__connections[str(cvs[0]) + '<->' + str(cvs[1])] = {
            'amplitude': amplitude,
            'cavity_ids': cvs,
            'ph_type': ph_type,
        }

    def disconnect(self, cavity_id1, cavity_id2, ph_type=None):
        cvs = sorted([cavity_id1, cavity_id2])

        to_delete = []

        if ph_type is None:
            for conn_i, conn in self.__connections.items():
                if cvs == conn['cavity_ids']:
                    to_delete.append(conn_i)
        else:
            for conn_i, conn in self.__connections.items():
                if conn['ph_type'] == ph_type and cvs == conn['cavity_ids']:
                    to_delete.append(conn_i)
                    break

        Assert(len(to_delete) != 0, 'len(to_delete) == 0')

        for v in to_delete:
            del self.__connections[v]

    def try_jump_cv(self):
        ans = []

        n_cavities = self.n_cavities()

        cv_states = []

        for cv_k, cv_v in self.cavities().items():
            cv_states.append(self.cavity(cv_k).as_array())

        for cv_k, cv_v in self.cavities().items():
            state = self.get_state()

            photons = state[cv_k][0]
            atoms = state[cv_k][1]

            wc = cv_v.wc()
            # print('state:', state)
            # print('state:', self.cavity(0).get_state())
            can_jump = cv_v.try_jump()

            # print('can_jump_cv:', can_jump)

            for jmp in can_jump:
                # print('JMP:', jmp)
                ans_ = ''

                for _ in range(cv_k):
                    ans_ += cv_states[_]
                ans_ += jmp['newcode']
                for _ in range(cv_k + 1, self.__n_cavities):
                    ans_ += cv_states[_]
                    # print('_', _)
                    # ans_ += self.cavity(_).as_array()
                # print('ans:', ans_)

                ans_i = {
                    'newcode': ans_,
                    'cavity': cv_k,
                    'amplitude': jmp['amplitude'],

                }

                for param in 'ph', 'atom_i', 'atom_lvl', 'sink_i', 'sink_lvl', 'sink_type':
                    if param in jmp:
                        ans_i[param] = jmp[param]

                ans.append(ans_i)
                # ans_ = "".join([_.try_jump() for _ in self.cavities()[:cv_k]])
        #     print(ans_)
        # print('chain_ans:')
        # for i in ans:
        #     print(i)
        # print()
        # exit(0)
        return ans

    def make_jump(self, cv_from, cv_to, ph_type):
        self.cavity(cv_from).remove_photon(type=ph_type)
        self.cavity(cv_to).add_photon(type=ph_type)

    # -----------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------------- GETTERS ----------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------
    def capacity(self):
        return self.__capacity

    def cavities(self):
        return self.__cavities

    def cavity(self, cavity_id):
        return self.__cavities[cavity_id]

    def connections(self):
        return self.__connections

    def get_state(self):
        state = ()

        for cv_k, cv_v in self.__cavities.items():
            state += (cv_v.get_state(),)

        return state
    # -----------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------------- INFO -------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------
    def json_data(self, mode):
        json_data = {}
        json_data['Capacity'] = {}

        for k, v in self.__capacity.items():
            json_data['Capacity'][k] = v['value']

        for cavity in self.__cavities.values():
            json_data['Cavity_' + str(cavity.id())] = cavity.json_data(mode)

        if self.__connections:
            json_data['Connections'] = {}

            for conn_k, conn_v in self.__connections.items():
                conn_type = 'Cavity_' + str(conn_v['cavity_ids'][0]) + '<->' + 'Cavity_' + str(conn_v['cavity_ids'][1])
                json_data['Connections'][conn_type] = to_Hz(conn_v['amplitude'])
                # print(cvs, ': ', to_Hz(mu), sep='')

        return json_data

    def info(self, title=None, mode=None):
        if title is None:
            title = 'CavityChain:'

        json_data = {title: self.json_data(mode)}

        json_formatted_str = json.dumps(json_data, indent=4)

        colorful_json = highlight(json_formatted_str, lexers.JsonLexer(), formatters.TerminalFormatter())

        print(colorful_json)
    # -----------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------
# =====================================================================================================================
