create_conda_env_dir=$(cd "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)
source ${create_conda_env_dir}/../defaults

create_env () {
    local env=${1:-$environment}
    local my_conda_base=$(cd "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)

    echo "Conda Python version $(conda run python --version)" >&2
    conda update -y -n base conda  || exit 1
    conda install -y -n base -c conda-forge mamba boa pip  || exit 1
    if [ "$(conda env list | awk '{print $1}' | grep $env)" = "" ]; then
        conda env create --file ${my_conda_base}/environment.yml  || exit 1
    fi
    conda env update -n $env --file ${my_conda_base}/dev_env.yml  || exit 1

    local env_dir=$(conda env list | grep "/${env}$" | awk '{print $NF}')
    local platform=$(conda info | grep platform | awk '{print $NF}')
    if [ "$(which gcc)" = "" ] && [ -e ${my_conda_base}/$platform ]; then
        conda env update -n $env --file ${my_conda_base}/${platform}/platform.yaml --prune

        shopt -s nullglob
        local cc=${env_dir}/bin/*gcc
        local cpp=${env_dir}/bin/*g++
        if [ "$cc" = "" ] || [ "$cpp" = "" ]; then
            echo "GCC/G++ not found"
            exit 1
        fi
        mkdir -p ${env_dir}/etc/conda/activate.d
        cat << EOF > ${env_dir}/etc/conda/activate.d/gcc_activate.sh
#!/bin/sh
export CC=$cc
export CXX=$cpp
EOF

        mkdir -p ${env_dir}/etc/conda/deactivate.d
        cat << EOF > ${env_dir}/etc/conda/deactivate.d/gcc_deactivate.sh
#!/bin/sh
unset CC
unset CXX
EOF

    fi
}