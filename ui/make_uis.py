
import os

app = "c:\\Apps\\Anaconda\\envs\\py38\\Scripts\\pyuic5.exe"

files = [
    "application",
    "setup",
    "action_dialog",
    "run_dialog"
    ]

def main():

    for file in files:
        os.system(f"{app} {file}.ui > ui_{file}.py")

if __name__ == '__main__':
    main()
