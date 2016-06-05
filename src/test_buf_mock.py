
class BuffMock(object):
    main_buffer = []
    current_line = 0
    current_letter = 0

    def __init__(self, lst, _y, _x):
        self.main_buffer = lst
        self.current_line = _y
        self.current_letter = _x
    
    def __iter__(self):
        return iter(self.main_buffer)

    def __len__(self):
        return len(self.main_buffer)

    def __str__(self):
        return str(self.main_buffer)

    # support indexing
    def __getitem__(self, index):
        return self.main_buffer[index]

    def __setitem__(self, index, value):
        self.main_buffer[index] = value

    def append(self, string):
        """ interface to underlying structure of list """
        self.main_buffer.append(string)

    def insert(self, index, value):
        """ interface to underlying list """
        self.main_buffer.insert(index, value)

    def remove(self, value):
        """ remove first occurance of value. Raises ValueError when no value is
        present """
        self.main_buffer.remove(value)
