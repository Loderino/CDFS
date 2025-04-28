from setuptools import setup, find_packages

setup(
    name="CDFS",
    version="0.0.0",
    packages=find_packages(),
    install_requires=[
        "faiss-cpu==1.9.0.post1",
        "fasttext==0.9.3",
        "numpy==1.26.4",
        "pillow==10.4.0",
        "pymorphy3==2.0.3"
        "python-magic==0.4.27",
        "scikit-learn==1.5.2",
        "tensorflow==2.17.0",
        "tqdm==4.67.1",
        "watchdog==6.0.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Linux",
    ],
    python_requires=">=3.11",
)
