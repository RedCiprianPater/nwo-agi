from setuptools import setup, find_packages

setup(
    name="nwo-agi",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.28.0",
        "asyncio",
    ],
    entry_points={
        "console_scripts": [
            "nwo-agi=nwo_agi.cli:main",
        ],
    },
)
