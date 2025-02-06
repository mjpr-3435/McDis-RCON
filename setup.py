from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    description = f.read()

setup(
    name="mcdis_rcon",
    version="0.4.9a",
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
        'requests',
        'ruamel.yaml',
    ],
    long_description = description,
    long_description_content_type = 'text/markdown',
    python_requires='>=3.8',
)
