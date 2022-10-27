# Network Analysis Project Repository (Group 12)

## Members

- Emil Dichmann
- Adam Isaac Wistoft
- Jan Piroutek
- Gustav Kristensen
- Arnór Ingi Grétarsson
- Lini Zhang

## Setup

Run `sh setup.sh` to setup the directory structure and download the dataset.
Store data in `data/` and any user specific files that should not be committed
in `user/`. The config file is located at `user/config.json` and you can change
in that file whether you by default want to save/cache graphs and change the
default data/cache paths.

## Repository structure

The default directory structure is as follows:

- Data (ignored by git)
  - Compressed
    - Here you can store compressed files, such as the rotten_tomatoes.zip that
      gets downloaded during setup
  - Extracted
    - Here you can store extracted data such as `.csv` files
  - Cache
    - Here you can store cache such as pickled graphs, etc.
- User (ignored by git)
  - `config.json`
    - User configuration of defaults is stored here
    - You can either pass the config path as an argument to `create_graph`,
      or set the environment variable `NAL_CONFIG_PATH`
- nal
  - Python module with code for generating the graph and doing stuff with it
  - You can install the module with `python -m pip install -e .` in the `nal` directory and use it with `import nal`
    - If you have the environment variable for the config path set, it should use your config file automatically
