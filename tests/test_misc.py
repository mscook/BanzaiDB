from context import misc

import unittest


class MiscTest(unittest.TestCase):
    """
    Test misc BanzaiDB methods
    """

    def test_create_a_genomic_feature(self):
        """
        Create a genomic feature
        """
        res = misc.create_feature(1, 10, "insertion")
        self.assertEquals(res.strand, None)
        self.assertEquals(res.type, "insertion")
        self.assertEquals(res.location.start, 1)
        self.assertEquals(res.location.end, 10)
        res = misc.create_feature(30, 30, "substitution")
        self.assertEquals(res.location.start, 30)
        self.assertEquals(res.location.end, 30)
        res = misc.create_feature(41, 41, "substitution", -1)
        self.assertEquals(res.location.strand, -1)
        with self.assertRaises(ValueError):
            misc.create_feature(100, 200, "deletion", "forward")

if __name__ == '__main__':
    unittest.main()
