# -*- coding: utf-8 -*-

from setuptools import setup
from os import path


VERSION = (0, 1, 0)
__version__ = VERSION
__versionstr__ = '.'.join(map(str, VERSION))

long_description = ''
try:
    f = open(path.join(path.dirname(__file__), 'README.md'))
    long_description = f.read().strip()
    f.close()
except:
    pass


setup(
    name = 'zelenamapa',
    description = "Django aplikace Zelená mapa Prahy http://www.zelenamapa.cz/",
    url = "http://github.com/auto-mat/zelenamapa",
    long_description = long_description,
    version = __versionstr__,
    author = "Auto*Mat",
    author_email = "kontakt@zelenamapa.cz",
    license = "AGPLv3",
    packages = ['zelenamapa', 'zm'],
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3",
    ],
)


