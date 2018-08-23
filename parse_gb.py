import re

# TODO(PHC): DELETEME Nice documentation, should this be here, or inside the function?
'''
This script is for parsing a standard genbank file that contains multiple entries and returning a fasta file.
It extracts the organism name and specimen voucher, and concatenates them
into the first description field separated by a '_'. This is followed the associated
accession number separated by ' '. The specimen sequences is written on the following line, in a single line. e.g.
>Cortinarius_dulciolens_OTA60170 JX178605
AAGTCGTAACAAGGTTTC...
>Cortinarius_dulciolens_PDD68471 NR_157914
AACAAGGTTTCCGTAGGT...
'''

def formatted_sequence(input_filename, sequence_filename):
    input_file = open(input_filename, 'r')
    sequence_file = open(sequence_filename, 'w')
    # TODO(PHC): DELETEME Are these PATTERNS something fixed, or change depending on the input?
    # if the second, these should be arguments for the function.
    # if the first, this is neat, please delete this comment
    # also I like the CAPS for denoting CONSTANTS
    SECTION_START_PATTERN = 'LOCUS'  # TODO: PHC: UNUSED, why?
    SEQUENCE_START_PATTERN = 'ORIGIN'
    END_PATTERN = '//'

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

    sequence_file.write('>' + organism + '_' + specimen_voucher + ' ' + accession_number + '\n' + sequence)


# TODO(PHC) DELETEME
# we use this to allow execute this file as a script,
# but also to be able to import it for other things with:
# from parse_gb import (foo, bar)
# see: https://stackoverflow.com/questions/419163/what-does-if-name-main-do
if __name__ == "__main__":
    """
    Suggestion as future exercises:
    1) IMPORTANT: create a test with the fixture data you have
     this is super important and will allow you to be sure that any future change works, ease your mind when you change stuff (tests are passing)
    see https://docs.python.org/3/library/unittest.html
    2) parse arguments when you are not using test data anymore
    see argparse https://docs.python.org/3/howto/argparse.html
    """
    inputFilename = 'sequence_multi.gb'
    outputFilename = 'formatted_seq.fasta'
    formatted_sequence(inputFilename, outputFilename)
