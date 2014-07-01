from context import database
from context import errors

import unittest
import mock


class DatabaseTest(unittest.TestCase):
    """
   Test the database methods
    """

    def test_make_connection_badname(self):
        """
        Test what happens when we provide an invalid RethinkDB database name
        """
        cfg_data = '\n'.join(['db_name = .test'])
        m = mock.mock_open(read_data=cfg_data)
        with mock.patch('__builtin__.open', m, create=True):
            # Why below -
            # bash-shell.net/blog/2014/feb/27/file-iteration-python-mock
            m.return_value.__iter__.return_value = cfg_data.splitlines()
            with self.assertRaises(errors.InvalidDBName):
                database.make_connection()
            # m.assert_called_once_with('/Users/mscook/.BanzaiDB.cfg')


if __name__ == '__main__':
    unittest.main()
