"""Stores definitions made in the assembly code.

It sorts data by section. There is one section for shared definitions,
section 0, and one section for each unit that has its own definitions.

Note this DOES NOT conform to the behaviour of the as compiler*. If you
put everything in the proper section some sharing/conflicts that happen
with as will not happen here.

* From conversation with its creator and because nothing about scope
  is given in the documentation.
"""


from collections import ChainMap


NUM_OF_UNITS = 11


class Defines:
    """All defines currently 'active' in the program."""

    def __init__(self):
        self._current_section = 0
        self.section_defines = [ChainMap({})]
        self.section_defines.extend(
            self.section_defines[0].new_child() for _ in range(NUM_OF_UNITS))
        self.current_section_define = self.section_defines[0]

    @property
    def current_section(self):
        """The ID number of the code section we are in."""
        return self._current_section

    @current_section.setter
    def current_section(self, value):
        assert 0 <= value < len(self.section_defines)
        self._current_section = value
        self.current_section_define = self.section_defines[value]

    def __getitem__(self, key):
        return self.current_section_define[key]

    def __setitem__(self, key, value):
        self.current_section_define[key] = value

    def __delitem__(self, key):
        del self.current_section_define[key]
