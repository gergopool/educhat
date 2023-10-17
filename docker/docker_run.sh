#!/bin/bash

# Variable initialization
source .dockerenv

it=""
p=""
gpu_params=""
os_type=$(uname)
command=""
image_name=${IMAGE_NAME}
cache_folder="/home/${USER}/.cache/huggingface"

# Check if GPUs are available (Linux only)
if [[ "$os_type" == "Linux" ]]; then
    if command -v nvidia-smi &> /dev/null; then
        gpu_params="--gpus all"
    fi
fi

# Usage instruction
print_usage() {
    echo "Usage: ./docker_run.sh [options] [command]"
    echo "Options:"
    echo "  -g  Which GPU(s) to use (sets CUDA_VISIBLE_DEVICES) (Linux only)"
    echo "  -i  Run Docker interactively"
    echo "  -p  Which port to use for the server"
    echo "  -h  Show this help message"
}

# Parse command-line arguments
while getopts "gp:ih:c" flag; do
    case "${flag}" in
        g) [ "$os_type" == "Linux" ] && gpu_params="-e CUDA_VISIBLE_DEVICES=${OPTARG}";;
        i) it="-it";;
        p) port_params="-p ${OPTARG}";;
        h) print_usage
           exit 0 ;;
        *) print_usage
           exit 1 ;;
    esac
done

# Get the remaining arguments as the command to run inside the container
shift $((OPTIND-1))
command="$@"

# Run Docker container
docker run --shm-size=50g --rm \
    $it $gpu_params $port_params \
    --user $(id -u):$(id -g) $(id -G | sed -e 's/\</--group-add /g')  \
    -e CUDA_DEVICE_ORDER=PCI_BUS_ID \
    -v `pwd`/../:/workspace \
    -v $cache_folder:$cache_folder \
    -v /etc/passwd:/etc/passwd:ro \
    -v /etc/group:/etc/group:ro \
    -v /etc/shadow:/etc/shadow:ro \
    --workdir=/workspace \
    $image_name $command
