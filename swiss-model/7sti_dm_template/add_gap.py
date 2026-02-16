import os
from pathlib import Path

config = {
    "in_template": os.path.join("original.pdb"),
    "out_template": os.path.join("gap.pdb"),
    "start_resid": 681,
    "shift": 4,
}


def set_config():
    pass


def add_gap(inname: str, outname: str, start_resid: int, shift: int):
    '''
    add gap into the pdb file
    
    :param inname: the name of input file
    :type inname: str
    :param outname: the name of output file
    :type outname: str
    :param start_resid: the start residue index to add gap
    :type start_resid: int
    :param shift: the length of gap to add
    :type shift: int
    '''
    Path(outname).parent.mkdir(parents=True, exist_ok=True)
    with open(inname, 'r') as inp, open(outname, 'w') as out:
        for line in inp:
            if line.startswith("ATOM") or line.startswith("HETATM"):
                resid = int(line[22:26])
                if resid >= start_resid:
                    resid += shift
                    line = line[:22] + f"{resid:4d}" + line[26:]
            out.write(line)


def main():
    set_config()
    add_gap(config["in_template"], config["out_template"], config["start_resid"], config["shift"])

if __name__ == "__main__":
    main()