from context import config

import unittest
import mock
import os
import sys


class ConfigTest(unittest.TestCase):
    """
   Test the config reader/setter
    """

    def test_config_read_config_default(self):
        """
        Test reading a config object using defaults (empty config file)
        """
        # For the file open recipie see:
        # http://www.voidspace.org.uk/python/mock/helpers.html#mock-open
        m = mock.mock_open(read_data='')
        with mock.patch('__builtin__.open', m, create=True):
            cfg = config.BanzaiDBConfig()
            # m.assert_called_once_with('/Users/mscook/.BanzaiDB.cfg')
            self.assertEqual(cfg['db_host'], 'localhost')
            self.assertEqual(cfg['port'], 28015)
            self.assertEqual(cfg['db_name'], 'Banzai')
            self.assertEqual(cfg['auth_key'], '')

    def test_config_read_config_overrides(self):
        """
        Test reading a config object with user overrides
        """
        cfg_data = '\n'.join(['db_host = 152.0.0.1', 'port = 99999',
                              'db_name = test'])
        m = mock.mock_open(read_data=cfg_data)
        with mock.patch('__builtin__.open', m, create=True):
            # Why below -
            # bash-shell.net/blog/2014/feb/27/file-iteration-python-mock
            m.return_value.__iter__.return_value = cfg_data.splitlines()
            cfg = config.BanzaiDBConfig()
            # m.assert_called_once_with('/Users/mscook/.BanzaiDB.cfg')
            self.assertEqual(cfg['db_host'], '152.0.0.1')
            self.assertEqual(cfg['port'], 99999)
            self.assertEqual(cfg['db_name'], 'test')
            self.assertEqual(cfg['auth_key'], '')

    def test_config_get_items(self):
        """
        Test getting config options
        """
        # For the file open recipie see:
        # http://www.voidspace.org.uk/python/mock/helpers.html#mock-open
        m = mock.mock_open(read_data='')
        with mock.patch('__builtin__.open', m, create=True):
            cfg = config.BanzaiDBConfig()
            # m.assert_called_once_with('/Users/mscook/.BanzaiDB.cfg')
            self.assertEqual(cfg['not_there'], None)
            self.assertEqual(cfg['db_host'], 'localhost')

    def test_config_set_items(self):
        """
        Test setting config options
        """
        # For the file open recipie see:
        # http://www.voidspace.org.uk/python/mock/helpers.html#mock-open
        m = mock.mock_open(read_data='')
        with mock.patch('__builtin__.open', m, create=True):
            cfg = config.BanzaiDBConfig()
            # m.assert_called_once_with('/Users/mscook/.BanzaiDB.cfg')
            cfg['port'] = '6666'
            self.assertEqual(cfg['port'], 6666)
            cfg['db_host'] = 'awesome.server.com'
            self.assertEqual(cfg['db_host'], 'awesome.server.com')
            with self.assertRaises(KeyError):
                cfg['ROW'] = 'blah'


class ConfigTest_no_config_file(unittest.TestCase):
    """
   Test the config reader/setter
    """

    def setUp(self):
        """
        If ~/.BanzaiDB.cfg exists move it
        """
        if os.path.isfile(os.path.expanduser('~/')+'.BanzaiDB.cfg'):
            original_file = os.path.expanduser('~/')+'.BanzaiDB.cfg'
            new_file = original_file+'.test'
            os.system("mv "+original_file+" "+new_file)

    def tearDown(self):
        """
        If ~/.BanzaiDB.cfg.test exists move it
        """
        if os.path.isfile(os.path.expanduser('~/')+'.BanzaiDB.cfg.test'):
            original_file = os.path.expanduser('~/')+'.BanzaiDB.cfg'
            new_file = original_file+'.test'
            os.system("mv "+new_file+" "+original_file)

    def test_config_read_config_no_file(self):
        """
        Test what happens when there is no ~/.BanzaiDB.cfg
        """
        config.BanzaiDBConfig()
        if not hasattr(sys.stderr, "getvalue"):
            self.fail("Need to run in buffered mode")
        output = sys.stderr.getvalue().strip()
        self.assertEquals(output, 'Using RethinkDB defaults')

    def test_config_dump_items(self):
        """
        Check dump_items()
        """
        expected = "db_name = Banzai\ndb_host = localhost\nport = 28015\nauth_key = "
        cfg = config.BanzaiDBConfig()
        self.assertEquals(cfg.dump_items(), expected)


if __name__ == '__main__':
    unittest.main(buffer=True)
