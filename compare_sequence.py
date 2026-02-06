#!/usr/bin/env python
import os
from pathlib import Path

config = {
    "initial_index": {"A": -29, "B": -47, "D": -29},
    "out_fasta_template": os.path.join("result", "fasta_{chain_id}.dat")
}
amino_code = {'CYS': 'C', 'ASP': 'D', 'SER': 'S', 'GLN': 'Q', 'LYS': 'K',
              'ILE': 'I', 'PRO': 'P', 'THR': 'T', 'PHE': 'F', 'ASN': 'N',
              'GLY': 'G', 'HIS': 'H', 'LEU': 'L', 'ARG': 'R', 'TRP': 'W',
              'ALA': 'A', 'VAL': 'V', 'GLU': 'E', 'TYR': 'Y', 'MET': 'M',}
amino_code_r = dict(zip(amino_code.values(), amino_code.keys()))


class FastaInfo():
    '''Get sequence infomation from fasta file.
    '''
    def __init__(self, fastaname):
        self._fastaname = fastaname
        self._rawinfo = open(self._fastaname, 'r').readlines()
        self.get_seq()

    def get_seq(self):
        self.seq = []
        seq = ''
        for rawline in self._rawinfo:
            line = rawline.strip()
            if len(line) == 0:
                continue
            if line.startswith('>'):
                if len(seq) != 0:
                    self.seq.append(seq)
                    seq = ''
            else:
                seq += line
        if len(seq) != 0:
            self.seq.append(seq)


def write_fasta_dat(outname: str, seq: str, length: int, initial_index: int=1, seq_from_index: int=1):
    '''
    output the sequence into a dat file
    
    :param length: Description
    :param initial_index: Description
    :param seq_from_index: Description
    
    :param outname: the name of output file
    :type outname: str
    :param seq: The sequence of amino acids
    :type seq: str
    :param length: the length of output sequence
    :type length: int
    :param initial_index: the initial index in output file
    :type initial_index: int
    :param seq_from_index: the initial index to output the sequence
    :type seq_from_index: int
    '''
    out_format = '{:4d} {} {}\n'
    Path(outname).parent.mkdir(parents=True, exist_ok=True)
    with open(outname, 'w') as out:
        for index in range(initial_index, initial_index+length):
            if index < seq_from_index:
                out.write(out_format.format(index, '-', '---'))
            elif index < seq_from_index + len(seq):
                out.write(out_format.format(index, seq[index-seq_from_index], amino_code_r[seq[index-seq_from_index]]))
            else:
                out.write(out_format.format(index, '-', '---'))


def main():
    fasta_dict = {
        'A': FastaInfo('input/P08069_6PYH_chainA.fasta'),
        'B': FastaInfo('input/P05019_6PYH_chainB.fasta'),
        'D': FastaInfo('input/P08069_6PYH_chainD.fasta')
        }
    
    len_dict = {key: len(value.seq[0]) for key, value in fasta_dict.items()}

    for key in fasta_dict:
        write_fasta_dat(config['out_fasta_template'].format(chain_id=key), fasta_dict[key].seq[0], len_dict[key], config['initial_index'][key], config['initial_index'][key])


if __name__ == '__main__':
    main()