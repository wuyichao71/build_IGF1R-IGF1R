import yaml
from pathlib import Path
import os
import re

config = {
    "human_IGF1R_fasta": os.path.join("input", "P08069_7S0Q_chainA.fasta"),
    "human_IGF1R_initial": 30,
    "human_IGF1R_length": 897,
    "human_IGF1_fasta": os.path.join("input", "P05019_6PYH_chainB.fasta"),
    "human_IGF1_initial": 50,
    "human_IGF1_length": 61,
    "cif_path": os.path.join("input", "6PYH.cif"),
    # "outname": os.path.join("boltz2_input", "boltz2_input.yaml"),
}


def set_config():
    name = Path(__file__).with_suffix('.yaml').name
    config["outname"] = os.path.join("boltz2_input", name)
    # tokens = Path(__file__).stem.split('_')


class FastaInfo():
    '''
    Get sequence infomation from fasta file.
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


def output_boltz2_yaml(outname: str, yaml_dict: dict):
    out_dict = yaml_dict
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
    yaml_dict = {
        "sequences": 
        [
            {"protein": {"id": ['A', 'B'], "sequence": human_IGF1R_fasta.seq[0][IGF1R_ini:IGF1R_lst]}},
            {"protein": {"id": 'C', "sequence": human_IGF1_fasta.seq[0][IGF1_ini:IGF1_lst]}},
        ],
    }
    if 'template' in __file__:
        yaml_dict["templates"] = [
            {"cif": config['cif_path'], "chain_id": ['A', 'B', 'C'], "template_id": ['C', 'A', 'B']},
        ]
    if 'force' in __file__:
        yaml_dict["templates"][0]["force"] = True
        threshold = 4.3
        match = re.search(r'force-([0-9.]+)', Path(__file__).stem)
        if match:
            threshold = float(match.group(1))
        yaml_dict["templates"][0]["threshold"] = threshold
    output_boltz2_yaml(config['outname'], yaml_dict)


if __name__ == "__main__":
    set_config()
    main()