"""Defining the raw key value pairs for op_code."""


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


_UPGRADE_OFFSET = 64


_UPGRADE_OPERATIONS = {
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
