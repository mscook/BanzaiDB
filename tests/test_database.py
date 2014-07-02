from context import database
from context import errors
from rethinkdb.errors import RqlDriverError

import unittest
import mock


class DatabaseTest(unittest.TestCase):
    """
   Test the database methods
    """

    def test_make_connection_badname(self):
        """
        Test what happens when we provide an invalid RethinkDB database name
        RethinkDB names must be -
            lowercase letters, uppercase letters, and numbers and underscore
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

    def test_make_connection_noconnection(self):
        """
        Make a call to a non-existant rethinkDB instance

        TODO: Too slow. Refactor with mocks!
        """
        cfg_data = '\n'.join(['db_name = nonexistant', 'db_host = 6.6.6.6'])
        m = mock.mock_open(read_data=cfg_data)
        with mock.patch('__builtin__.open', m, create=True):
            # Why below -
            # bash-shell.net/blog/2014/feb/27/file-iteration-python-mock
            m.return_value.__iter__.return_value = cfg_data.splitlines()
            with self.assertRaises(RqlDriverError):
                database.make_connection()
            # m.assert_called_once_with('/Users/mscook/.BanzaiDB.cfg')

    def test_make_connection_make_connection(self):
        """
        Make a connection. We mock out the actual connection
        """
        r_connect = mock.Mock()
        r_connect.return_value = True
        #r_connect.side_effect = RuntimeError("No touching RethinkDB - "
        #                                        "Mocked connection made")
        cfg_data = '\n'.join(['db_name = mocked'])
        m = mock.mock_open(read_data=cfg_data)
        with mock.patch('__builtin__.open', m, create=True):
            with mock.patch('rethinkdb.connect', r_connect):
                # Why below -
                # bash-shell.net/blog/2014/feb/27/file-iteration-python-mock
                m.return_value.__iter__.return_value = cfg_data.splitlines()
                self.assertEquals(database.make_connection(), True)
                # m.assert_called_once_with('/Users/mscook/.BanzaiDB.cfg')


if __name__ == '__main__':
    unittest.main()
