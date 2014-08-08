BanzaiDB tables schema
======================

The following tables are defined in BanzaiDB -


references
----------

Provides information on a reference used in mapping.

references::

    Elements:
    ---------

    id:             string
    reference_name: string or null
    revision:       int 
    reference_id:   string or null

    Example:
    --------

    [{"id":"NC_008527","reference_name":"Lactococcus lactis subsp. cremoris SK11, complete genome.","revision":1},{"id":"current_reference","reference_id":"NC_008527","revision":1}] 

    $ head NC_008527_1.gbk
    LOCUS       NC_008527            2438589 bp    DNA              CON 27-AUG-2013
    DEFINITION  Lactococcus lactis subsp. cremoris SK11, complete genome.
    ACCESSION   NC_008527
    VERSION     NC_008527.1  GI:116510843
    ...

    Thus: ACCESSION = reference["id"]
          VERSION = reference["id"]+reference["revision"]
          DEFINITION = reference["reference_name"]

    Note: Primary key 'current_reference' is added to keep track of multiple runs


reference_features
------------------

Provides information on the features of a given reference.

Only supports: CDS, gene and xRNA features

reference_features::

    Elements:
    ---------

    end:          int
    id:           string
    locus_tag:    string
    product":     string
    reference_id: string
    sequence:     string
    start:        int
    strand:       int
    translation:  string or null

    Example:
    --------

    1) CDS
    
    {
    "end": 12450 ,
    "id":  "NC_008527.1_LACR_0008_CDS" ,
    "locus_tag":  "LACR_0008" ,
    "product":  "XRE family transcriptional regulator" ,
    "reference_id":  "NC_008527.1" ,
    "sequence":  "ATGGAAATATCCGAAATAATCAAAGAAAATCGTAAACTCAAAAATCTCAGTCAGGAAGAGTTAGCAAAGGAACTACACATCTCTCGTCAATCTATCTTAAAATGGGAGACAGGAAAATCACTTCCCACCACAGACCAACTTATCTTACTCAGTGAAATTTTCGATTGTTCTTTGGACACGTTGCTCAAAGGTGACAAAAAAATGGAAGAAAAAGTAAAACATGAAATTGATGACAAACGGACCTTAAAGTTAATTTATAAGGTTGGTTGGGGTTTTATTGTTCCCTTACTTTTTATTTTGAAATTTGTTTTACATTTGTTTTGA" ,
    "start": 12126 ,
    "strand": 1 ,
    "translation":  "MEISEIIKENRKLK

    2) gene  

    {
    "end": 24970 ,
    "id":  "NC_008527.1_LACR_0018_gene" ,
    "locus_tag": null ,
    "product": null ,
    "reference_id":  "NC_008527.1" ,
    "sequence":  "ATGAATAACAACAAACAACCAAGACAAGGAAATTTTGTAAAAAATATCTTAATGTGGGTTATATTGGCTATTGTTGTTGTTGTCGGTTTCAATTTCTTCTTCAGTAGTAATCAATCAGGAGTGGATAAAATTAGCTATTCACAATTGATGACTAAACTTGATGATAATAATATTGAAAACGTCACAATGCAACCATCAGATAGCTTAATTACTGTAACAGGTGAGTATAAAAAACCTGTAAAGGTAAAAGGAAAAAACAATTTCCCACTTTTAGGTAATACTACAAGTGAAGTTAAAAACTTCCAAGCTTATATTATTCCAACTGACAGTGTTGTCAAAGATATCCAAAATGCAGCTAAAAGTAATGATGTAAAACTTAGTGTCGTTCAAGCGTCATCAAGTGGTATGTGGGTTCAAATTCTCTCATATATCATCCCAATGATTTTATTTGTTGGTATCTTCTGGCTCATGATGGGTGGAATGGGCGCTCGTGGCGGAGGCGGCGGTGGAAATCCGATGTCCTTCGGTAAATCTCGTGCTAAACAACAAGATGGTAAAACATCAAAAGTTCGTTTTGCTGATGTTGCCGGTTCTGAAGAGGAAAAACAAGAGCTTGTTGAAGTTGTTGACTTCCTTAAAAATCCGAAAAAATATCACGATTTAGGTGCTCGTATCCCAGCAGGTGTTCTCCTTGAAGGCCCTCCGGGTACAGGGAAAACTTTGCTTGCTAAGGCTGTTGCCGGTGAAGCAGGAGTTCCTTTCTATAGTATCTCAGGTTCTGATTTCGTTGAAATGTTTGTCGGAGTCGGGGCTTCACGTGTTCGTGATTTATTCGAAAATGCGAAGAAAACTGCTCCATCAATCATTTTCATCGATGAAATTGATGCTGTTGGTCGCCAACGTGGTGCAGGTTTAGGTGGGGGTAATGATGAACGTGAACAAACCCTCAACCAATTGCTTGTTGAAATGGATGGATTCCAAGACGATGGAAACTCAGTAATCGTTATCGCTGCAACTAACCGTTCAGATGTGCTTGACCCAGCGCTTTTACGTCCAGGTCGTTTTGACCGTAAAGTCTTGGTCGGAGCACCAGATGTTAAAGGTCGTGAAGCTGTCCTTAAAGTTCATGCTAAAAACAAACCTTTAGCAAGTGATGTTGATTTACACACTGTTGCTACACAAACTCCTGGTTATGTCGGAGCTGATTTGGAAAATGTTTTGAATGAAGCTGCTCTTGTTGCTGCACGTCAAAATAAAAAAGAAATCAATGCTGCTGATATTGATGAAGGAATGGACCGTGCAATGGCTGGTCCTGCTAAGAAAGATCGTATTCAATCAATGCGTGAGCGTGAAATCGTGGCTTATCACGAAGCAGGTCATGCTATTGTTGGTCTCGTTCTTGAAAATGGATCTACTGTTCGTAAAGTTACCGTTGTCCCTCGTGGACGTATCGGTGGTTACATGCTAGCTCTTCCAGATGAAGAAATCATGCAACCAACTAATCTTCATCTTCAAGACCAACTTGCCAGCCTTATGGGTGGACGACTTGGTGAAGAAATTGTCTTTGGTGTAGCTACTCCAGGTGCATCAAATGACATTGAAAAAGCAACACACATTGCTCGTTCAATGGTAACTGAATATGGGATGTCTAAGAAACTTGGTATGGTATCTTATGAAGGAGACCATCAAGTATTTATCGGCCGTGACTATGGTCAGACTAAGACTTACTCAGAAGCTACTGCTGTTATGATTGATGATGAAGTGCGTCGTATTCTTGGTGAAGCTTATGACCGTGCTAAAGAAGCAATTGAAACACATCGTGAACAACATAAAGCAATTGCGCAAGCTCTGCTTAAATACGAAACGCTCGATGCGAAACAAATCATGTCGCTCTTTACAACAGGTAAAATGCCTGATGAAGCAGCTGCATCAGAAGTACCAGAACCAAAAACATTTGAAGAATCTCTCAAAGATGCAAATGCGAATGTTGATGATTTTTCAAACATTAATATCTATAATGGTGAAGAAAAAACAGATTCTAAACCAGAAGAAAATAAGGAAAAATCAGAAGATGAAACAGCCAATTAA" ,
    "start": 22882 ,
    "strand": 1 ,
    "translation": null
    }

    3) xRNA

    {
    "end": 25518 ,
    "id":  "NC_008527.1_25445-25518" ,
    "locus_tag": null ,
    "product":  "tRNA-Phe" ,
    "reference_id":  "NC_008527.1" ,
    "sequence":  "GGCTCGGTAGCTCAGTTGGTAGAGCAATGGATTGAAGCTCCATGTGTCGGCGGTTCGATTCCGTCTCGCGCCA" ,
    "start": 25445 ,
    "strand": 1 ,
    "translation": null
    }
    

