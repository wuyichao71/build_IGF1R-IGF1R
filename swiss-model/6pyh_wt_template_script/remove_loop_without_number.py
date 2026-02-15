#!/usr/bin/env python
import os

config = {
    "in_template": os.path.join("swiss-model", "model_01_add-terminal_reorder.pdb"),
    "out_template": os.path.join("swiss-model", "model_01_add-terminal_reorder_rmv.pdb"),
    "remove_range": (706, 742),
}


def set_config():
    pass


def get_chain_start(lines):
    start = [0]
    old_res_seq = 0
    resid = 0
    for line in lines:
        if line.startswith("ATOM") or line.startswith("HETATM"):
            res_seq = int(line[22:26])
            if res_seq != old_res_seq:
                old_res_seq = res_seq
                resid += 1
        if line.startswith("TER"):
            start.append(resid)
    return start


def remove_loop(out_template, in_template):
    with open(in_template, "r") as f:
        lines = f.readlines()

    start = get_chain_start(lines)
    print(start)

    with open(out_template, "w") as f:
        old_skip = False
        for line in lines:
            if line.startswith("ATOM") or line.startswith("HETATM"):
                res_seq = int(line[22:26])
                for i in range(len(start)-1):
                    if start[i] + config["remove_range"][0] <= res_seq < start[i] + config["remove_range"][1]:
                        skip = True
                        break
                else:
                    skip = False
                if skip and not old_skip:
                    f.write("TER\n")
                old_skip = skip
                if skip:
                    continue
            f.write(line)


def main():
    set_config()
    remove_loop(config["out_template"], config["in_template"])


if __name__ == '__main__':
    main()