# Rocky Horror Casting Application

Takes in information about cast roles and outputs all available casts.

## Usage

1. Create CSV files for roles and preferences using the examples in `tests/fixtures` and place them in the `data/` folder using the names `roles.csv` and `preferences.csv`.

2. Set up your environment by running:

    ```{bash}
    pip install poetry
    poetry install
    ```

3. Run the following python in the terminal or use the VSCode launch.json file below:

    ```{bash}
    poetry run python main.py 
    ```

    ```{json}
    {
        "version": "0.2.0",
        "configurations": [
            {
                "name": "Python Debugger: Module",
                "type": "debugpy",
                "request": "launch",
                "module": "main",
            }
        ]
    }
    ```

After running, this will write to `outfile.csv` with a sheet of all possible casts as well as a preference score for each cast based on the preferences provided.

The preferences are scaled by 0.75 for Trixie, 0.5 for Eddie and Scott, and 0.25 for crew, 1 for all other roles.

## Deliverable Goals

### v0.1.0 (MVP) __DONE__

- Get All Valid Casts locally
- Output this cast to a file

### v0.2.0

- Use cloud storage for data files (preferably gdocs)

### v0.3.0 __IN_PROGRESS__

- Order Casts by Preference
- (stretch) Order Casts by historical performance

### v1.0.0

- Use APIs to have user-friendly product (filtering and such)