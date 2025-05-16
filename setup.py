from setuptools import setup, find_packages

setup(
    name="physics-text-processor",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'ftfy>=6.1.1',
        'unicodedata2>=14.0.0',
    ],
    python_requires='>=3.6',
) 