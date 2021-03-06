import ast
import codecs
import os
import re

from setuptools import setup


def read(*parts):
    """
    Build an absolute path from *parts* and and return the contents of the
    resulting file.  Assume UTF-8 encoding.
    """
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, *parts), 'r', 'utf-8') as f:
        return f.read()


def find_version(*file_paths):
    """
    Build a path from *file_paths* and search for a ``__version__``
    string inside.
    """

    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ =\s*(.*)$", version_file, re.M)
    if version_match:
        txt = version_match.group(1)
        numVersion = ast.literal_eval(txt)
        return ".".join(str(el) for el in numVersion)
    raise RuntimeError("Unable to find version string.")


if __name__ == "__main__":
    setup(
        classifiers=[
            'Environment :: Web Environment',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: Implementation :: CPython',
            'Programming Language :: Python :: Implementation :: PyPy',
            'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
            'Topic :: Software Development :: Libraries :: Python Modules'
        ],
        description="klein + injector",
        long_description=read('README.rst'),
        install_requires=[
            "klein"
        ],
        keywords="klein injector",
        license="MIT",
        name="klein-injector",
        packages=["klein_injector"],
        url="https://github.com/VRGhost/klein_injector",
        version=find_version('klein_injector', '__init__.py'),
        maintainer='Ilja Orlovs',
        maintainer_email='vrghost@gmail.com',
    )
