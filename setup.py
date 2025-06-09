# this will help create the ML project as an application which can then be downloaded or containorized
from setuptools import find_packages,setup
from typing import List
H_DOT='-e .'

def get_requirements(file_path: str) -> List[str]:
    requirements = []
    with open(file_path) as file_obj:
        for line in file_obj:
            req = line.strip()
            if req and req != H_DOT and not req.startswith("#"):
                requirements.append(req)
    return requirements
setup(
    name='e2e_MLProject',
    version='12.8.2',
    author="Shubham",
    author_email='shubham23official@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)