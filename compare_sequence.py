#!/usr/bin/env python
import os
from pathlib import Path

config = {
    "initial_index": {"A": -29, "B": -47, "D": -29},
    "out_human_fasta_template": os.path.join("result", "human_fasta_{chain_id}.dat"),
    "out_mouse_fasta_template": os.path.join("result", "mouse_fasta_{chain_id}.dat"),
    "out_pdb_fasta_template": os.path.join("result", "pdb_fasta_{chain_id}.dat"),
    "out_pdb_template": os.path.join("result", "pdb_{chain_id}.dat"),
    "out_format": '{:4d} {} {}\n'
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


class PdbInfo():
    '''Get residue infomation from pdb file. 
    '''

    def __init__(self, pdbname):
        self._pdbname = pdbname
        self._rawinfo = open(self._pdbname, 'r').readlines()
        self.get_seq()
        self.get_residue()
        self.get_missing_residue()

    def get_seq(self):
        self._seq = {}
        for rawline in self._rawinfo:
            if rawline.startswith('SEQRES'):
                tokens = rawline.strip().split()
                chain_id = tokens[2]
                res_3l = tuple(tokens[4:])
                res_1l = [amino_code[i] for i in res_3l]
                self.add_dict_data(self._seq, 'extend', chain_id, res_3l)

        # for i in self._seq.values():
        #     print(len(i))

    def get_missing_residue(self):
        self.missing_residue = {}
        record = False
        for rawline in self._rawinfo:
            if rawline.startswith('REMARK 465'):
                line = rawline.strip()
                if line.endswith('SSSEQI'):
                    record = True
                elif record:
                    res_name = line[15:18]
                    # res_name = tokens[2]
                    # chain_id = tokens[3]
                    chain_id = line[19]
                    res_seq = int(line[21:26])
                    self.add_dict_data(self.missing_residue, 'append', chain_id, (res_seq, res_name))

    def add_dict_data(self, d, func_type, chain_id, data):
        if chain_id not in d.keys():
            d[chain_id] = []
        getattr(d[chain_id], func_type)(data)

    def get_residue(self):
        self.residue = {}
        for rawline in self._rawinfo:
            if rawline.startswith('ATOM'):
                line = rawline.strip()
                atom_name = line[12:16].strip()
                if atom_name == 'CA':
                    res_name = line[17:21].strip()
                    res_seq = int(line[22:26])
                    chain_id = line[21]
                    self.add_dict_data(self.residue, 'append', chain_id, (res_seq, res_name))
                    # if chain_id not in self.residue.keys():
                    #     self.residue[chain_id] = []
                    # self.residue[chain_id].append([res_seq, res_name])


def write_fasta_dat(outname: str, seq: str, length: int, initial_index: int=1, seq_from_index: int=1):
    '''
    output the fasta sequence into a dat file
    
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
    out_format = config["out_format"]
    Path(outname).parent.mkdir(parents=True, exist_ok=True)
    with open(outname, 'w') as out:
        for index in range(initial_index, initial_index+length):
            if index < seq_from_index:
                out.write(out_format.format(index, '-', '---'))
            elif index < seq_from_index + len(seq):
                out.write(out_format.format(index, seq[index-seq_from_index], amino_code_r[seq[index-seq_from_index]]))
            else:
                out.write(out_format.format(index, '-', '---'))


def write_residue_dat(outname:str, data: tuple, length: int, initial_index: int=1):
    '''
    output the sequence of pdb existed residue into a dat file
    
    :param outname: the name of output file
    :type outname: str
    :param data: The sequence of amino acids, it contains (residue_index, residue_name)
    :type data: tuple
    :param length: the length of output sequence
    :type length: int
    :param initial_index: the initial index in output file
    :type initial_index: int
    '''
    out_format = config["out_format"]
    data_index = 0
    with open(outname, 'w') as out:
        i = 0
        while i < length:
            index = i + initial_index
            if data_index == len(data) or index < data[data_index][0]:
                out.write(out_format.format(index, '-', '---'))
                i += 1
            elif index == data[data_index][0]:
                out.write(out_format.format(index, amino_code[data[data_index][1]], data[data_index][1]))
                data_index += 1
                i += 1
            else:
                data_index += 1


def main():
    human_fasta_dict = {
        'A': FastaInfo('input/P08069_7S0Q_chainA.fasta').seq[0],
        'B': FastaInfo('input/P05019_6PYH_chainB.fasta').seq[0],
        'D': FastaInfo('input/P08069_7S0Q_chainD.fasta').seq[0],
        }
    
    len_dict = {key: len(value) for key, value in human_fasta_dict.items()}

    for key in human_fasta_dict:
        write_fasta_dat(config['out_human_fasta_template'].format(chain_id=key), human_fasta_dict[key], len_dict[key], config['initial_index'][key], config['initial_index'][key])

    mouse_fasta_dict = {
        'A': FastaInfo('input/Q60751_6PYH_chainA.fasta').seq[0],
        'B': FastaInfo('input/P05019_6PYH_chainB.fasta').seq[0],
        'D': FastaInfo('input/Q60751_6PYH_chainD.fasta').seq[0],
        }
    
    len_dict = {key: len(value) for key, value in mouse_fasta_dict.items()}

    for key in mouse_fasta_dict:
        write_fasta_dat(config['out_mouse_fasta_template'].format(chain_id=key), mouse_fasta_dict[key], len_dict[key], config['initial_index'][key], config['initial_index'][key])

    pdb_fasta = FastaInfo("input/rcsb_pdb_6PYH.fasta")

    pdb_fasta_dict = {
        'A': pdb_fasta.seq[0],
        'B': pdb_fasta.seq[1],
        'D': pdb_fasta.seq[0],
    }

    for key in pdb_fasta_dict:
        write_fasta_dat(config['out_pdb_fasta_template'].format(chain_id=key), pdb_fasta_dict[key], len_dict[key], config['initial_index'][key], 1)

    pdb = PdbInfo("input/initial.pdb")
    # for key in pdb._seq:
    #     print(key, pdb._seq[key])
    # for key in pdb.missing_residue:
    #     print(key, pdb.missing_residue[key])
    # for key in pdb.residue:
    #     print(key, pdb.residue[key])
    for key in pdb.residue:
        write_residue_dat(config['out_pdb_template'].format(chain_id=key), pdb.residue[key], len_dict[key], config['initial_index'][key])


if __name__ == '__main__':
    main()