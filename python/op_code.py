"""Look up from operation names to op codes.

An operation here are the three letter combination that starts off each
assembly instructions. This file defines each one known, who has access to it
and the op code each repersents.
"""


from itertools import chain, repeat
from typing import Mapping, Optional, FrozenSet


__all__ = ['OPERATIONS', '']


OpCodeMapping = Mapping[str, Optional[str]]


OPERATIONS: FrozenSet[str]
CAPTAIN_OPS: OpCodeMapping
MORTAR_OPS: OpCodeMapping
SNIPER_OPS: OpCodeMapping
ENGINEER_OPS: OpCodeMapping
RIFLEMAN_OPS: OpCodeMapping
MACHINEGUNNER_OPS: OpCodeMapping
SCOUT_OPS: OpCodeMapping
SECTION_OPS: Mapping[int, OpCodeMapping]


# End of interface.

# Maps of Operations to Op-Codes
_BASIC_OFFSET = 0
_BASIC_OPERATIONS = {
    'ADD': 0,
    'SUB': 1,
    'MUL': 2,
    'DIV': 3,
    'AND': 4,
    'ORR': 5,
    'XOR': 6,
    'NAN': 7,
    'CLZ': 8,
    'CNT': 9,
    'LSR': 10,
    'LSL': 11,
    'ABS': 12,
    'RND': 13,
    'CMP': 14,
    'JIZ': 15,
    'JNZ': 16,
    'JGZ': 17,
    'JLZ': 18,
    'JGE': 19,
    'JLE': 20,
    'BIZ': 21,
    'BNZ': 22,
    'BGZ': 23,
    'BLZ': 24,
    'BGE': 25,
    'BLE': 26,
    'BLX': 27,
    'LDR': 28,
    'STR': 29,
    'POP': 30,
    'PSH': 31,
    }

_COMBAT_OFFSET = 32
_COMBAT_OPERATIONS = {
    'WHO': 0,
    'WHT': 1,
    'QCS': 2,
    'QCT': 3,
    'QBP': 4,
    'QCK': 5,
    'GND': 6,
    'WHR': 7,
    'DST': 8,
    'CVR': 9,
    'DED': 10,
    'SHT': 11,
    'DIR': 12,
    'WLK': 13,
    'CRL': 14,
    'SWM': 15,
    'CAP': 16,
    'LIN': 17,
    'HID': 18,
    'SAY': 19,
    'RAD': 20,
    'YEL': 21,
    'EAR': 22,
    'DIE': 23,
    'NRT': 24,
    'NRE': 25,
    'EST': 26,
    'SOE': 27,
    'SOT': 28,
    'SOW': 29,
    'WST': 30,
    'NRW': 31,
    }

_UPGRATE_OFFSET = 64
_UPGRADE_COMMANDS = {
    'WHO': 0,
    'WHT': 1,
    'QCS': 2,
    'QCT': 3,
    'QBP': 4,
    'QCK': 5,
    'GND': 6,
    'WHR': 7,
    'DST': 8,
    'CVR': 9,
    'DED': 10,
    'SHT': 11,
    'DIR': 12,
    'WLK': 13,
    'CRL': 14,
    'SWM': 15,
    'CAP': 16,
    'LIN': 17,
    'HID': 18,
    'SAY': 19,
    'RAD': 20,
    'YEL': 21,
    'EAR': 22,
    'DIE': 23,
    'NRT': 24,
    'NRE': 25,
    'EST': 26,
    'SOE': 27,
    'SOT': 28,
    'SOW': 29,
    'WST': 30,
    'NRW': 31,
    }


_SPECIAL_OFFSET = 96


_CAPTAIN_OPERATIONS = {
    }


_MORTAR_OPERATIONS = {
    }


_SNIPER_OPERATIONS = {
    }


_ENGINEER_OPERATIONS = {
    }


_MACHINEGUNNER_OPERATIONS = {
    }


_SCOUT_OPERATIONS = {
    }


_RIFLEMAN_OPERATIONS = {
    }


_PSEUDO_OPERATIONS = [
    'RAW',
    ]


# Combine all the lists and keys.
OPERATIONS = frozenset(
    chain(_PSEUDO_OPERATIONS,
          _BASIC_OPERATIONS,
          _COMBAT_OPERATIONS,
          _UPGRADE_OPERATIONS,
          _CAPTAIN_OPERATIONS,
          _MORTAR_OPERATIONS,
          _SNIPER_OPERATIONS,
          _ENIGNEER_OPERATIONS,
          _RIFLEMAN_OPERATIONS,
          _MACHINEGUNNER_OPERATIONS,
          _SCOUT_OPERATIONS,
          ))


def _items_offset(mapping, offset):
    for key, value in mapping.items():
        yield key, value + offset


_GENERAL_OPERATIONS = dict(
    chain(zip(_PSEUDO_OPERATIONS, repeat(None)),
          _items_offset(_BASIC_OPERATIONS, _BASIC_OFFSET),
          _items_offset(_COMBAT_OPERATIONS, _COMBAT_OFFSET),
          _items_offset(_UPGRADE_OPERATIONS, _UPGRADE_OFFSET),
          ))


def _unit_op_map(mapping):
    return dict(chain(_GENERAL_OPERATIONS.items(),
                      _item_offset(mapping, _SPECIAL_OFFSET)))



CAPTAIN_OPERATIONS = _unit_op_map(_CAPTIAN_OPERATIONS)
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
