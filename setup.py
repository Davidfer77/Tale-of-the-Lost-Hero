from setuptools import setup

setup(
    name="TotLH",
    version="0.0.1",
    packages=["TotLH"],
    install_requires=["pygame"],
    entry_points={
        "console_scripts": [
            "TotLH = TotLH.__main__:main"
        ]
    }
)