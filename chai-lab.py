#!/home/2/uj02562/data/software/miniconda3/envs/chai_lab/bin/python

from pathlib import Path
from fastainfo import FastaInfo
import os
import sys
import subprocess
import grp
import shutil

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
""",
    "esm": False,
    "use_msa_server": False,
    "use_templates_server": False,
}


def set_config():
    stem = Path(__file__).stem
    config["fasta_name"] = os.path.join("chai-lab_input", Path(__file__).with_suffix('.fasta').name)
    config["outdir"] = os.path.join("chai-lab_output", stem)
    if "esm" in stem:
        config["esm"] = True
    if "template" in stem:
        config["use_msa_server"] = True
        config["use_templates_server"] = True


def in_grid_engine_job() -> bool:
    """
    judge whether the job is on the compute node.
    """
    return ("JOB_ID" in os.environ) or ("SGE_TASK_ID" in os.environ) or ("PE_HOSTFILE" in os.environ)


def run():
    try:
        from chai_lab.chai1 import run_inference
        print("load run_inference")
    except Exception:
        pass
    try:
        import torch
        print("load torch")
    except Exception:
        pass
    set_config()
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
    shutil.rmtree(output_dir)

    device = "cpu"
    if 'torch' in locals():
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"device is {device}")
    print("Run run_inference")
    print(config["esm"])
    if 'run_inference' in locals():
        candidates = run_inference(
            fasta_file=fasta_path,
            output_dir=output_dir,
            num_trunk_recycles=3,
            device=device,
            use_esm_embeddings=config['esm'],
            use_msa_server=config["use_msa_server"],
            use_templates_server=config["use_templates_server"]
        )
    print("Job finished!")


def submit():
    TIME = "02:00:00"
    QUEUE = "gpu_h"
    NODE = 1
    GROUP = grp.getgrgid(os.getgroups()[-1]).gr_name
    JOB_NAME = Path(__file__).stem
    with open(__file__, 'r') as f:
        py = f.readline().split('!')[1].strip()
    print(py)
    script = Path(__file__).name
    qsub_cmd = [
            'qsub',
            '-cwd',
            '-g', GROUP,
            '-l', f'h_rt={TIME}',
            '-l', f'{QUEUE}={NODE}',
            '-o', f'stdout/{JOB_NAME}.log',
            '-j', 'y',
            '-b', 'y',
            py, str(script),
            ]
    print("Submitting:", " ".join(map(str, qsub_cmd)))
    subprocess.run(qsub_cmd, check=True)


def main():
    """
    main function
    """
    if ('--submit' in sys.argv) or not in_grid_engine_job():
        submit()
    else:
        run()


if __name__ == "__main__":
    main()
