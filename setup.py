from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="job_scraper",
    version="0.1.0",
    author="Taiki Iwamura",
    author_email="takki.0206@gmail.com",
    description=("Python package for scraping job events"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/t-iwamura/job-scraper",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    include_package_data=True,
    python_requires=">= 3.8",
    install_requires=[
        "beautifulsoup4",
        "selenium",
        "click",
    ],
    entry_points={
        "console_scripts": [
            "job-scraper=job_scraper.scripts.main:main",
        ]
    },
)
