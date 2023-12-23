from setuptools import find_packages, setup
from typing import List

#adding -e . in the requirements.txt will automatically triggers the setup.py file hence installing the requirements automatically
CONSTANT='-e .' 
def get_requirements(file_path:str)-> List[str]:
    '''
    this function will return the list of requirements 
    '''
    requirements=[]
    with open(file_path) as file_obj:
        requirements=file_obj.readlines()
    requirements= [req.replace("\n", "") for req in requirements] 

    if CONSTANT in requirements:
        requirements.remove(CONSTANT)

    return requirements        




setup(
name='mle_project',
version='0.0.1',
author='sumit kumar',
author_email='sumit.atlancey@gmail.com',
packages=find_packages(),
install_requires= get_requirements('requirements.txt')
)