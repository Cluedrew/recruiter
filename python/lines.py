"""Lines of code."""


import node


FIRST_ROW = 1
FIRST_COL = 1


def iter_logical_lines(source_name):
    for physical_line in iter_physical_lines(source_name):
        yield LogicalLine([physical_line])


class LogicalLine:

    def __init__(self, physical):
        self._physical = physical

    def __iter__(self):
        # This one is not a mere loop, we break up the strings into
        # non-terminal symbols as we go.
        text = ' '.join(map(lambda l: l.strip_comment(), self._physical))
        yield from node.iter_terminals_from_str(text)


def iter_physical_lines(file_name):
    with open(file_name) as file:
        for num, line in enumerate(file, start=FIRST_ROW):
            yield PhysicalLine(line, file_name, num)


class PhysicalLine:

    def __init__(self, text, file_name, line_number):
        self.text = text
        self.file_name = file_name
        self.line_number = line_number

    def strip_comment(self) -> str:
        return self.text.split(';', 1)[0]
