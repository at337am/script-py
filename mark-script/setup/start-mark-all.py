import subprocess

def run_mark(file, date, *params):
    command = ["python3", "./mark.py", file, date] + list(params)
    subprocess.run(command)

files_pos = {
    "0_saved": ["1444", "1544"],
    "9_saved": ["1365", "1600"],
    "20_saved": ["758", "958"],
    "23_saved": ["509", "609"],
    "27_saved": ["868", "1020"],
}

date = '20240827'

for i in range(29):
    file = f"{i}_saved"
    if file in files_pos:
        run_mark(file, date, *files_pos[file])
    else:
        run_mark(file, date)
