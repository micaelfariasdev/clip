import subprocess

def notify(type = 'Aviso', msg = 'TEste'):
    subprocess.run(["notify-send", type, msg])


if __name__ == '__main__':
    notify()