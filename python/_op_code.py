"""Defining the raw key value pairs for op_code.

This module should be considered an implementation detail of op_code
and so should never be used outside that module.

The operation dictionaries all store Tuple[Optional[int], str]. The
integer is the op-code of the instruction, Pseudo operations have
None as they do not have a particular op-code. The string is the
format of instruction, showing what arguments it takes.

Letters indicate the type of each argument and are listed in the
order they appear.

O: Operation, implied at the start of all formats (7-bits unsigned)
A,B,C: The first, second and third registers. Currently provided
seperately for visual differentation. (5-bits unsigned each)
I: Immediate value (20-bits unsigned)
L: Long immediate value (32-bits unsigned)
S: Short immediate value (10-bits signed)
"""

# TODO: Consider lower case letters as optional arguments:
# +   Allows any command to be filled, with extra data if wanted.
#     Which is currently possible only for ABCS, AI & L commands.
# +   Operations like MOV, which often don't care about all their arguments
#     (the arival location is often ignored) can declare them optional.


_BASIC_OPERATIONS = {
    'ADD': (0, 'ABCS'),
    'SUB': (1, 'ABCS'),
    'MUL': (2, 'ABCS'),
    'DIV': (3, 'ABCS'),
    'AND': (4, 'ABCS'),
    'ORR': (5, 'ABCS'),
    'XOR': (6, 'ABCS'),
    'NAN': (7, 'ABCS'),
    'CLZ': (8, 'ABCS'),
    'CNT': (9, 'ABCS'),
    'LSR': (10, 'ABCS'),
    'LSL': (11, 'ABCS'),
    'ABS': (12, 'ABCS'),
    'RND': (13, 'ABCS'),
    'CMP': (14, 'ABCS'),
    'JIZ': (15, 'AI'),
    'JNZ': (16, 'AI'),
    'JGZ': (17, 'AI'),
    'JLZ': (18, 'AI'),
    'JGE': (19, 'AI'),
    'JLE': (20, 'AI'),
    'BIZ': (21, 'AI'),
    'BNZ': (22, 'AI'),
    'BGZ': (23, 'AI'),
    'BLZ': (24, 'AI'),
    'BGE': (25, 'AI'),
    'BLE': (26, 'AI'),
    'BLX': (27, 'AI'),
    'LDR': (28, 'ABCS'),
    'STR': (29, 'ABCS'),
    'POP': (30, 'ABCS'),
    'PSH': (31, 'ABCS'),
    }


_COMBAT_OPERATIONS = {
    'WHO': (32, 'ABCS'),
    'WHT': (33, 'ABCS'),
    'QCS': (34, 'ABCS'),
    'QCT': (35, 'ABCS'),
    'QBP': (36, 'ABCS'),
    'QCK': (37, 'ABCS'),
    'GND': (38, 'ABCS'),
    'WHR': (39, 'ABCS'),
    'DST': (40, 'ABCS'),
    'CVR': (41, 'ABCS'),
    'DED': (42, 'ABCS'),
    'SHT': (43, 'ABCS'),
    'DIR': (44, 'ABCS'),
    'WLK': (45, 'ABCS'),
    'CRL': (46, 'ABCS'),
    'SWM': (47, 'ABCS'),
    'CAP': (48, ''),
    'LIN': (49, ''),
    'HID': (50, 'AI'),
    'SAY': (51, 'AI'),
    'RAD': (52, 'AI'),
    'YEL': (53, 'AI'),
    'EAR': (54, 'AI'),
    'DIE': (55, 'ABCS'),
    'NRT': (56, 'ABCS'),
    'NRE': (57, 'ABCS'),
    'EST': (58, 'ABCS'),
    'SOE': (59, 'ABCS'),
    'SOT': (60, 'ABCS'),
    'SOW': (61, 'ABCS'),
    'WST': (62, 'ABCS'),
    'NRW': (63, 'ABCS'),
    }


_UPGRADE_OPERATIONS = {
    'WCS': (64, 'A'),
    'WCT': (65, 'A'),
    'WBP': (66, 'A'),
    'WCL': (67, 'A'),
    'TCS': (68, 'AI'),
    'TCT': (69, 'AI'),
    'TBP': (70, 'AI'),
    'TCL': (71, 'AI'),
    'PNT': (72, 'A'),
    'CCS': (73, 'A'),
    'CCT': (74, 'A'),
    'CBP': (75, 'A'),
    'CCL': (76, 'A'),
    'UCS': (77, 'A'),
    'UCT': (78, 'A'),
    'UBP': (79, 'A'),
    'UCL': (80, 'A'),
    'DCS': (81, 'A'),
    'DCT': (82, 'A'),
    'DBP': (83, 'A'),
    'DCL': (84, 'A'),
    'MCS': (85, 'A'),
    'MCT': (86, 'A'),
    'MBP': (87, 'A'),
    'MCL': (88, 'A'),
    'RCS': (89, 'A'),
    'RCT': (90, 'A'),
    'RBP': (91, 'A'),
    'RCL': (92, 'A'),
    'TIM': (93, 'ABCS'),
    'DLY': (94, ''),
    'ADV': (95, ''),
    }


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


_PSEUDO_OPERATIONS = {
    'RAW': (None, 'L'),
    }
