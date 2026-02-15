#!/usr/bin/env python
import os

config = {
    "order": {'A': "B", "B": "C", "C": "A"},
    "in_template": os.path.join("swiss-model", "model_01_add-terminal.pdb"),
    "out_template": os.path.join("swiss-model", "model_01_add-terminal_reorder.pdb"),
}


def set_config():
    pass


def order_chain(out_template, in_template, order):
    with open(in_template, "r") as f:
        lines = f.readlines()

    header = []
    content = {key:[] for key in order.values()}
    read_content = False
    with open(out_template, "w") as f:
        for line in lines:
            if not read_content:
                if line.startswith("ATOM") or line.startswith("HETATM"):
                    read_content = True
                else:
                    header.append(line)

            if line.startswith("ATOM") or line.startswith("HETATM"):
                chain_id = line[21]
                new_chain_id = order[chain_id]
                line = line[:21] + new_chain_id + line[22:]
                content[new_chain_id].append(line)
        for line in header:
            f.write(line)
        for key in sorted(content.keys()):
            for line in content[key]:
                f.write(line)
            f.write("TER\n")
        f.write("END\n")


def main():
    set_config()
    order_chain(config["out_template"], config["in_template"], config["order"])


if __name__ == '__main__':
    main()