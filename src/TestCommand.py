""" This is a unit test program for commands """

import unittest

from Command import Delete, Insert, Replace
from test_buf_mock import BuffMock


class TestDelete(unittest.TestCase):

    def setUp(self):
        self.list = ['To jest pierwsza', 'linijka', 'czy cos']

    def test_delete_line(self):
        self.buffer = BuffMock(self.list, 1, 0)
        _del = Delete(self.buffer, 'd')
        lista = ['To jest pierwsza', 'czy cos']
        _del.execute()
        self.assertEqual(lista, self.buffer.main_buffer)
        _del.undo()
        self.assertEqual(self.buffer.main_buffer, self.list)

    def test_delete_end(self):
        self.buffer = BuffMock(self.list, 0, 2)
        _del = Delete(self.buffer, 'D')
        lista = ['To', 'linijka', 'czy cos']
        _del.execute()
        self.assertEqual(lista, self.buffer.main_buffer)
        _del.undo()
        self.assertEqual(self.list, self.buffer.main_buffer)

    def test_delete_current(self):
        self.buffer = BuffMock(self.list, 0, 2)
        lista = ['Tojest pierwsza', 'linijka', 'czy cos']
        _del = Delete(self.buffer, 'l')
        _del.execute()
        self.assertEqual(lista, self.buffer.main_buffer)
        _del.undo()
        self.assertEqual(self.list, self.buffer.main_buffer)

    def test_delete_before(self):
        self.buffer = BuffMock(self.list, 0, 4)
        lista = ['To est pierwsza', 'linijka', 'czy cos']
        _del = Delete(self.buffer, 'h')
        _del.execute()
        self.assertEqual(lista, self.buffer.main_buffer)
        _del.undo()
        self.assertEqual(self.list, self.buffer.main_buffer)

class TestInsert(unittest.TestCase):

    def setUp(self):
        self.old_buffer = []
        self.new_buff = ['Tekst', 'Drugi tekst', 'Trzeci tekst']

    def test_initial(self):
        _ins = Insert(self.old_buffer, self.new_buff)
        _ins.execute()
        self.assertEqual(self.old_buffer, self.new_buff)
        _ins.undo()
        self.assertEqual(self.old_buffer, [])

    def test_other_initial(self):
        self.old_buffer = []
        new_buff = ['', 'Tekst', '', 'I tekst']
        _ins = Insert(self.old_buffer, new_buff)
        _ins.execute()
        self.assertEqual(self.old_buffer, new_buff)
        _ins.undo()
        self.assertEqual(self.old_buffer, [])

    def test_some_data_already(self):
        self.old_buffer = ['To sa', 'calkiem ', 'stare', 'dane']
        lista = ['To sa', 'dodatkowe dane','', 'calkiem ','rozne od tych','' ,'starych', 'danych']
        _ins = Insert(self.old_buffer, lista)
        _ins.execute()
        self.assertEqual(self.old_buffer, lista)
        _ins.undo()
        self.assertEqual(self.old_buffer, ['To sa', 'calkiem ', 'stare', 'dane'])


class TestReplace(unittest.TestCase):

    def setUp(self):
        self.init = ['To jest piekna dluga linijak','ok','dobra','super']
        self.buffor = BuffMock(self.init, 0, 5)

    def test_replace(self):
        from copy import deepcopy
        org_buff = deepcopy(self.buffor.main_buffer)
        ok_buff = ['To jest piekna dluga linijka','ok','dobra','super']
        _rpl = Replace(self.buffor, 'linijak', 'linijka', 0)
        _rpl.execute()
        self.assertEqual(self.buffor.main_buffer, ok_buff)
        _rpl.undo()
        self.assertEqual(self.buffor.main_buffer, org_buff)

    def test_vanish(self):
        from copy import deepcopy
        org_buff = deepcopy(self.buffor.main_buffer)
        ok_buff = ['To jest piekna dluga linijak','','dobra','super']
        _rpl = Replace(self.buffor, 'ok', '', 1)
        _rpl.execute()
        self.assertEqual(ok_buff, self.buffor.main_buffer)
        _rpl.undo()
        self.assertEqual(org_buff, self.buffor.main_buffer)

if __name__ == "__main__":
    unittest.main()
