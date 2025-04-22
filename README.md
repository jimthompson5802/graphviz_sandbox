# Graphviz Sandbox

This assumes a minimal Ubunutu x86 docker container with miniconda installed.  See files in `.devcontainer` for more information.


```bash
# create skeleton conda environment
conda create -n myenv -y python=3.11 ipykernel jupyter

# activate the environment
conda activate myenv

# install other dependencies
conda install -n myenv -y -c conda-forge graphviz python-graphviz xorg-libxrender 
```