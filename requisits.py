from subprocess import Popen
from getpass import getpass
import platform
import os
import shutil

urs = 'urs.earthdata.nasa.gov'
homeDir = os.path.expanduser("~") + os.sep

# 1. Criar .urs_cookies e .dodsrc
with open(homeDir + '.urs_cookies', 'w') as file:
    file.write('')
with open(homeDir + '.dodsrc', 'w') as file:
    file.write(f'HTTP.COOKIEJAR={homeDir}.urs_cookies\n')
    file.write(f'HTTP.NETRC={homeDir}.netrc\n')
print('Saved .urs_cookies and .dodsrc to:', homeDir)

if platform.system() == "Windows":
    shutil.copy2(homeDir + '.dodsrc', os.getcwd())
    print('Copied .dodsrc to working directory:', os.getcwd())

# 2. Criar .netrc
prompts = ['Enter NASA Earthdata Login Username: ', 'Enter NASA Earthdata Login Password: ']
username = input(prompts[0])
password = getpass(prompts[1])

with open(homeDir + '.netrc', 'w') as file:
    file.write(f'machine {urs} login {username} password {password}\n')
print('Saved .netrc to:', homeDir)

if platform.system() != "Windows":
    Popen('chmod og-rw ~/.netrc', shell=True)