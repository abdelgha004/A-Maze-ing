import sys


def read_config(filename):

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
                key, value = line.split("=", 1)
                key = key.strip().upper()
                value = value.strip()

                if key in ("WIDTH", "HEIGHT"):
                    try:
                        value = int(value)
                        if key == "WIDTH" and value > 50:
                            print(f"Error:'{key}' must be <= 50,"
                                  f" got '{value}'")
                            sys.exit(1)
                        elif key == "HEIGHT" and value > 50:
                            print(f"Error:'{key}' must be <= 50,"
                                  f" got '{value}'")
                            sys.exit(1)
                    except ValueError:
                        print(f"Error: '{key}' must be an integer,"
                              f"got '{value}'")
                        sys.exit(1)
                elif key in ("ENTRY", "EXIT"):
                    try:
                        value = tuple(map(int, value.split(",")))
                        if len(value) != 2:
                            raise ValueError
                    except ValueError:
                        print(f"Error: '{key}' must be a tuple of two integers"
                              f" like '0,1', got '{value}'")
                        sys.exit(1)
                elif key == "PERFECT":
                    if value.lower() not in ("true", "false"):
                        print(f"Error: 'PERFECT' must be 'true' or 'false',"
                              f" got '{value}'")
                        sys.exit(1)
                    value = value.lower() == "true"
                elif key == "SEED":
                    try:
                        value = int(value)
                    except ValueError:
                        print(f"Error: '{key}' must be an integer,"
                              f"got '{value}'")
                        sys.exit(1)
                elif key == "ALGORITHM":
                    if value not in ("dfs", "DFS", "BT", "bt"):
                        print(f"Error: '{key}' must be 'dfs' or 'bt',"
                              f"got '{value}'")
                        sys.exit(1)
                config[key] = value
        return config

    except FileNotFoundError:
        print(f"{filename}: No such file or directory")
        sys.exit(1)
    except ValueError as e:
        print(f"Error parsing config: {e}")
        sys.exit(1)


def validate_config(config):

    required_keys = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE",
                     "PERFECT"]
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Missing required key: {key}")

    if config["OUTPUT_FILE"].strip() == "":
        raise ValueError("OUTPUT_FILE cannot be empty.")

    if config["WIDTH"] <= 0 or config["HEIGHT"] <= 0:
        raise ValueError("WIDTH and HEIGHT must be positive integers.")

    entry_x, entry_y = config["ENTRY"]
    exit_x, exit_y = config["EXIT"]

    valid_entry = (0 <= entry_x < config["WIDTH"]) and \
        (0 <= entry_y < config["HEIGHT"])
    valid_exit = (0 <= exit_x < config["WIDTH"]) and \
        (0 <= exit_y < config["HEIGHT"])

    if not valid_entry:
        raise ValueError("ENTRY position out of bounds.")

    if not valid_exit:
        raise ValueError("EXIT position out of bounds.")

    if config["ENTRY"] == config["EXIT"]:
        raise ValueError("ENTRY and EXIT positions cannot be the same.")
