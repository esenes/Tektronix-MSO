from setuptools import setup, find_packages

# long description
with open("README.md", 'r', encoding='utf-8') as fh:
    long_description = fh.read()

# requirements
REQUIREMENTS = ['python-vxi11']

# more details
CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3.6',
]

setup(name='tekscope',
    version='1.0.0',
    description='A python wrapper for GPIB commands for Tektronix scopes',
    url='https://github.com/esenes/Tektronix-MSO',
    author='Eugenio Senes',
    author_email='a@b.ch',
    license='MIT',
    packages=find_packages(),
    classifiers=CLASSIFIERS,
    install_requires=REQUIREMENTS,
    keywords='GPIB oscilloscope scope LXI wrapper',
)