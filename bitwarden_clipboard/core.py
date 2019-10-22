import os
import json
from subprocess import Popen, PIPE
from bitwarden_keyring import bw, get_session, get_password
import pyperclip

session = get_session(os.environ)

class Cache():
    def __init__(self):
        self.cache_dir = os.path.expanduser("~/.config/bitwarden_clipboard/")
        self.cache_file = "cache.txt"
        self.file_path = os.path.expanduser(
                f"{self.cache_dir}{self.cache_file}")
        self.cache_last_update = "never" # to be completed at a later time
        self._generate_cache_path()
        self.cache_list = self._generate_cache_list()
        self._write_cache()


    def _generate_cache_path(self):
        try: 
            os.mkdir(self.cache_dir)
        except FileExistsError:
            pass

    def _get_cache_date(self):
        pass

    @staticmethod
    def _get_bw_items():
        #session = get_session(os.environ)
        t = bw("list", "items", session=session)
        t = t.decode("utf-8")
        return t

    @staticmethod
    def _load_bw_items(bw_items: str) -> dict:
        return json.loads(bw_items)

    @staticmethod
    def _create_cache_list(bw_dict: dict) -> list:
        l = []
        for item in bw_dict:
            try:
                name = item['name']
                user = item['login']['username']
                l.append(f"{name} | {user}")
            except KeyError:
                pass # Eventuallog
        return l

    def _generate_cache_list(self) -> list:
        bi = self._get_bw_items()
        bd = self._load_bw_items(bi)
        cache_list = self._create_cache_list(bd)
        bi = ""
        return cache_list

    def _write_cache(self):
        with open(self.file_path, 'w') as f:
            for line in self.cache_list:
                f.writelines(f"{line}\n")
        
        

def fzf_interop(file: str) -> str:
    cat = Popen(["cat", f"{file}"], stdout=PIPE)
    fzf = Popen(["fzf"], stdin=cat.stdout, stdout=PIPE)
    cat.stdout.close()
    out, err = fzf.communicate()
    outstring = str(out.strip().decode("utf-8"))
    s1, s2 = outstring.split("|")
    return s1,s2

def fetch_password(account: str, user: str, session: str) -> str:
    return get_password(account.strip(), user.strip(), session)


def password_to_clipboard(password: str) -> None:
    pyperclip.copy(password)
