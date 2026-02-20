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

### `download_pdb.sh`

bash language
download pdb of P08069.

## bad result

`swiss-model/6pyh_wt_template/` is use 6PYH as the template, I think that the loop part is not right.  
`swiss-model/6pyh_wt_template/model_01.pdb` is predicted by swiss-model.  
`swiss-model/6pyh_wt_template/model_01_add-terminal.pdb` use pymol to add terminal missing residue.  
`swiss-model/6pyh_wt_template/model_01_add-terminal_reorder.pdb` change the chain order(A->B, B->C, D->A) (`order_chain.py`).  
`swiss-model/6pyh_wt_template/model_01_add-terminal_reorder_numbered.pdb` numbered the residue one by one (`number_residue.py`).  
`swiss-model/6pyh_wt_template/model_01_add-terminal_reorder_numbered_rmv.pdb` removed the useless loop (`remove_loop.py`).  
`swiss-model/6pyh_wt_template/model_01_add-terminal_reorder_rmv.pdb` removed the useless loop before numbering, it is used for `compare_sequence.py` (`remove_loop_without_number.py`).

handle python script is put to `swiss-model/6pyh_wt_template_script`.

### wt IGF1R/IGF1R w/ IGF1

`swiss-model/7sti_wt_template/` is the directory for wild type of IGF1R/IGF1R w/ IGF1.  
`swiss-model/wt` is soft link of it, this is as the wild type IGF1R/IGF1R w/ IGF1.

`swiss-model/7sti_wt_template/model_02.pdb` is predicted by swiss-model, template is 7STI.  
`swiss-model/7sti_wt_template/model_02_rloop.pdb` replace the bad loop by loop from `swiss-model/7sti_dm_template/model_01.pdb`.
`swiss-model/7sti_wt_template/model_02_rloop_at.pdb` add terminal missing residues by pymol.
`swiss-model/7sti_wt_template/original.pdb` is a soft link of `swiss-model/7sti_wt_template/model_02_rloop_at.pdb`.
`swiss-model/7sti_wt_template/gap.pdb` adds the residue index of mutant part and chain C (IGF1). script is `swiss-model/7sti_wt_template/add_gap.py`.
`swiss-model/7sti_wt_template/order.pdb` is reorder the chain id. script is `swiss-model/7sti_wt_template/order.py`.
`swiss-model/7sti_wt_template/remove_loop.pdb` is remove the useless loop. script is `swiss-model/7sti_wt_template/remove_loop.py`.

`swiss-model/7sti_wt_template/wt.pdb` is a soft link of `swiss-model/7sti_wt_template/remove_loop.pdb`.
**`swiss-model/wt/wt.pdb` is final wild type IGF1R/IGF1R w/ IGF1**

### dm IGF1R/IGF1R w/ IGF1

`swiss-model/7sti_dm_template/` is the directory for deletion mutant IGF1R/IGF1R w/ IGF1.  
`swiss-model/dm` is soft link of it, this is as the deletion mutant IGF1R/IGF1R w/ IGF1.

`swiss-model/7sti_dm_template/model_01.pdb` is predicted by swiss-model, template is 7STI.  
`swiss-model/7sti_dm_template/model_01_at.pdb` add terminal missing residues by pymol.
`swiss-model/7sti_dm_template/model_01_at_repigf1.pdb` replaces the IGF1 from `swiss-model/7sti_wt_template/model_02_rloop_at.pdb`.
`swiss-model/7sti_dm_template/original.pdb` is a soft link of `swiss-model/7sti_dm_template/model_01_at_repigf1.pdb`.
`swiss-model/7sti_dm_template/gap.pdb` adds the residue index of mutant part and chain C (IGF1). script is `swiss-model/7sti_dm_template/add_gap.py`.
`swiss-model/7sti_dm_template/order.pdb` is reorder the chain id. script is `swiss-model/7sti_dm_template/order.py`.
`swiss-model/7sti_dm_template/remove_loop.pdb` is remove the useless loop. script is `swiss-model/7sti_dm_template/remove_loop.py`.

`swiss-model/7sti_dm_template/dm.pdb` is a soft link of `swiss-model/7sti_dm_template/remove_loop.pdb`.
**`swiss-model/dm/dm.pdb` is final deletion mutant IGF1R/IGF1R w/ IGF1**

## disulfide bonds

