"""Context-Free Grammer Parsing Rules"""

# See cfg.py


from collections import namedtuple

from node import NodeSymbol


START = NodeSymbol.START
INSTRUCTION = NodeSymbol.INSTRUCTION
Operation = NodeSymbol.Operation
Register = NodeSymbol.Register
Integer = NodeSymbol.Integer
Comma = NodeSymbol.Comma


# TODO: On Python 3.6: typing.NamedTuple is prettier and typed.
Rule = namedtuple('Rule', ['head', 'children'])


S_INST = Rule(START, (INSTRUCTION))
INST_OP = Rule(INSTRUCTION, (Operation))
INST_OA = Rule(INSTRUCTION, (Operation, Register))
INST_OAI = Rule(INSTRUCTION, (Operation, Register, Comma, Integer))
INST_OABC = Rule(
    INSTRUCTION, (Operation, Register, Comma, Register, Comma, Register))


ALL_RULES = (S_INST, INST_OP, INST_OA, INST_OAI, INST_OABC)