strains_under_investigation
---------------------------

Provides information on the strains in this study.

strains_under_investigation::

    Elements:
    ---------
    
    StrainID: string
    VarCount: int   
    id:       string
    
    Example:
    -------- 
    
    {
    "StrainID":  "ASCC880397" ,
    "VarCount": 40797 ,
    "id":  "ASCC880397"
    }


determined_variants
-------------------

Provides information on the variants called for a mapping run.

determined_variants::

    Elements:
    ---------

    CDSAANum:         int
    CDSBaseNum:       int
    CDSRegion:        string
    ChangeAA:         char
    ChangeBase:       char
    Class:            string
    CorrelatedChange: boolean
    Evidence:         dict
    LocusTag:         string
    Position:         int
    Product:          string
    RefAA:            char
    RefBase:          char
    StrainID:         string
    SubClass:         string
    UncalledBlock:    boolean
    id:               string

    Example:
    --------

    [{"CDSAANum":null,"CDSBaseNum":null,"CDSRegion":null,"ChangeAA":null,"ChangeBase":"A","Class":"substitution","CorrelatedChange":null,"Evidence":{"A":252,"T":1},"LocusTag":null,"Position":100230,"Product":null,"RefAA":null,"RefBase":"T","StrainID":"ASCC880030","SubClass":null,"UncalledBlock":true,"id":"ASCC880030_NC_008527_100230"}