| sequence id | pdb id            | charmm id       |
| ----------- | ----------------- | --------------- |
|             | intra-IGF1R(A)    |                 |
| 3-22        | A3-A22            | PROA3-PROA22    |
| 120-148     | A120-A148         | PROA120-PROA148 |
| 152-175     | A152-A175         | PROA152-PROA175 |
| 162-181     | A162-A181         | PROA162-PROA181 |
| 185-194     | A185-A194         | PROA185-PROA194 |
| 189-200     | A189-A200         | PROA189-PROA200 |
| 201-209     | A201-A209         | PROA201-PROA209 |
| 205-218     | A205-A218         | PROA205-PROA218 |
| 221-230     | A221-A230         | PROA221-PROA230 |
| 234-246     | A234-A246         | PROA234-PROA246 |
| 252-273     | A252-A273         | PROA252-PROA273 |
| 277-291     | A277-A291         | PROA277-PROA291 |
| 294-298     | A294-A298         | PROA294-PROA298 |
| 302-323     | A302-A323         | PROA302-PROA323 |
| 425-458     | A425-A458         | PROA425-PROA458 |
| 633-849     | A633-A849         | PROA633-PROB849 |
| 669-672     | A669-A672         | PROA669-PROA672 |
| 776-785     | A776-A785         | PROA776-PROB785 |
|             | intra-IGF1R(B)    |                 |
| 3-22        | B3-B22            | PROC3-PROC22    |
| 120-148     | B120-B148         | PROC120-PROC148 |
| 152-175     | B152-B175         | PROC152-PROC175 |
| 162-181     | B162-B181         | PROC162-PROC181 |
| 185-194     | B185-B194         | PROC185-PROC194 |
| 189-200     | B189-B200         | PROC189-PROC200 |
| 201-209     | B201-B209         | PROC201-PROC209 |
| 205-218     | B205-B218         | PROC205-PROC218 |
| 221-230     | B221-B230         | PROC221-PROC230 |
| 234-246     | B234-B246         | PROC234-PROC246 |
| 252-273     | B252-B273         | PROC252-PROC273 |
| 277-291     | B277-B291         | PROC277-PROC291 |
| 294-298     | B294-B298         | PROC294-PROC298 |
| 302-323     | B302-B323         | PROC302-PROC323 |
| 425-458     | B425-B458         | PROC425-PROC458 |
| 633-849     | B633-B849         | PROC633-PROD849 |
| 669-672     | B669-B672         | PROC669-PROC672 |
| 776-785     | B776-B785         | PROC776-PROD785 |
|             | intra-IGF1(C)     |                 |
| 6-48        | C6-C48            | PROE6-PROE48    |
| 18-61       | C18-C61           | PROE18-PROE61   |
| 47-52       | C47-C52           | PROE47-PROE52   |
|             | inter-IGF1R-IGF1R |                 |
| 514-514     | A514-B514         | PROA514-PROC514 |
| 670-670     | A670-B670         | PROA670-PROC670 |

check:  
A514-B514:  
1IGF do not have  
5U8Q exist  
5U8R do not have  
6JK8 do not have  
6VWG+6VWH do not have  
6VWI+6VWJ do not have  
7S0Q+7S8V exist  
7U23 do not have  
7V3P do not have  
7XGD not exist  
7XLC not exist  
7YRR not exist  
8TAN not exist but close

## protonation state

| sequence id  | pdb id         | charmm id        |
| ------------ | -------------- | ---------------- |
|              | intra-IGF1R(A) |                  |
| 30 HIS->HSE  | A30 HIS->HSE   | PROA30 HIS->HSE  |
| 202 HIS->HSD | A202 HIS->HSD  | PROA202 HIS->HSD |
| 223 HIS->HSE | A223 HIS->HSE  | PROA223 HIS->HSE |
| 269 HIS->HSE | A269 HIS->HSE  | PROA269 HIS->HSE |
| 362 HIS->HSE | A362 HIS->HSE  | PROA362 HIS->HSE |
| 364 HIS->HSE | A364 HIS->HSE  | PROA364 HIS->HSE |
| 406 HIS->HSE | A406 HIS->HSE  | PROA406 HIS->HSE |
| 464 HIS->HSE | A464 HIS->HSE  | PROA464 HIS->HSE |
| 480 HIS->HSD | A480 HIS->HSD  | PROA480 HIS->HSD |
| 539 HIS->HSE | A539 HIS->HSE  | PROA539 HIS->HSE |
| 563 HIS->HSE | A563 HIS->HSE  | PROA563 HIS->HSE |
| 630 HIS->HSD | A630 HIS->HSD  | PROA630 HIS->HSD |
| 697 HIS->HSE | A697 HIS->HSE  | PROA697 HIS->HSE |
| 774 HIS->HSD | A774 HIS->HSD  | PROB774 HIS->HSD |
| 778 HIS->HSD | A778 HIS->HSD  | PROB778 HIS->HSD |
|              | intra-IGF1R(B) |                  |
| 30 HIS->HSE  | B30 HIS->HSE   | PROC30 HIS->HSE  |
| 202 HIS->HSD | B202 HIS->HSD  | PROC202 HIS->HSD |
| 223 HIS->HSE | B223 HIS->HSE  | PROC223 HIS->HSE |
| 269 HIS->HSE | B269 HIS->HSE  | PROC269 HIS->HSE |
| 362 HIS->HSE | B362 HIS->HSE  | PROC362 HIS->HSE |
| 364 HIS->HSE | B364 HIS->HSE  | PROC364 HIS->HSE |
| 406 HIS->HSE | B406 HIS->HSE  | PROC406 HIS->HSE |
| 464 HIS->HSE | B464 HIS->HSE  | PROC464 HIS->HSE |
| 480 HIS->HSD | B480 HIS->HSD  | PROC480 HIS->HSD |
| 539 HIS->HSE | B539 HIS->HSE  | PROC539 HIS->HSE |
| 563 HIS->HSE | B563 HIS->HSE  | PROC563 HIS->HSE |
| 630 HIS->HSD | B630 HIS->HSD  | PROC630 HIS->HSD |
| 697 HIS->HSE | B697 HIS->HSE  | PROC697 HIS->HSE |
| 774 HIS->HSD | B774 HIS->HSD  | PROD774 HIS->HSD |
| 778 HIS->HSD | B778 HIS->HSD  | PROD778 HIS->HSD |
|              | intra-IGF1(C)  |                  |
|              |                |                  |

## `charmm-gui`

the force field of wild type IGF1R/IGF1R w/ IGF1 is `swiss-model/wt/charmm-gui/charmm-gui-7122467825/`  
the force field of deletion mutant IGF1R/IGF1R w/ IGF1 is `swiss-model/dm/charmm-gui/charmm-gui-7122866311/`  
here set `{wt} = swiss-model/wt/charmm-gui/charmm-gui-7122467825/` and `{dm} = swiss-model/dm/charmm-gui/charmm-gui-7122866311/`

### `{wt}/gromacs_run`

### `{wt}genesis_run_gmx_convert`

### `{dm}/gromacs_run`

### `{dm}genesis_run_gmx_convert`
