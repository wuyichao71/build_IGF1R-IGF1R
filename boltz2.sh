#!/usr/bin/env bash

function set_config() {
    TIME="00:30:00"
    QUEUE="gpu_h"
    STDOUT='stdout/$JOB_NAME.log'
    NUM_NODE=1
    GROUP=$(groups |awk '{print $NF}')
}

function get_jobname() {
    if [[ -n $JOB_NAME ]]; then
        jobname=${JOB_NAME%.sh}
    else
        jobname=${0%.sh}
    fi
}

function activate_environment() {
    # 1. Set Environment
    source ~/data/software/load_conda.sh
    conda activate boltz
    get_jobname
    use_potentials=""
    if [[ $input =~ .*potentials.* ]]; then
        use_potentials="--use_potentials"
    fi
    if [[ $input =~ .*reducemsa.* ]]; then
        n=32
        num=${input#*reducemsa-}
        num=${num%%[^0-9]*}
        [[ -n $num ]] && ((n = num))
        echo $n
        max_msa_seqs="--max_msa_seqs $n"
    fi
}

function submission_main() {
    activate_environment
    # 2. Run Boltz
    echo "Starting Boltz-2 for ${jobname}..."
    date
    time boltz predict "$input" --use_msa_server --out_dir "boltz2_output" --override $use_potentials $max_msa_seqs
    date
    echo "Job finished."
}

function submit() {
    cat >${script} <<EOF
#!/usr/bin/env bash
#$ -cwd
#$ -j y
input=${input}
$(declare -f get_jobname)
$(declare -f activate_environment)
$(declare -f submission_main)

submission_main

EOF
qsub -l "h_rt=$TIME" -o "$STDOUT" -l "$QUEUE=${NUM_NODE}" -g "${GROUP}" $script
}

function main() {
    set_config
    mkdir -p sub_script
    if [[ $# -lt 1 ]]; then
        echo "bash boltz2.sh INPUT" >&2 && exit 1
    fi
    input=$1
    base="${input##*/}"
    base="${base%.*}"
    script=sub_script/${base}.sh
    echo $script
    # activate_environment
    submit
}

main "$@"

# boltz predict "/home/2/uj02562/data/study/bz_run/bz_input/Experiment_A_noPhos_Truncated_xray.yaml" \
#     --out_dir "../bz_output" \
#     --use_msa_server \
#     --method "x-ray diffraction" \
#     --use_potentials \
#     --recycling_steps 3 \
#     --override
