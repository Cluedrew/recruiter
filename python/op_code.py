"""Look up from operation names to op codes.

An operation here are the three letter combination that starts off each
assembly instructions. This file defines each one known, who has access to it
and the op code each repersents.
"""


__all__ = [
    'OPERATIONS',
    'CAPTAIN_OPS',
    'MORTAR_OPS',
    'SNIPER_OPS',
    'ENGINEER_OPS',
    'RIFLEMAN_OPS',
    'MACHINEGUNNER_OPS',
    'SCOUT_OPS',
    'SECTION_OPS',
    'OpCodeMapping',
    ]


from itertools import chain, repeat
from typing import Mapping, Optional, FrozenSet

from _op_code import (
    _BASIC_OPERATIONS,
    _COMBAT_OPERATIONS,
    _UPGRADE_OPERATIONS,
    _CAPTAIN_OPERATIONS,
    _MORTAR_OPERATIONS,
    _SNIPER_OPERATIONS,
    _ENGINEER_OPERATIONS,
    _RIFLEMAN_OPERATIONS,
    _MACHINEGUNNER_OPERATIONS,
    _SCOUT_OPERATIONS,
    _PSEUDO_OPERATIONS,
    )


class OpData:
    """Stores information about the operation.

    op_code: The integer value that repersents the operation. Pseudo-
        operations that don't repersent a particular command store
        None instead.
    format: The layout of the regesters and imediate values the command
        stores and how they can be presented in code.
    """

    def __init__(self, op_code, format):
        self.op_code = op_code
        self.format = format


class OpCodeMapping(dict, Mapping[str, OpData]):

    def __init__(self, *source_mappings):
        super().__init__(map(
            lambda kvp: (kvp[0], OpData(*kvp[1])),
            chain.from_iterable(map.items() for map in source_mappings)
            ))


# TODO: Python 3.6 has the variable annotation, although I don't know
# if they work quite like this.
#OPERATIONS: FrozenSet[str]
#CAPTAIN_OPS: OpCodeMapping
#MORTAR_OPS: OpCodeMapping
#SNIPER_OPS: OpCodeMapping
#ENGINEER_OPS: OpCodeMapping
#RIFLEMAN_OPS: OpCodeMapping
#MACHINEGUNNER_OPS: OpCodeMapping
#SCOUT_OPS: OpCodeMapping
#SECTION_OPS: Mapping[int, OpCodeMapping]


OPERATIONS = frozenset(
    chain(_PSEUDO_OPERATIONS,
          _BASIC_OPERATIONS,
          _COMBAT_OPERATIONS,
          _UPGRADE_OPERATIONS,
          _CAPTAIN_OPERATIONS,
          _MORTAR_OPERATIONS,
          _SNIPER_OPERATIONS,
          _ENGINEER_OPERATIONS,
          _RIFLEMAN_OPERATIONS,
          _MACHINEGUNNER_OPERATIONS,
          _SCOUT_OPERATIONS,
          ))


def _unit_op_map(unit_operations):
    return OpCodeMapping(
        _PSEUDO_OPERATIONS,
        _BASIC_OPERATIONS,
        _COMBAT_OPERATIONS,
        _UPGRADE_OPERATIONS,
        unit_operations,
        )


CAPTAIN_OPERATIONS = _unit_op_map(_CAPTAIN_OPERATIONS)
MORTAR_OPERATIONS = _unit_op_map(_MORTAR_OPERATIONS)
SNIPER_OPERATIONS = _unit_op_map(_SNIPER_OPERATIONS)
ENGINEER_OPERATIONS = _unit_op_map(_ENGINEER_OPERATIONS)
RIFLEMAN_OPERATIONS = _unit_op_map(_RIFLEMAN_OPERATIONS)
MACHINEGUNNER_OPERATIONS = _unit_op_map(_MACHINEGUNNER_OPERATIONS)
SCOUT_OPERATIONS = _unit_op_map(_SCOUT_OPERATIONS)


SECTION_OPS = {
    1: CAPTAIN_OPERATIONS,
    2: MORTAR_OPERATIONS,
    3: SNIPER_OPERATIONS,
    4: ENGINEER_OPERATIONS,
    5: ENGINEER_OPERATIONS,
    6: MACHINEGUNNER_OPERATIONS,
    7: MACHINEGUNNER_OPERATIONS,
    8: SCOUT_OPERATIONS,
    9: SCOUT_OPERATIONS,
    10: RIFLEMAN_OPERATIONS,
    11: RIFLEMAN_OPERATIONS,
    }
