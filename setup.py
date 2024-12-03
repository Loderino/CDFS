from setuptools import setup, find_packages

setup(
    name="CDFS",
    version="0.0.0",
    packages=find_packages(),
    install_requires=[
        "faiss-cpu==1.9.0.post1",
        "fasttext==0.9.3",
        "numpy==2.1.3",
        "python-magic==0.4.27"
        "scikit-learn==1.5.2",
        "watchdog==6.0.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Linux",
    ],
    python_requires=">=3.11",
)
