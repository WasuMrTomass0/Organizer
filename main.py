"""
main.py file for nicegui's Docker service.
To run locally execute src/main.py
"""
import sys
import os


main = 'src/main.py'
requirements = 'requirements.txt'
repo = 'git@github.com:WasuMrTomass0/Organizer.git'


commands = [
    f'apt-get -y update',       # Update all tools in docker's environment
    f'apt-get -y install git',  # Install git
    f'git clone {repo} ./',     # Clone into current working directory
    f'{sys.executable} -V',     # Debug message
    f'{sys.executable} -m pip install -r {requirements}',   # Install requirements
    f'{sys.executable} {main}', # Run server
]

# Execute all commands
for cmd in commands:
    code = os.system(cmd)
    print('# # # # # # # # # # # # # # # # # # # #')
    print('Executed:', cmd, '\nExit code:', code)
