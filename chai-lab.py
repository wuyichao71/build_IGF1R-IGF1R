#!~/data/software/miniconda3/envs/chai_lab/bin/python

from pathlib import Path
from fastainfo import FastaInfo
import os
try:
    from chai_lab.chai1 import run_inference
except:
    pass
try:
    import torch
except:
    pass

config = {
    "human_IGF1R_fasta": os.path.join("input", "P08069_7S0Q_chainA.fasta"),
    "human_IGF1R_initial": 30,
    "human_IGF1R_length": 897,
    "human_IGF1_fasta": os.path.join("input", "P05019_6PYH_chainB.fasta"),
    "human_IGF1_initial": 50,
    "human_IGF1_length": 61,

    "fasta_template": """
>protein|name={IGF1R_name}-A
{IGF1R_seq}
>protein|name={IGF1R_name}-B
{IGF1R_seq}
>protein|name={IGF1_name}-C
{IGF1_seq}
"""
}

def set_config():
    config["fasta_name"]= os.path.join("chai-lab_input", Path(__file__).with_suffix('.fasta').name)
    config["outdir"] = os.path.join("chai-lab_output", Path(__file__).stem)


def main():
    human_IGF1R_fasta = FastaInfo(config['human_IGF1R_fasta'])
    human_IGF1_fasta = FastaInfo(config['human_IGF1_fasta'])
    IGF1R_ini = config['human_IGF1R_initial']
    IGF1R_lst = config['human_IGF1R_length'] + config['human_IGF1R_initial']
    IGF1_ini = config['human_IGF1_initial']
    IGF1_lst = config['human_IGF1_length'] + config['human_IGF1_initial']
    human_IGF1R_seq = human_IGF1R_fasta.seq[0][IGF1R_ini:IGF1R_lst]
    human_IGF1_seq = human_IGF1_fasta.seq[0][IGF1_ini:IGF1_lst]
    fasta_seq = config['fasta_template'].format(
        IGF1R_name='human_IGF1R',
        IGF1R_seq=human_IGF1R_seq,
        IGF1_name='human_IGF1',
        IGF1_seq=human_IGF1_seq
    ).strip()

    fasta_path = Path(config['fasta_name'])
    fasta_path.parent.mkdir(parents=True, exist_ok=True)
    fasta_path.write_text(fasta_seq)

    output_dir = Path(config['outdir'])
    output_dir.mkdir(parents=True, exist_ok=True)

    device = "cpu"
    if 'torch' in globals():
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    if 'run_inference' in globals():
        candidates = run_inference(
            fasta_file=fasta_path,
            output_dir=output_dir,
            # 'default' setup
            num_trunk_recycles=3,
            num_diffn_timesteps=200,
            seed=42,
            device=device,
            use_esm_embeddings=True,
        )



if __name__ == "__main__":
    set_config()
    main()