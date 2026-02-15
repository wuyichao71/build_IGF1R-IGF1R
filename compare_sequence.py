#!/usr/bin/env python
import os
from pathlib import Path
from fastainfo import FastaInfo
from pdbinfo import PdbInfo
from amino_acid import amino_code, amino_code_r

config = {
    "initial_index": {"A": -29, "B": -47, "D": -29},
    "wt_initial_index": {"A": -29, "B": -29, "C": -47},
    "out_human_fasta_template": os.path.join("result", "human_fasta_{chain_id}.dat"),
    "out_mouse_fasta_template": os.path.join("result", "mouse_fasta_{chain_id}.dat"),
    "out_pdb_fasta_template": os.path.join("result", "pdb_fasta_{chain_id}.dat"),
    "out_pdb_template": os.path.join("result", "pdb_{chain_id}.dat"),
    "out_wt_template": os.path.join("result", "wt_{chain_id}.dat"),
    "out_format": '{:4d} {} {}\n'
}
# amino_code = {'CYS': 'C', 'ASP': 'D', 'SER': 'S', 'GLN': 'Q', 'LYS': 'K',
#               'ILE': 'I', 'PRO': 'P', 'THR': 'T', 'PHE': 'F', 'ASN': 'N',
#               'GLY': 'G', 'HIS': 'H', 'LEU': 'L', 'ARG': 'R', 'TRP': 'W',
#               'ALA': 'A', 'VAL': 'V', 'GLU': 'E', 'TYR': 'Y', 'MET': 'M',}
# amino_code_r = dict(zip(amino_code.values(), amino_code.keys()))


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
    for key in pdb.residue:
        write_residue_dat(config['out_pdb_template'].format(chain_id=key), pdb.residue[key], len_dict[key], config['initial_index'][key])

    wt_len_dict = {'A': len(human_fasta_dict['D']), 'B': len(human_fasta_dict['A']), 'C': len(human_fasta_dict['B'])}
    wt = PdbInfo("swiss-model/model_01/model_01_add-terminal_reorder_rmv.pdb")
    for key in wt.residue:
        write_residue_dat(config['out_wt_template'].format(chain_id=key), wt.residue[key], wt_len_dict[key], config['wt_initial_index'][key])

if __name__ == '__main__':
    main()