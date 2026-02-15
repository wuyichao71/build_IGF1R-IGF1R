#!/usr/bin/env python
import os

config = {
    "in_template": os.path.join("swiss-model", "model_01_add-terminal_reorder.pdb"),
    "out_template": os.path.join("swiss-model", "model_01_add-terminal_reorder_numbered.pdb"),
}


def set_config():
    pass


def get_chain_length(lines):
    length = []
    length_t = 0
    old_res_seq = 0
    for line in lines:
        if line.startswith("ATOM") or line.startswith("HETATM"):
            res_seq = int(line[22:26])
            if res_seq != old_res_seq:
                old_res_seq = res_seq
                length_t += 1
        if line.startswith("TER"):
            length.append(length_t)
            length_t = 0
    return length


def number_residue(out_template, in_template):
    with open(in_template, "r") as f:
        lines = f.readlines()

    with open(out_template, "w") as f:
        old_res_seq = 0
        new_res_seq = 0
        for line in lines:
            if line.startswith("ATOM") or line.startswith("HETATM"):
                res_seq = int(line[22:26])
                if res_seq != old_res_seq:
                    old_res_seq = res_seq
                    new_res_seq += 1
                line = line[:22] + f"{new_res_seq:4d}" + line[26:]
            f.write(line)


def main():
    set_config()
    number_residue(config["out_template"], config["in_template"])


if __name__ == '__main__':
    main()