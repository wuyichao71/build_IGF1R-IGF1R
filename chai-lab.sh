#!/usr/bin/env bash

function set_config() {
    TIME="00:30:00"
    QUEUE="gpu_1"
    NODE=1
    STDOUT='stdout/$JOB_NAME.log'
    FASTA="chai-lab_input/chai-lab.fasta"
    
}

function activate_environment() {
    # 1. Set Environment
    source ~/data/software/load_conda.sh
    conda activate chai_lab
}

function submission_main() {
    activate_environment
    # 2. Run chai-lab
    echo "Starting chai-lab for ${jobname}..."
    date
    time chai-lab fold --use-msa-server --use-templates-server "$input" "$outdir"
    date
    echo "Job finished."
}

function submit() {
cat >sub_script/${jobname}.sh <<EOF
#!/usr/bin/env bash
outdir="chai-lab_output/${jobname}"
input="${FASTA}"
$(declare -f activate_environment)
$(declare -f submission_main)
submission_main
EOF
qsub -cwd -j y -l "h_rt=${TIME},${QUEUE}=${NODE}" -o "${STDOUT}" -g "${GROUP}" -N "${jobname}"
}

function main() {
    set_config
    if [[ $# -gt 0 ]]; then
        outdir="$1"
        jobname=$(basename "$outdir")
    else
        echo "Usage: $0 <job_name>" >&2
        exit 1
    fi
    submit
}

main "$@"
