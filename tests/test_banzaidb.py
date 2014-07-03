from context import banzaidb

import unittest


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
        init
        """
        with self.assertRaises(SystemExit) as cm:
            parsed  = self.parser.parse_args(['init'])
            self.assertEquals(parsed.force, False)
        self.assertEquals(cm.exception.code, 0)

    def test_init_parser_force(self):
        """
        init --force
        """
        with self.assertRaises(SystemExit) as cm:
            results = self.parser.parse_args(['init', '--force'])
            print results.force
        self.assertEqual(cm.exception.code, 0)


if __name__ == '__main__':
    # unittest.main()
    unittest.main(buffer=True)
