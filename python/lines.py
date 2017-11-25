"""Lines of code."""


FIRST_ROW = 1
FIRST_COL = 1


class LogicalLine:

    def __init__(self, physical):
        self._physical = physical

    def __iter__(self):
        # This one is not a mere loop, we break up the strings into
        # non-terminal symbols as we go.
        pass


def iter_physical_lines(file_path):
    name = str(file_path)
    with file_path.open() as file:
        for num, line in enumerate(file, start=1):
            yield PhysicalLine(line, name, num)


class PhysicalLine:

    def __init__(self, text, file_name, line_number):
        self.text = text
        self.file_name = file_name
        self.line_number = line_number
