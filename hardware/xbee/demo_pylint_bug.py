from collections import MutableMapping

class CustomMapping(MutableMapping):

    def __init__(self, *args, **kwargs):
        #triggers E1002, which should *never* occur in python 3 (where old-style classes don't exist)
        super().__init__(*args, **kwargs)
