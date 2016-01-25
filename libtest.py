import imp
try:
    imp.find_module('dataset')
    found = True
except ImportError:
    found = False
print found
