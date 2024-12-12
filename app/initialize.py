from pathlib import Path

def read_env_file():
    env_vars = {}
    with open(Path(__file__).resolve().parent.parent / '.env') as file:
        for line in file:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                env_vars[key] = value
    return env_vars

env_vars = read_env_file()