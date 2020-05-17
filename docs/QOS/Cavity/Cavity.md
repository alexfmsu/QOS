## QOS/Cavity.py

##
#### Description

class 'Cavity'
##
#### Constructor
`__init__(self, wc, atoms=[]):`
##
#### Methods
`add_photon(self, type, count=1)`
  ###### Parameters:
  * type: dict
  * count: int (optional)
  ###### Examples:
  * `cv.add_photon(type='0<->1')`
  * `cv.add_photon(type='0<->2')`
  * `cv.add_photon(type='1<->2', count=2)`

`remove_photon(self, type, count=1)`
  ###### Parameters:
  * type:dict
  * count:int (optional)
  ###### Examples:
  * `cv.remove_photon(type='0<->1')`
  * `cv.remove_photon(type='0<->2')`
  * `cv.remove_photon(type='1<->2', count=2)`

`add_atom(self, atom)`
  ###### Parameters:
  * atom: Atom (object)
  ###### Examples:
  * ```
    at = Atom(
        wa={'1': wc},
        g={'0<->1': wc * 1e-2}
    )

    cv.add_atom(at)
    ```
`remove_atom(self, atom)`
  ###### Parameters:
  * atom: Atom (object)
  ###### Examples:
  * ```
    at = Atom(
        wa={'1': wc},
        g={'0<->1': wc * 1e-2}
    )

    cv.add_atom(at)
    # ...
    cv.remove_atom(at)
    ```

`remove_atom_by_id(self, atom_id)`
  ###### Parameters:
  * atom_id: int
  ###### Examples:
  * `cv.remove_atom_by_id(0)`

`id(self)`
  ###### Parameters:
  * None
  ###### Examples:
  * `cv_id = cv.id()
    ```

`wc(self)`
  ###### Parameters:
  * None
  ###### Examples:
  * `wc = cv.wc()`

`photons(self, ph_type=None)`
  ###### Parameters:
  * ph_type: dict (optional)
  ###### Examples:
  * `photons = cv.photons()`
  * `photons = cv.photons(ph_type='0<->1')`

`atom(self, i)`

`get_state(self)`

`info(self, title=None, prefix=None, mode=None)`
##
#### Examples
```
from QOS.Cavity.Cavity import Cavity

cv0 = Cavity(wc={'0<->1': wc}, atoms=[])
```
