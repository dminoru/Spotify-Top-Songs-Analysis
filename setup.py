from setuptools import setup
from setuptools import find_packages

# list dependencies from file
with open('requirements.txt') as f:
    content = f.readlines()
requirements = [x.strip() for x in content]

setup(name='song_analysis',
      description="package description",
      packages=find_packages(),
      install_requires=requirements,
      scripts=['scripts/song_analysis-run'])
