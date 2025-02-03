from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess
import sys

class CustomInstall(install):
    def run(self):
        install.run(self)
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--force', 'ruamel.yaml'])

setup(
    name="mcdis_rcon",
    version="0.4.5a",
    packages=find_packages(),
    include_package_data=True,
    package_data={
    },
    entry_points={
        'console_scripts': [
            'mcdis=mcdis_rcon.scripts.cli:main',
        ],
    },
    install_requires=[
        'polib',
        'psutil',
        'discord.py',
        'flask',
        'requests',
        'nbtlib',
        'requests'
    ],
    cmdclass={
        'install': CustomInstall,
    },
)
