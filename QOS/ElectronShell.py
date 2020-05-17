class SubShell:

    def __init__(self, max_electrons):
        self.max_electrons = max_electrons
        # self.l = l


class ElectronShell:
    __ID = 1

    def __init__(self, n_levels):
        self.__n_levels = n_levels

        self.__spins = {}

        for lvl in range(n_levels):
            self.__spins[lvl] = [0, 0]

        self.set_id()
        # self.levels = {}

        # for i in electron_shell:
        #     Assert(isinstance(i, tuple), 'i is not tuple')
        #     Assert(len(i) == 2, 'len(i) != 2')
        #     self.set_level(i[0], i[1])

    # -----------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------------- SETTERS ----------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------
    def set_id(self):
        self.__id = ElectronShell.__ID
        ElectronShell.__ID += 1
    # -----------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------

    def set_spin(self, lvl, direction):
        # Assert(spin == 0 or spin == '0' or spin == 'up' or spin == 'down', 'incorrect spin')
        if direction == 'up':
            self.__spins[lvl][0] = self.__id
        elif direction == 'down':
            self.__spins[lvl][1] = self.__id
        else:
            Assert(1 == 0, 'undefined spin direction \'' + str(direction) + '\'')

    def unset_spin(self, lvl, direction):
        Assert(lvl >= 0 and lvl <= self.__n_levels, 'lvl < 0 or lvl > self.__n_levels')

        if direction == 'up':
            self.__spins[lvl][0] = 0
        elif direction == 'down':
            self.__spins[lvl][1] = 0
        else:
            Assert(1 == 0, 'undefined spin direction \'' + str(direction) + '\'')

    def set_electron_id(self, id, new_id):
        found = False

        for k, v in self.__spins.items():
            for i in range(2):
                if v[i] == id:
                    self.__spins[k][i] = new_id
                    found = True
                    break

        Assert(found, 'not found')

    def info(self):
        for k, v in self.__spins.items():
            print('lvl_', k, ': (', v[0], ',', v[1], ')', sep='')
