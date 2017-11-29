"""Definition of language's actual grammer."""


import enum

from node import NodeSymbol


START = NodeSymbol.START
INSTRUCTION = NodeSymbol.INSTRUCTION
Operation = NodeSymbol.Operation
Register = NodeSymbol.Register
Integer = NodeSymbol.Integer
Comma = NodeSymbol.Comma


S_INST = Rule(START, (INSTRUCTION))
INST_OP = Rule(INSTRUCTION, (Operation))
INST_OA = Rule(INSTRUCTION, (Operation, Register))
INST_OAI = Rule(INSTRUCTION, (Operation, Register, Comma, Integer))
INST_OABC = Rule(
    INSTRUCTION, (Operation, Register, Comma, Register, Comma, Register))


ALL_RULES = (S_INST, INST_OP, INST_OA, INST_OAI, INST_OABC)
