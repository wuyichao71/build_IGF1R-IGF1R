# PDB ID

6PYH

# records

in IGF1R/INSR
the relationship between chain ID and structure is:

- A: IGF1R
- B: changed INSR
- D: IGF1

in IGF1R/IGF1R
the relationship between chain ID and structure is:

- A: changed IGF1R
- B: IGF1
- D: IGF1R

## `compare_sequence.py`

first, we compared the sequence with fasta information, for original structure (`input/6PYH.pdb`).

### Input

#### `input/6PYH.pdb`

`input/initial.pdb` is a soft link of `input/6PYH.pdb`.

#### `input/P08069_6PHY_chainA.pdb`

P08069 is the full length sequence of human IGF1R.

#### `input/P05019_6PHY_chainB.pdb`

P05019 is the full length sequence of human IGF1.

#### `input/P08069_6PHY_chainD.pdb`

soft link of `input/P05019_6PHY_chainA.pdb`
