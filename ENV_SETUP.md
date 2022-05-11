# Project Setup

This package makes use of the Poetry project manager. First, make sure that you have poetry installed. One can install it using the PyPi package:
```bash
pip install poetry
```

For convenience sake, I prefer to have poetry create the .venv folder in the project directory. To do this, execute the command:

```bash
poetry config virtualenvs.in-project true
```

Now, to get started with using these scripts, run the command 

```bash
poetry install
```

from within the project directory. This will install all required project dependencies from pip, then place them in the .venv folder located in the project directory.

