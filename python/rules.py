"""Context-Free Grammer Parsing Rules"""


from node import NodeSymbol


START = NodeSymbol.START
INSTRUCTION = NodeSymbol.INSTRUCTION
Operation = NodeSymbol.Operation
Register = NodeSymbol.Register
Integer = NodeSymbol.Integer
Comma = NodeSymbol.Comma


# TODO: NamedTuple isn't avaible yet either but I think it would work.
class Rule:

    def __init__(self, head, *children):
        #assert head.is_nonterminal()
        self.head = head
        self.children = children


S_INST = Rule(START, INSTRUCTION)
INST_OP = Rule(INSTRUCTION, Operation)
INST_OA = Rule(INSTRUCTION, Operation, Register)
INST_OAI = Rule(INSTRUCTION, Operation, Register, Comma, Integer)
INST_OABC = Rule(
    INSTRUCTION, Operation, Register, Comma, Register, Comma, Register)


ALL_RULES = (S_INST, INST_OP, INST_OA, INST_OAI, INST_OABC)
