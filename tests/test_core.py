from context import core

import unittest


class CoreTest(unittest.TestCase):
    """
    Test core BanzaiDB methods
    """
    def test_reference_genome_features_to_JSON_reference_JSON(self):
        """
        """
        ref_detail, feat_details = core.reference_genome_features_to_JSON('data/EC958.gbk')
        self.assertEquals(ref_detail['id'], 'HG941718')
        self.assertEquals(ref_detail['revision'], 1)
        self.assertEquals(ref_detail['reference_name'], 'Escherichia coli O25b:H4-ST131 str. EC958 chromosome, complete genome.')

    def test_reference_genome_features_to_JSON_feat_JSON(self):
        ref_detail, feat_details = core.reference_genome_features_to_JSON('data/EC958.gbk')
        CDS_count, gene_count, other_count = 0, 0, 0
        CDS_p, gene_p = 0, 0
        for e in feat_details:
            if e['id'].endswith('_CDS'):
                CDS_count += 1
                if e['product'] == 'pseudo':
                    CDS_p += 1
            elif e['id'].endswith('_gene'):
                gene_count += 1
                if e['product'] == 'pseudo':
                    gene_p += 1
            else:
                other_count += 1
        self.assertEquals(CDS_count, 4981)
        self.assertEquals(gene_count, 4981)
        self.assertEquals(other_count, 89+22+1)
        self.assertEquals(CDS_p, 25)
        self.assertEquals(gene_p, 25)


if __name__ == '__main__':
    unittest.main(buffer=True)
