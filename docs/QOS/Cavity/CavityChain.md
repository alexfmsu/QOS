## QOS/Cavity/CavityChain.py
##
#### Description
class 'CavityChain'
##
#### Constructor
`__init__(self, cavities, capacity)`
###### Parameters:
* cavities: list
* capacity: dict
###### Examples:
* `cv_chain = CavityChain(cavities=[cv1, cv0, cv2], capacity={'0<->1': 3})`
##
#### Methods
`capacity(self)`
###### Returns:
* capacity
###### Return type:
* dict
###### Parameters:
* None
###### Examples:
* `print(cv.capacity())`

`cavity(self, cavity_id)`
###### Returns:
* cavity by id (object)
###### Return type:
* Cavity (object)
###### Parameters:
* cavity_id: int
###### Examples:
* `cv_0 = cavity_chain.cavity(0))`

`get_state(self)`

`connections(self)`

`cavities(self)`
###### Returns:
* cavities
###### Return type:
* dict
###### Parameters:
* None
###### Examples:
* `cavities = cavity_chain.cavities())`

`connect(self, cavity_id1, cavity_id2, amplitude, ph_type)`
###### Returns:
* None
###### Return type:
* None
###### Parameters:
* cavity_id1: int
* cavity_id2: int
* amplitude: complex
* ph_type: str
###### Examples:
* `cv_chain.connect(0, 1, wc * 1e-2, ph_type='0<->1')`

`make_jump(self, cv_from, cv_to, ph_type)`

`info(self, mode=None)`
###### Description:
* Prints info as JSON
###### Returns:
* None
###### Return type:
* None
###### Parameters:
* None

#### Examples
```
from utils._print import print

print('123')
print('123', color='red')
print('123', prefix='\t')
print('123', prefix='\t', color='red')
```
