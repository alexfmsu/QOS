# =====================================================================================================================
# EXAMPLES:

# ---------------------------------------------------------------------------------------------------------------------
# cv = Cavity(wc=0.2, wa=0.2, g=1, __n_atoms=2)
# cv = Cavity(wc=1, wa=1, g=[1.0, 0.5], __n_atoms=2)
# cv = Cavity(wc=1, wa=[1, 1], g=[1.0, 0.5], __n_atoms=2)
# cv = Cavity(wc=0.2, wa=[0.2, 0.2], g=[1.0, 0.5], __n_atoms=2)
# ---------------------------------------------------------------------------------------------------------------------
# =====================================================================================================================


# =====================================================================================================================
# system
import re
import numpy as np
# ---------------------------------------------------------------------------------------------------------------------
# utils
# from PyQuantum.lib.Sub import *
from utils.ParseJumps import *
# =====================================================================================================================


# =====================================================================================================================
class Cavity:
    # -----------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------------- INIT --------------
    # -----------------------------------------------------------------------------------------------------------------
    __slots__ = ['__id', 'wc', 'atoms', '__n_photons', '__n_atoms', 'jumps', '__in_use']

    __ID = 0

    def json_data(self, mode=None):
        json_data = {}

        if mode == '-v':
            json_data['id'] = self.__id

            if self.__n_atoms:
                json_data['n_atoms'] = self.__n_atoms

            json_data['in_use'] = self.__in_use

        json_data['wc'] = {}
        for k, v in self.wc.items():
            json_data['wc'][k] = to_Hz(v['value'])

        if self.__n_atoms:
            json_data['atoms'] = []

        for atom in self.atoms:
            json_data['atoms'].append(atom.json_data(mode))

        return json_data

    def __init__(self, wc, atoms):
        self.__id = Cavity.__ID
        Cavity.__ID += 1

        self.wc = parse_jumps(wc)

        self.unlock()
        Assert(isinstance(atoms, list), 'atoms is not list')
        self.atoms = atoms
        # self.__n_photons = {}

        for i in range(len(self.atoms)):
            atom[i].info()
            Assert(atom[i].in_use(), 'Atom is already in use')
            atom[i].lock()

        self.__n_atoms = len(atoms)

        self.jumps = self.wc.keys()
        self.__n_photons = {ph_type: 0 for ph_type in self.jumps}
        # print(self.__n_photons)
        # exit(0)
        # self.jumps = set(i['notation'] for i in self.wc)

    # -----------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------------- WC_INFO -----------
    # -----------------------------------------------------------------------------------------------------------------
    def wc_info(self):
        print('\twc: ', color='yellow', attrs=['bold'])

        for k, v in self.wc.items():
            print('\t', k, ':\t', to_Hz(v['value']), sep='')

        print()
    # -----------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------------- __n_atoms_INFO ------
    # -----------------------------------------------------------------------------------------------------------------
    def __n_atoms_info(self):
        print('__n_atoms: ', color='yellow', attrs=['bold'], end='')

        print(self.__n_atoms)

        print()
    # -----------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------

    def get_id(self):
        return self.__id

    def get_n_atoms(self):
        return self.__n_atoms

    def set_id(self, id):
        self.__id = id

    # -----------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------------- INFO --------------
    # -----------------------------------------------------------------------------------------------------------------

    def info(self, title=None, prefix=None, mode=None):
        json_data = {'Cavity_' + str(self.get_id()): self.json_data(mode)}

        json_formatted_str = json.dumps(json_data, indent=4)

        colorful_json = highlight(json_formatted_str, lexers.JsonLexer(), formatters.TerminalFormatter())

        print(colorful_json)
    # -----------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------

    # ---------------------------------------------------------
    def add_photon(self, type, count=1):
        Assert(count >= 1, 'count < 1')
        print(self.__n_photons)
        self.__n_photons[type] += count

    def remove_photon(self, type, count=1):
        Assert(count >= 1, 'count < 1')

        self.__n_photons[type] -= count

    def get_n_photons(self):
        return self.__n_photons

    def set_n_photon(self, count=1):
        Assert(count >= 0, 'count < 0')

        self.__n_photons = count
    # ---------------------------------------------------------

    def get_state(self):
        state = []

        ph_state = {}

        for k_wc, v_wc in self.wc.items():
            ph_state[k_wc] = self.__n_photons[k_wc]

        at_state = [i.lvl for i in self.atoms]

        return [ph_state, at_state]

    def print_state(self):
        print('|', self.__n_photons, '⟩', sep='', end='')

        print('|', end='')
        for atom in self.atoms:
            print(atom.lvl, end='')
        print('⟩')

    def set_atomic_states(self, atomic_states):
        for k, v in enumerate(atomic_states):
            self.atoms[k].lvl = v

    def add_atom(self, atom):
        Assert(not atom.in_use(), 'Cavity is already is use')

        self.atoms.append(atom)

        self.__n_atoms += 1

    def remove_atom(self, id):
        for i in range(self.__n_atoms):
            if id == self.atoms[i]:
                self.atoms[i].unlock()

                self.atoms.remove(id)
                self.__n_atoms -= 1

                break

    def lock(self):
        self.__in_use = True

    def unlock(self):
        self.__in_use = False

    def in_use(self):
        return self.__in_use

# =====================================================================================================================
