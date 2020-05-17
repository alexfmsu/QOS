import builtins

from utils._assert import Assert
builtins.Assert = Assert

from utils._print import print as Print
builtins.print = Print

from utils._print import hr
builtins.hr = hr

import json as json
builtins.json = json

from time import sleep as sleep
builtins.sleep = sleep

from pygments import highlight, lexers, formatters
builtins.highlight = highlight
builtins.lexers = lexers
builtins.formatters = formatters

from utils.to_Hz import to_Hz
builtins.to_Hz = to_Hz

from utils.sub import sub
builtins.sub = sub

import sys
builtins.sys = sys

import os
builtins.os = os

from math import sqrt
builtins.sqrt = sqrt

from copy import copy, deepcopy
builtins.copy = copy
builtins.deepcopy = deepcopy

from QOS.Constants import wc, ns, mks, ms, KHz, MHz, GHz
builtins.wc = wc
builtins.ns = ns
builtins.mks = mks
builtins.ms = ms
builtins.KHz = KHz
builtins.MHz = MHz
builtins.GHz = GHz

# import numpy as np
