#!/usr/bin/env bash

seq=(6JK8 7V3P 6VWG 6VWH 6VWI 6VWJ 7S0Q 7S8V 7U23 8TAN 7XGD 7XLC 7YRR 5U8Q 5U8R 1IGR)

mkdir -p IGF1R_pdb
for i in "${seq[@]}"
do
    wget -P IGF1R_pdb "https://files.rcsb.org/download/${i}.pdb"
done