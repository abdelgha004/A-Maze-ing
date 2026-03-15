import sys
from typing import Union


def read_config(filename: str) -> dict:

    config = {}
    try:
        with open(filename) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    print(f"Error: invalid config line (missing '='):"
                          f"'{line}'")
                    sys.exit(1)
                key, raw = line.split("=", 1)
                key = key.strip().upper()
                raw = raw.strip()
                value: Union[str, int, bool, tuple[int, int]] = raw

                if key in ("WIDTH", "HEIGHT"):
                    try:
                        int_value = int(raw)
                        if key == "WIDTH" and int_value > 50:
                            print(f"Error:'{key}' must be <= 50,"
                                  f" got '{raw}'")
                            sys.exit(1)
                        elif key == "HEIGHT" and int_value > 50:
                            print(f"Error:'{key}' must be <= 50,"
                                  f" got '{raw}'")
                            sys.exit(1)
                        value = int_value
                    except ValueError:
                        print(f"Error: '{key}' must be an integer,"
                              f"got '{raw}'")
                        sys.exit(1)
                elif key in ("ENTRY", "EXIT"):
                    try:
                        parts = tuple(map(int, raw.split(",")))
                        if len(parts) != 2:
                            raise ValueError
                        value = (parts[0], parts[1])
                    except ValueError:
                        print(f"Error: '{key}' must be a tuple of two integers"
                              f" like '0,1', got '{raw}'")
                        sys.exit(1)
                elif key == "PERFECT":
                    if raw.lower() not in ("true", "false"):
                        print(f"Error: 'PERFECT' must be 'true' or 'false',"
                              f" got '{raw}'")
                        sys.exit(1)
                    if raw.lower() == "true":
                        value = True
                    else:
                        value = False
                elif key == "SEED":
                    try:
                        value = int(raw)
                    except ValueError:
                        print(f"Error: '{key}' must be an integer,"
                              f"got '{raw}'")
                        sys.exit(1)
                elif key == "ALGORITHM":
                    if raw not in ("dfs", "DFS", "BT", "bt"):
                        print(f"Error: '{key}' must be 'dfs' or 'bt',"
                              f"got '{raw}'")
                        sys.exit(1)
                config[key] = value
        return config

    except FileNotFoundError:
        print(f"{filename}: No such file or directory")
        sys.exit(1)
    except ValueError as e:
        print(f"Error parsing config: {e}")
        sys.exit(1)


def validate_config(config: dict) -> None:

    required_keys = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE",
                     "PERFECT"]
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Missing required key: {key}")

    if config["OUTPUT_FILE"].strip() == "":
        raise ValueError("OUTPUT_FILE cannot be empty.")

    if config["WIDTH"] <= 0 or config["HEIGHT"] <= 0:
        raise ValueError("WIDTH and HEIGHT must be != 0"
                         "and positive integers.")

    entry_r, entry_c = config["ENTRY"]
    exit_r, exit_c = config["EXIT"]

    valid_entry = (0 <= entry_r < config["HEIGHT"]) and \
        (0 <= entry_c < config["WIDTH"])
    valid_exit = (0 <= exit_r < config["HEIGHT"]) and \
        (0 <= exit_c < config["WIDTH"])

    if not valid_entry:
        raise ValueError("ENTRY position out of bounds.")

    if not valid_exit:
        raise ValueError("EXIT position out of bounds.")

    if config["ENTRY"] == config["EXIT"]:
        raise ValueError("ENTRY and EXIT positions cannot be the same.")
