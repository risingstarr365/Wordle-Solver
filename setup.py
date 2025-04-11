from setuptools import setup, find_packages

setup(
    name="quantum-wordle-solver",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "qiskit>=0.45.0",
        "qiskit-aer>=0.12.0",
        "qiskit-ibm-runtime>=0.37.0",
        "numpy>=1.24.0",
        "matplotlib>=3.7.0",
        "pylatexenc>=2.10"
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A quantum computing-based Wordle solver using Grover's algorithm",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/quantum-wordle-solver",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
) 
