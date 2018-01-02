"""Syntax Nodes and conversion from parse tree to syntax tree."""


from grammar import (
    VNSSymbols,
    )
from op_code import (
    SECTION_OPERATIONS,
    )


# I don't support them yet, but I will need to think about context for
# identifiers. I might also need to construct null object nodes, which will
# not be constructed from parse nodes.


def to_node(parse_node, override_type=None):
    if parse_node is None:
        return None
    elif override_type is None:
        return _symbol_node_types[parse_node.symbol](parse_node)
    else:
        return override_type(parse_node)

_symbol_node_types = {}


class SyntaxNode:
    """Abstract base class for SyntaxNodes."""

    # __new__ as node type dispatcher?

    def __init__(self, parse_node):
        self.parse_node = parse_node

    def write(self, file=sys.stdout):
        print(str(self), file=file)

    def __str__(self):
        raise NotImplementedError()

    def __repr__(self):
        return '{}(parse_node={!s})'.format(
            type(self).__name__, self.parse_node)


class OperationNode(SyntaxNode):

    def __init__(self, parse_node):
        super().__init__(parse_node)
        self.operation = parse_node.children[0]
        self.args = self._build_args(self.parse_node)

    @classmethod
    def _build_args(cls, node):
        arg_list = []
        for child in parse_node.children:
            if VNSSymbols.ARGUMENT is child.symbol:
                arg_list.append(to_node(child))
            elif VNSSymbols.ARG_TAIL is child.symbol:
                arg_list.extend(cls._build_args(child))
        return arg_list

    def __str__(self):
        return str(self.operation) + ' ' + ', '.join(map(str, self.args))


def _get_register_default(args, i):
    try:
        return args[i]
    except IndexError:
        # Construct a fake 'r0' value.
        return None


def _get_immediate_default(args, i):
    try:
        return args[i]
    except IndexError:
        # Construct a fake '0' value.
        return None


class OperationABCSNode(OperationNode):

    def __init__(self, parse_node):
        super().__init__(parse_node)

    @property
    def register_a(self):
        return _get_register_default(self.args, 0)

    @property
    def register_b(self):
        return _get_register_default(self.args, 1)

    @property
    def register_c(self):
        return _get_register_default(self.args, 2)

    @property
    def small_immediate(self):
        return _get_immediate_default(self.args, 3)


class OperationAINode(OperationNode):

    def __init__(self, parse_node):
        super().__init__(parse_node)

    @property
    def register_a(self):
        return _get_register_default(self.args, 0)

    @property
    def immediate(self):
        return _get_immediate_default(self.args, 1)


#   if 'A' in self.format:
#       self.register_a = RegisterGetter(0)
#   elif 'a' in self.format:
#       self.register_a = RegisterGetter(0, optional=True)
#   if 'B' in self.format:
#       self.register_b = RegisterGetter(1)
#   elif 'b' in self.format:
#       self.register_b = RegisterGetter(1, optional=True)
#   if 'C' in self.format:
#       self.register_c = RegisterGetter(2)
#   elif 'c' in self.format:
#       self.register_c = RegisterGetter(2, optional=True)


class TerminalSyntaxNode(SyntaxNode):

    def __str__(self):
        return self.parse_node.text


class RegisterNode(TerminalSyntaxNode):
    pass


class IntegerNode(TerminalSyntaxNode):

    def __int__(self):
        return int(str(self))
