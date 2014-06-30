from context import converters
from context import errors

import unittest


class ConvertersTest(unittest.TestCase):
    """
    Test the data format conversion tools
    """

    def test_convert_from_JSON_to_CSV_defaults(self):
        """
        Test the JSON to CSV with defaults
        """
        json = {"id": 3232, "name": "Mitch", "email": "m.stantoncook@gmail.com"}
        tmp = converters.convert_from_JSON_to_CSV(json)
        expect = 'm.stantoncook@gmail.com,Mitch,3232'
        self.assertEqual(tmp, expect)

    def test_convert_from_JSON_to_CSV_header_true(self):
        """
        Test the JSON to CSV and get the header aswell
        """
        json = {"id": 3232, "name": "Mitch", "email": "m.stantoncook@gmail.com"}
        tmp = converters.convert_from_JSON_to_CSV(json, header=True)
        expect = 'email,name,id\nm.stantoncook@gmail.com,Mitch,3232'
        self.assertEqual(tmp, expect)

    def test_convert_from_JSON_to_CSV_nested_JSON(self):
        """
        Test that we handle nested JSON gracefully
        """
        json = {"id": 3232, "names": {"firstname": "Mitch", "lastname": "Stanton-Cook"}, "email": "m.stantoncook@gmail.com"}
        with self.assertRaises(errors.NestedJSONError):
            converters.convert_from_JSON_to_CSV(json)

    def test_convert_from_JSON_to_CSV_multi_element(self):
        """
        Test that we handle multi JSON gracefully
        """
        json = [{"id": 3233, "name": "Mitch", "email": "m.stantoncook@gmail.com"}, {"id": 3233, "name": "Nouri", "email": "nbz@gmail.com"}]
        with self.assertRaises(errors.CouldNotParseJSONError):
            converters.convert_from_JSON_to_CSV(json)

    def test_convert_from_csv_to_JSON_stub(self):
        """
        The convert_from_csv_to_JSON is a STUB. This test will fail when it

        is updated flagging need to write new TestCases
        """
        input_csv = ('name, idea, date\nMitch, "Check , work",26-6-14')
        with self.assertRaises(SystemExit) as cm:
            converters.convert_from_csv_to_JSON(input_csv)
        self.assertEqual(cm.exception.code, 1)


if __name__ == '__main__':
    # Buffer turns off any print statements
    unittest.main(buffer=True)
    # , verbosity=2)
