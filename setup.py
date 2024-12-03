from setuptools import find_packages, setup

with open("deps/requirements.txt") as f:
    install_requires = f.read()


if __name__ == "__main__":
    setup(
        name="decision_sabotage",
        version="0.1.0",
        url="https://github.com/ConnorWatts/decision_sabotage ",
        license="Apache License 2.0",
        install_requires=install_requires,
        packages=find_packages(),
        python_requires=">=3.11.0",
        zip_safe=True,
    )
