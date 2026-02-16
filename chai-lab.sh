#!/usr/bin/env bash

function set_config() {
    TIME="00:30:00"
    QUEUE="gpu_1"
    NODE=1
    GROUP=$(groups |awk '{print $NF}')
    FASTA="chai-lab_input/chai-lab.fasta"
    
}

function activate_environment() {
    # 1. Set Environment
    source ~/data/software/load_conda.sh
    conda activate chai_lab
    export PATH=~/bin:$PATH
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
    rm -rf ${outdir}
    mkdir -p ${outdir}
    script=sub_script/${jobname}.sh 
    cat >${script} <<EOF
#!/usr/bin/env bash
input="${FASTA}"
outdir=\$1
$(declare -f activate_environment)
$(declare -f submission_main)
submission_main
EOF
qsub -cwd -j y -l "h_rt=${TIME},${QUEUE}=${NODE}" -o "stdout/${jobname}.log" -g "${GROUP}" ${script} ${outdir}
}

function main() {
    set_config
    if [[ $# -gt 0 ]]; then
        outdir="$1"
        jobname=$(basename "$outdir")
    else
        echo "Usage: $0 <outdir>" >&2
        exit 1
    fi
    submit
}

main "$@"
