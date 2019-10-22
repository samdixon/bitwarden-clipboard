import argparse
import logging
import shutil
import bitwarden_clipboard.core as core

logger = logging.getLogger(__name__)


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="This app")
    parser.add_argument("command", default="fzf", nargs="?")
    parser.add_argument("--update-cache", action="store_true")
    parser.add_argument("--rebase-cache", action="store_true")
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()
    return args

def set_log_level(debug: bool) -> None:
    if debug:
        logging.basicConfig(filename="debug.log", level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

def check_binaries(binaries: list) -> dict:
    values = {}
    for binary in binaries:
        if shutil.which(binary):
            values[binary] = shutil.which(binary)
        else:
            values[binary] = False

    return values

def confirm_binary_values(values: dict) -> bool:
    for key, val in values.items():
        if values[key] == False:
            print(f"Binary {key} not found. Please install before proceeding.")
            exit()
        else:
            return True

def cli():
    args = get_args()
    set_log_level(args.debug)

    confirm_binary_values(check_binaries(["fzf", "bw", "cat"]))

    cachefile = core.Cache()

    account, username = core.fzf_interop(cachefile.file_path)

    core.password_to_clipboard(core.fetch_password(account, username, core.session))
