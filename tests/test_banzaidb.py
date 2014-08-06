from context import banzaidb

import unittest
import mock

class BanzaiDBTest(unittest.TestCase):
    """
    Test the exceptions
    """

    def setUp(self):
        self.parser = banzaidb.create_parser()

    def test_create_parser_no_args(self):
        """
        Should exit throwing exception
        """
        with self.assertRaises(SystemExit) as cm:
            parsed = self.parser.parse_args([])
            # Should test all the defaults here..
            self.assertEquals(parsed.verbose, False)
            self.assertEquals(cm.exception.code, 2)

    def test_create_parser_help_args(self):
        """
        -h flag. Print help & exit cleanly
        """
        with self.assertRaises(SystemExit) as cm:
            self.parser.parse_args(['-h'])
            # Not sure below is working
            self.assertEquals(cm.exception.code, 0)

    def test_create_parser_verbose_args(self):
        """
        -v flag. Makes no sense. Exit with exception
        """
        with self.assertRaises(SystemExit) as cm:
            parsed = self.parser.parse_args(['-v'])
            self.assertEquals(parsed.verbose, True)
            # Not sure below is working
            self.assertEquals(cm.exception.code, 2)

    def test_create_parser_help_verbose_args(self):
        """
        -h, -v flag. Exit cleanly
        """
        with self.assertRaises(SystemExit) as cm:
            parsed = self.parser.parse_args(['-h', '-v'])
            self.assertEquals(parsed.verbose, True)
            # Not sure below is working
            self.assertEquals(cm.exception.code, 0)

    def test_create_parser_choices_init(self):
        """
        init -h
        """
        with self.assertRaises(SystemExit) as cm:
            self.parser.parse_args(['init', '-h'])
        self.assertEqual(cm.exception.code, 0)

    def test_create_parser_choices_populate(self):
        """
        populate -h
        """
        with self.assertRaises(SystemExit) as cm:
            self.parser.parse_args(['populate', '-h'])
        self.assertEqual(cm.exception.code, 0)

    def test_create_parser_choices_update(self):
        """
        update -h
        """
        with self.assertRaises(SystemExit) as cm:
            self.parser.parse_args(['update', '-h'])
        self.assertEqual(cm.exception.code, 0)

    def test_create_parser_choices_query(self):
        """
        query -h
        """
        with self.assertRaises(SystemExit) as cm:
            self.parser.parse_args(['query', '-h'])
        self.assertEqual(cm.exception.code, 0)

    # Specific Init tests

    def test_init_parser(self):
        """
        init parser methods -> don't know why not returning expected error
        statuses or if I even need to mock here
        """
        initdb = mock.Mock()
        initdb.return_value = True
        # with self.assertRaises(Exception) as cm:
        with mock.patch('BanzaiDB.banzaidb.init_database_with_default_tables', initdb):
            results = self.parser.parse_args(['init'])
            self.assertEquals(results.force, False)

        # self.assertEquals(cm.exception.code, 1)

        # with self.assertRaises(SystemExit) as cm:
        with mock.patch('BanzaiDB.banzaidb.init_database_with_default_tables', initdb):
            results = self.parser.parse_args(['init', '--force'])
            self.assertEquals(results.force, True)
        # self.assertEqual(cm.exception.code, 0)

    def test_init_database_with_default_tables(self):
        """
        Test the DB initalization methods
        """
        connection = mock.Mock()
        connection.__enter__ = mock.Mock(return_value='We have a mocked connection')
        connection.__exit__ = mock.Mock(return_value=False)
        args = self.parser.parse_args(['init'])
        with mock.patch('BanzaiDB.database.make_connection', connection):
            banzaidb.init_database_with_default_tables(args)

if __name__ == '__main__':
    #unittest.main()
    unittest.main(buffer=True)
