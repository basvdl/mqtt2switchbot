import setuptools

setuptools.setup(
    name="mqtt2switchbot",
    packages=setuptools.find_packages(),
    install_requires=[
        "paho-mqtt==1.5.1",
        "bleak==0.10.0"
    ],
    tests_require=[
        "pytest",
        "flake8",
        "mypy"
    ]
)
