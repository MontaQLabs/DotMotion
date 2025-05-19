from setuptools import setup

setup(
    name="dotmotion",
    version="0.1.0",
    author="MontaQLabs",
    author_email="info@montaqlabs.com",
    description=(
        "Animation toolkit for creating Polkadot ecosystem visualizations"),
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/MontaQLabs/DotMotion",
    py_modules=["dotmotion"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "manim>=0.17.0",
        "numpy>=1.20.0",
    ],
)
