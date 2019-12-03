from setuptools import setup

setup(
    name="wiki_futures",
    packages=["wiki_futures"],
    version="0.0.1",
    description="Asynchronously downloads Wikipedia pages",
    author="Andrew Porter",
    author_email="porter.r.andrew@gmail.com",
    license="MIT License",
    url="https://github.com/AndrewRPorter/wiki-futures",
    download_url="https://github.com/AndrewRPorter/wiki-futures/releases",
    install_requires=["setuptools", "requests", "requests-futures"],
)
