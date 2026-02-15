# PDB ID

6PYH

# records

in IGF1R/INSR
the IGF1R is from human
the relationship between chain ID and structure is:

- A: IGF1R
- B: changed INSR
- D: IGF1

in IGF1R/IGF1R
the IGF1R is from mouse
the relationship between chain ID and structure is:

- A: changed IGF1R
- B: IGF1
- D: IGF1R

If I want to mutant mouse IGF1R to human IGF1R, I need to mutant those residues.
The sequence index is for mouse IGF1R.

```text
28 F->Y
125 I->V
156 L->M
188 V->T
210 H->S
211 T->A
214 D->N
215 N->D
217 T->A
227 K->A
237 G->N
256 P->L
257 N->S
264 D->E
271 D->G
285 S->G
286 T->S
303 G->E
304 D d
327 L->F
406 N->D
412 V->I
413 R->K
414 S->A
465 R->H
472 W->S
532 E->D
533 G->V
606 T->S
651 V->I
666 D->E
709 R->K
730 V->A
742 F->L
896 P->Q
```

`input/6PYH.pse` show those mutant residues.

# compare

## `compare_sequence.py`

first, we compared the sequence with fasta information, for original structure (`input/6PYH.pdb`).

### Input

- `input/P08069_7S0Q_chainA.fasta`: P08069 is the full length sequence of human IGF1R
- `input/P05019_6PYH_chainB.fasta`: P05019 is the full length sequence of human IGF1
- `input/P08069_7S0Q_chainD.fasta`: P08069 is the full length sequence of human IGF1R
- `input/Q60751_6PYH_chainA.fasta`: Q60751 is the full length sequence of mouse IGF1R
- `input/P05019_6PYH_chainB.fasta`: P05019 is the full length sequence of human IGF1
- `input/Q60751_6PYH_chainD.fasta`: Q60751 is the full length sequence of mouse IGF1R
- `rcsb_pdb_6PYH.fasta`: sequence of 6PYH
- `input/initial.pdb`: soft link of `input/6PYH.pdb`, the structure of mouse IGF1R/IGF1R with IGF1

### Output

- `result/human_fasta_A.dat`: the sequence of human IGF1R
- `result/human_fasta_B.dat`: the sequence of human IGF1
- `result/human_fasta_D.dat`: the sequence of human IGF1R
- `result/mouse_fasta_A.dat`: the sequence of mouse IGF1R
- `result/mouse_fasta_B.dat`: the sequence of human IGF1
- `result/mouse_fasta_D.dat`: the sequence of mouse IGF1R
- `result/pdb_fasta_A.dat`: the sequence of 6PYH of mouse IGF1R
- `result/pdb_fasta_B.dat`: the sequence of 6PYH of human IGF1
- `result/pdb_fasta_D.dat`: the sequence of 6PYH of mouse IGF1R
- `result/pdb_A.dat`: the sequence of structure in 6PYH of mouse IGF1R
- `result/pdb_B.dat`: the sequence of structure in 6PYH of human IGF1
- `result/pdb_D.dat`: the sequence of structure in 6PYH of mouse IGF1R

# boltz2

script for run boltz2
boltz2 can not get right heterodimer of IGF1R/IGF1R

## `boltz2_input.py`

python language
generate input for boltz2, only input sequence.
output is `boltz2_input/boltz2_input.yaml`
structure is apo state

## `boltz2_input_template.py`

python language
generate input for boltz2, provide template, but without force.
output is `boltz2_input/boltz2_input_template.yaml`
structure is apo state

## `boltz2_input_template_force.py`

python language
generate input for boltz2, provide template, with force.
threshold for force is 4.3
output is `boltz2_input/boltz2_input_template_force.yaml`
structure is strange.

## `boltz2_input_template_force-1.0.py`

python language
generate input for boltz2, provide template, with force.
the threshold is from file name
output is `boltz2_input/boltz2_input_template_force-1.0.yaml`
structure is strange.

## `boltz2_input_template_force_potentials.py`

python language
generate input for boltz2, provide template, with force.
threshold for force is 12.0
add `--use_potentials` flag
output is `boltz2_input/boltz2_input_template_force.yaml`
structure is strange.

## `boltz2.sh`

bash language
submission script
submit boltz2 run in tsubame

# chai-lab

script for run chai-lab, chai-lab can not get right heterodimer of IGF1R/IGF1R

## `chai-lab.py`

python language
submission script

## `chai-lab_esm.py`

soft link of `chai-lab.py`
set `--use_esm_embeddings` to True

## `chai-lab_template.py`

soft link of `chai-lab.py`
set `--use_msa_server` to True
set `--use_templates_server` to True

## swiss-model

use website [swiss-model](https://swissmodel.expasy.org) to homology model the structure.
get right structure.
structure is `swiss-model/model_01.pdb`
use pymol to add terminal missing residue, structure is `swiss-model/model_01_add-terminal.pdb`

`swiss-model/model_01` is use 6PYH as the template, I think that the loop part is not right. It is used to save IGF1
