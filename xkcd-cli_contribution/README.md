# XKCD-cli contribution

The current repository contains a python notebook file and the python dependencies requirements for its use. This tutorial considers only linux users. However, it is possible to adapt it for Windows or Mac users as well by bring of some effort on the subject. 

## How to install

The installation requires some pre-installation steps, with isntructiosn avaialble on following repository: https://github.com/brunolnetto/engage

1) Clone the repository above on folder of choice;
2) Perform the command on its file README.md. RELAX, it will just install necessary packages, and not any harmful package to your system. 
3) Navigate back to this repository; 
4) Activate the virtual repository by name of choice:

```sh
virtualenv .env
```

5) Install python requirements by command below:

```sh
pip install -r pip_requirements.txt
```

6) Run the command below on your terminal: it will open an instance of jupyter notebook on your default browser;

```sh 
jupyter notebook
``` 

7) In opened notebook folder, open the file ```xkcd_index_predictor.ipynb```;
8) Run the necessary cells with ```Shift+Enter```
