import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python-test-migration-garett-b",
    version="0.0.1",
    author="Garett Beukeboom",
    author_email="beukeboom@gmail.com",
    description="Mock data migrations to various cloud providers",
    include_package_data=True,
    install_requires=["dill"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/garettB/python-test-migration",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    test_suite="test",
)
