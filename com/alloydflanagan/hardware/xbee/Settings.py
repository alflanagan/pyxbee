'''
Created on Jul 8, 2012

@author: lloyd
'''


class Setting(object):
    """
    Setting for an xbee device. Name, AT command(s) used to get/set it
    whether it's writable, etc.
    """
    #TODO: Need to know which xbee types setting is valid for (coord, router,
    #      endpoint). Also some explanatory text for tooltips, etc.
    #      valid values (set or range). Some settings will have special
    #      interpretation of some or all values.
    def __init__(self, name, at_cmds, writable=True, readable=True,
                 encoding="hex"):
        """
        name: short readable name for setting.
        at_cmds: tuple of one or more two-byte strings, used to get/set value.
                 For multi-byte commands, the one to set high bytes comes
                 first.
        writable: if False, setting is read-only
        readable: if False, setting is write-only
        encoding: encoding of value, useful for display, etc.
            Acceptable values:
            # any encoding string accepted by str() (usually "ascii")
            # "hex" to display as hex string
            # "enabled" to display 0 as "disabled" and 1 as "enabled"
        """
        self.name = name
        self.cmds = []
        for c in at_cmds:
            self.cmds.append(c.encode('ascii'))
        self.writeable = writable
        self.readable = readable
        self.encoding = encoding

    @property
    def output_ctrl(self):
        return self.txt_ctrl

    @output_ctrl.setter
    def output_ctrl(self, txt_ctrl):
        self.txt_ctrl = txt_ctrl

    def set_device(self, xbee):
        self.xb = xbee

    def read_value(self):
        if not self.xb or not self.cmds[0]:
            return ''
        result = ''
        for cmd in self.cmds:
            self.xb.at(command=cmd)
            resp = self.xb.wait_read_frame()
            try:
                returned_val = resp['parameter']
                if self.encoding == 'hex':
                    result += self.hex_str(returned_val)
                elif self.encoding == 'enabled':
                    if returned_val == 0:
                        result = 'disabled'
                    else:
                        result = 'enabled'
                else:
                    result += str(returned_val, self.encoding)
            except KeyError:
                result = "N/A"
        return result

    @staticmethod
    def hex_str(data):
        result = ''
        for bytein in data:
            result += '{:02X}'.format(bytein)
        return result
