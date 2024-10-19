# Rocky Horror Casting Application

Takes in information about cast roles and outputs all available casts.

## Usage

1. Create CSV files for roles and preferences using the examples in `tests/fixtures` and place them in the `data/` folder.

2. Set up your environment by running:
    
    ```{bash}
    pipenv install
    pipenv shell
    ```

3. Run the following python in the terminal or use the VSCode launch.json file below:

    ```{bash}
    python main.py -l Alex Dakota Avery Skyler Jamie Shawn Parker Reese Taylor Cameron Logan 
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
                "args": ["-l", "Alex", "Dakota", "Avery", "Skyler", "Jamie", "Shawn", "Parker", "Reese", "Taylor", "Cameron", "Logan"]
            }
        ]
    }
    ```

    The list of names determines who is available for casting in the show.

After running, this will write to `outfile.csv` with a dataset of all possible casts.

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