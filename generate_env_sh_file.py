import configparser
import json
import os

from json_sample.json_with_comment import JSONWithCommentsDecoder


def gg_account():
    # Load credentials from a JSON file
    with open(
        TREASURE_BOX_PATH + "/Work/Other/credentials_bk/google-account.json", "r"
    ) as f:
        account = json.loads(f.read(), cls=JSONWithCommentsDecoder)[0]
        return {
            "GMAIL_USER": account["email"],
            "GMAIL_APP_PW": account["password"],
        }


def load_env_from_json(filename):
    """Read environment variables from a JSON file, e.g., {"VAR": "value"}."""
    with open(filename, "r") as f:
        data = json.load(f)
    return data


def load_env_from_ini(filename):
    """Read environment variables from an INI file.

    This example will load variables from the DEFAULT section.
    """
    config = configparser.ConfigParser()
    config.read(filename)
    env_vars = dict(config.defaults())
    return env_vars


def load_env_from_env_file(filename):
    """Read environment variables from a .env file (key=value per line)."""
    env_vars = {}
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            # Skip empty lines and comments
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, value = line.split("=", 1)
                env_vars[key.strip()] = value.strip()
    return env_vars


def write_env_script(env_vars, output_file):
    """Generate a shell script that exports environment variables."""
    with open(output_file, "w") as f:
        f.write("#!/bin/bash\n")
        for key, value in env_vars.items():
            f.write(f'export {key}="{value}"\n')
    # Make the script executable.
    os.chmod(output_file, 0o755)


def load_environment_files(file_list):
    """
    Load environment variables from a list of files.
    Supported file types: .json, .ini and .env.
    Files later in the list override variables from files earlier in the list.
    """
    combined_env = {}
    for file in file_list:
        if not os.path.exists(file):
            print(f"Warning: {file} not found. Skipping.")
            continue

        if file.endswith(".json"):
            env = load_env_from_json(file)
            print(f"Loaded environment variables from JSON file: {file}")
        elif file.endswith(".ini"):
            env = load_env_from_ini(file)
            print(f"Loaded environment variables from INI file: {file}")
        elif file.endswith(".env"):
            env = load_env_from_env_file(file)
            print(f"Loaded environment variables from .env file: {file}")
        else:
            print(f"Unsupported file format for {file}. Skipping.")
            continue

        combined_env.update(env)
        combined_env.update(gg_account())
    return combined_env


if __name__ == "__main__":
    TREASURE_BOX_PATH = os.environ["TREASURE_BOX_PATH"]
    # List your environment files here. Order matters: later files override earlier ones.
    env_files = [
        ".env",  # .env file in the workspace root
        "env.ini",  # an INI file
        "env.json",  # a JSON file
        TREASURE_BOX_PATH + "/Work/showheroes/jenkins_account.env",
        TREASURE_BOX_PATH
        + "/Work/Other/credentials_bk/github_basic-token-PhungXuanAnh.env",
    ]

    output_script = "env.sh"
    env_vars = load_environment_files(env_files)
    env_vars["PYTHONPATH"] = f"/home/{os.environ.get('USER')}/repo/python-note"

    if not env_vars:
        print("No environment variables loaded. Please check your environment files.")
        exit(1)

    write_env_script(env_vars, output_script)
    print(
        f"Environment script '{output_script}' generated successfully with the following variables:"
    )
    for key in env_vars:
        print(f"  {key}={env_vars[key]}")
