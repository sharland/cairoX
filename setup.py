from setuptools import setup

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='cairoX',
    url='https://github.com/sharland/cairoX',
    author='Brian Sharland',
    author_email='tyhopho@gmail.com',
    # Needed to actually package something
    packages=['cairoX'],
    # Needed for dependencies
    install_requires=['numpy','math'],
    # *strongly* suggested for sharing
    version='0.1',
    # The license can be anything you like
    license='MIT',
    description='Additional functions for the pycairo module',
    # We will also need a readme eventually (there will be a warning)
    long_description=open('README.md').read(),
)
