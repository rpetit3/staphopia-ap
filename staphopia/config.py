#! /usr/bin/env python
"""
Static variables used throughout the analysis pipeline.

Please note, the Makefile should update BASE_DIR, but if not you will need to.
"""
BASE_DIR = CHANGE_ME

# PATH
PATH = BASE_DIR + '/bin'
PIPELINE_PATH = PATH + '/pipelines'
THIRD_PARTY_PATH = PATH + '/third-party'
PROKKA_PATH = BASE_DIR + '/src/third-party/prokka/binaries/linux'
TOOL_DATA = BASE_DIR + '/tool-data'

# PYTHONPATH
PYTHON_REQS = BASE_DIR + '/src/third-party/python'
VCFANNOTATOR = BASE_DIR + '/src/third-party/python/vcf-annotator'
CALL_VARIANTS = '{0}{1}:{0}{2}:{0}{3}'.format(
    BASE_DIR,
    '/src/third-party/call_variants',
    '/src/third-party/call_variants/src/third-party/python',
    '/src/third-party/call_variants/src/third-party/python/vcf-annotator'
)

# Programs
BIN = {
    # FASTQ related
    'fastq_cleanup': PATH + '/fastq_cleanup',
    'fastq_stats': PATH + '/fastq_stats',
    'fastq_validator': THIRD_PARTY_PATH + '/fastq_validator',

    # Assembly related
    'kmergenie': THIRD_PARTY_PATH + '/kmergenie',
    'velvetg': THIRD_PARTY_PATH + '/velvetg',
    'velveth': THIRD_PARTY_PATH + '/velveth',
    'spades': THIRD_PARTY_PATH + '/spades.py',
    'makeblastdb': THIRD_PARTY_PATH + '/makeblastdb',
    'assemblathon_stats': THIRD_PARTY_PATH + '/assemblathon_stats.pl',

    # MLST related
    'srst2': THIRD_PARTY_PATH + '/srst2.py',
    'blastn': THIRD_PARTY_PATH + '/blastn',

    # SCCmec related
    'tblastn': THIRD_PARTY_PATH + '/tblastn',
    'samtools': THIRD_PARTY_PATH + '/samtools-1.0',
    'genomeCoverageBed': THIRD_PARTY_PATH + '/genomeCoverageBed',

    # SNP/InDel related
    'bwa': THIRD_PARTY_PATH + '/bwa',
    'java': THIRD_PARTY_PATH + '/java',
    'picardtools': '{0}/picard.jar'.format(
        THIRD_PARTY_PATH
    ),
    'gatk': THIRD_PARTY_PATH + '/GenomeAnalysisTK.jar',
    'vcf_annotator': THIRD_PARTY_PATH + '/vcf-annotator',

    # K-mer related
    'jellyfish': THIRD_PARTY_PATH + '/jellyfish',

    # Annotation related
    'prokka': THIRD_PARTY_PATH + '/prokka/prokka',

    # Pipelines
    'fastq_cleanup_pipeline': PIPELINE_PATH + '/fastq_cleanup',
    'illumina_assembly': PIPELINE_PATH + '/illumina_assembly',
    'predict_mlst': PIPELINE_PATH + '/predict_mlst',
    'predict_sccmec': PIPELINE_PATH + '/predict_sccmec',
    'call_variants': THIRD_PARTY_PATH + '/call_variants',
    'kmer_analysis': PIPELINE_PATH + '/kmer_analysis',
    'annotation': PIPELINE_PATH + '/annotation',

    # Staphopia related
    'download_ena': PATH + '/download_ena',
    'ascp': THIRD_PARTY_PATH + '/ascp',
    'aspera_key': THIRD_PARTY_PATH + '/asperaweb_id_dsa.openssh',
    'fastq_interleave': PATH + '/fastq_interleave',
    'manage': '/staphopia/ebs/staphopia.com/manage.py',

    # s3tools related
    'bucket-contents': THIRD_PARTY_PATH + '/s3tools/bucket-contents',
    'cleanup': THIRD_PARTY_PATH + '/s3tools/cleanup',
    'compare-directory': THIRD_PARTY_PATH + '/s3tools/compare-directory',
    'copy': THIRD_PARTY_PATH + '/s3tools/copy',
    'delete-contents': THIRD_PARTY_PATH + '/s3tools/delete-contents',
    'download': THIRD_PARTY_PATH + '/s3tools/download',
    'download-directory': THIRD_PARTY_PATH + '/s3tools/download-directory',
    'move': THIRD_PARTY_PATH + '/s3tools/move',
    'multipart-upload': THIRD_PARTY_PATH + '/s3tools/multipart-upload',
    'upload': THIRD_PARTY_PATH + '/s3tools/upload',
    'upload-directory': THIRD_PARTY_PATH + '/s3tools/upload-directory',
}

MLST = {
    'mlst_db': TOOL_DATA + '/mlst/Staphylococcus_aureus.fasta',
    'mlst_definitions': TOOL_DATA + '/mlst/saureus.txt',
    'mlst_blastdb': TOOL_DATA + '/mlst/blastdb',
}

SCCMEC = {
    'primers': TOOL_DATA + '/sccmec_primers.fasta',
    'proteins': TOOL_DATA + '/sccmec_proteins.fasta',
    'cassettes': TOOL_DATA + '/sccmec/sccmec_cassettes',
}

SNP = {
    'reference': TOOL_DATA + '/snp/n315.fasta',
    'ref_genbank': TOOL_DATA + '/snp/n315.gb',
}

ANNOTATION = {
    'genus': 'Staphylococcus-uniref90',
    'proteins': TOOL_DATA + '/annotation/sa-uniref90-reviewed.prokka'
}
