    cfg = config.BanzaiDBConfig()
    try:
        connection = r.connect(host=cfg['db_host'], port=cfg['port'],
                            db=cfg['db_name'])
    except RqlDriverError:
        print "No database connection could be established."
    exit()
    ### Howto plot SNPS
    ##SNP_positions = query_functions.get_SNP_positions(cfg, 'S77EC', [1, 1000000])
    ##feat = []
    ##for pos in SNP_positions:
    #    feat.append(misc.create_feature(pos, pos, "SNP", strand=None))
    ##imaging.plot_SNPs(feat)
    ### Howto get CDS core alignment
    query_functions.get_core_alignment(cfg)
    sys.exit()
    if not os.path.isfile(cfg['db_all']+'.ns'):
        print "Database missing. Please use create"
        sys.exit(1)
    if args.mongo != '':
        pass
    elif args.locus_tag != '':
        from collections import Counter
        # Get all required collections
        snp_coll = database.get_collection(cfg, 'VARIANTS')
        ref_features_coll = database.get_collection(cfg, 'REF_FEAT')
        strains_coll = database.get_collection(cfg, 'STRAINS')
        # Get all stored strains and store
        strains = []
        for strain in strains_coll.find({}, {"StrainID" : 1, "_id" : 0}):
            strains.append(strain.values()[0])
        # Get the CDS sequence, product for refernce(LocusTag) and store
        dat = ref_features_coll.find_one({"LocusTag": args.locus_tag}, {"Sequence" : 1, "Product" : 1, "_id" : 0})
        sequence = list(dat['Sequence'])
        product  = dat['Product']
        # Find all SNPs with given LocusTag for given strain. Use PQL
        for strain in strains:
            occur_pos, occur_type, occur_stype, occur_strain = [], [], [], []
            query =  pql.find("StrainID == '"+strain+"' and LocusTag == '"+args.locus_tag+"'")
            # Build up the allele sequence
            cur_seq = list(sequence)
            for idx, snp in enumerate(snp_coll.find(query)):
                # Sanity check
                #print snp
                if snp['RefBase'] != sequence[snp['CDSBaseNum']-1]:
                    print "Error- Sanity check failed"
                else:
                    cur_seq[snp['CDSBaseNum']-1] = snp['ChangeBase']
            print ">%s %s (%s)" % (strain, args.locus_tag, product)
            print ''.join(cur_seq)
