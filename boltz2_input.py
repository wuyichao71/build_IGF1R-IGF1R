import yaml
from pathlib import Path
import os

config = {
    "human_IGF1R_fasta": os.path.join("input", "P08069_7S0Q_chainA.fasta"),
    "human_IGF1R_initial": 30,
    "human_IGF1R_length": 897,
    "human_IGF1_fasta": os.path.join("input", "P05019_6PYH_chainB.fasta"),
    "human_IGF1_initial": 50,
    "human_IGF1_length": 61,
    # "outname": os.path.join("boltz2_input", "boltz2_input.yaml"),
}


def set_config():
    name = Path(__file__).with_suffix('.yaml').name
    config["outname"] = os.path.join("boltz2_input", name)


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


def output_boltz2_yaml(outname: str, sequence_dict: list):
    out_dict = {"sequences": sequence_dict}
    Path(outname).parent.mkdir(parents=True, exist_ok=True)
    with open(outname, 'w') as f:
        yaml.dump(out_dict, f, sort_keys=False)


def main():
    human_IGF1R_fasta = FastaInfo(config['human_IGF1R_fasta'])
    human_IGF1_fasta = FastaInfo(config['human_IGF1_fasta'])
    IGF1R_ini = config['human_IGF1R_initial']
    IGF1R_lst = config['human_IGF1R_length'] + config['human_IGF1R_initial']
    IGF1_ini = config['human_IGF1_initial']
    IGF1_lst = config['human_IGF1_length'] + config['human_IGF1_initial']
    seqence_dict = [
        {"protein":"IGF1R", "chain": ['A', 'B'], "sequence": human_IGF1R_fasta.seq[0][IGF1R_ini:IGF1R_lst]},
        {"protein":"IGF1", "chain": 'D', "sequence": human_IGF1_fasta.seq[0][IGF1_ini:IGF1_lst]},
    ]
    output_boltz2_yaml(config['outname'], seqence_dict)


if __name__ == "__main__":
    set_config()
    main()