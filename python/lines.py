"""Lines of code."""


from pathlib import Path


import node


FIRST_ROW = 1
FIRST_COL = 1


class SourceFile:
    """Wrapper around a source code file."""

    def __init__(self, path):
        self.path = path

    @staticmethod
    def from_name(name):
        """Create a source file wrapper from the file name.

        name is relative to the present/current working directory.
        """
        return SourceFile(Path(name).resolve())

    def include(self, name):
        """Include a new source file from this one.

        Same as from_name, but if the file is not found, ties searching
        from self's directory.
        """
        try:
            return self.from_name(name)
        except FileNotFoundError:
            try:
                return type(self)(Path(self.path.parent, name).resolve())
            except FileNotFoundError:
                pass
            raise

    def _iter_physical(self):
        with self.path.open() as file:
            for num, line in enumerate(file, start=FIRST_ROW):
                yield PhysicalLine(line, str(self.path), num)

    def __iter__(self):
        """Return an iterator that produces each logical line in the file."""
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


class PhysicalLine:

    def __init__(self, text, file_name, line_number):
        self.text = text
        self.file_name = file_name
        self.line_number = line_number

    def strip_comment(self) -> str:
        return self.text.split(';', 1)[0]
