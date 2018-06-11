import subprocess

dir = subprocess.run(
    ['dir'], stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell = True)
print(dir.stdout.decode('gbk'))