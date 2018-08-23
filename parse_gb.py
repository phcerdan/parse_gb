import re

'''
This script is for parsing a standard genbank file that contains multiple entries and returning a fasta file.
It extracts the organism name and specimen voucher, and concatenates them
into the first description field separated by a '_'. This is followed the associated
accession number separated by ' '. The specimen sequences is written on the following line, in a single line. e.g.


>Cortinarius_dulciolens_OTA60170 JX178605
AAGTCGTAACAAGGTTTCCGTAGGTGAACCTGCGGAAGGATCATTATTGAAATAAACCTGATGAGTTGCTGCTGGTTCTCTAGGGAGCATGTGCACGCTTGTCATCTTTATATCTCCACCTGTGCACTTTGTGTAGACCTGGATATCTTTCTGAATGCCCTGCATTCAGGTTTGAGGATTGACTTTGCCGTCTTTCCTTACAATTCCGGGCCTATGTTTTTCATATTCCCCATAACCCCTGTTTATAGAATGTAATGAATGGGCCTTTGTGCCTATAAATCTTTATACAACTTTCAGCAACGGATCTCTTGGCTCTCGCATCGATGAAGAACGCAGCGAAATGCGATAAGTAATGTGAATTGCAGAATTCAGTGAATCATCGAATCTTTGAACGCACCTTGCGCTCCTTGGTATTCCGAGGAGCATGCCTGTTTGAGTGTCATTAATATATCAACCTCTTCAGATTTTTGTTTGTCGAGTGTTGGATGTGGGGGTCTTCCTTTTGCTGGCCTTTATTACTGAGGTCAGCTCCCCTGAAATGCATTAGCAGAACATTTTGTTGACTCGTTCATTGGTGTGATAACTATCTACGCTATTGACGTGGAAGCAACCCAAGTTCAGCTTCTAACAGTCTATTGATTTGGACAAAATTCTTTATTAATGTGACCTCAAATCAGGTAGGACTACCCGCTGAACTTAA
>Cortinarius_dulciolens_PDD68471 NR_157914
AACAAGGTTTCCGTAGGTGAACCTGCGGAAGGATCATTATTGAAATAAACCTGATGAGTTGCTGCTGGTTCTCTAGGGAGCATGTGCACGCTTGTCATCTTTATATCTCCACCTGTGCACTTTTTGTAGTCCTGGATATCTCTCTGAATGCTACCTAGCATTCAGGTATGAGGATTGACTTTGTAGTCTCTCCTTGCATTTCCAGGCCTATGTTTTTTCATATACCCATCCCCTGTTTATAGAATGTAATAAAATGGGCCTTTGTGCCTATAAACCTTTATACAACTTTCAGCAACGGATCTCTTGGCTCTCGCATCGATGAAGAACGCAGCGAAATGCGATAAGTAATGTGAATTGCAGAATTCAGTGAATCATCGAATCTTTGAACGCACCTTGCGCTCCTTGGTATTCCGAGGAGCATGCCTGTTTGAGTGTCATTAATATATCAACCTCTTCAGATTTTTTGTTTGTCGAGTGTTGGACGTGGGGGTTCTTTTGCTGGCCTTGAGGTCAGCTCCCCTGAAATGCATTAGCAGAACATTTTGTTAACCTGTTCATTGGTGTGATAACTATCTACGCTATTGACATGGAGCAACCAAGTTCAGCTTCCAACAGTCCATTGATTTGGACAAATTTTTCATTAATGTGACCTCAAATCAGGTAGGACTACCCGCTGAACTTA


'''


SECTION_START_PATTERN = 'LOCUS'
SEQUENCE_START_PATTERN = 'ORIGIN'
END_PATTERN = '//'

input_file = open('sequence_single.gb','r')
sequnce_file = open('formatted_seq.fasta', 'w')


def formatted_seqence(input_file):
    match = False
    accession_number = ''
    organism = ''
    specimen_voucher = ''
    sequence = ''
    for line in input_file:
        if re.search('ACCESSION', line):
            accession_number = line.split()[1]
        elif re.search('ORGANISM', line):
            organism_line = line.split()
            organism = ' '.join(organism_line[1:3]).replace(' ','_')
        elif re.search('/specimen_voucher', line):
            specimen_voucher = line.split('"')[1].replace(':','').replace('.','').replace(' ','_')
        elif re.search(SEQUENCE_START_PATTERN, line):
            match == True
            continue
        elif re.search(END_PATTERN, line):
            match = False
            continue
        elif match == True:
            line = line.strip().split(" ")[1:]
            line = ''.join(line).upper()
            sequence += line

            sequnce_file.write('>' + organism + '_' + specimen_voucher + ' ' + accession_number + '\n' + sequence)


formatted_seqence(input_file)
