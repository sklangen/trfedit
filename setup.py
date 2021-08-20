from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(
    name='trfedit',
    version='0.0.1',
    author='Schachklub Langen e. V.',
    author_email='Turnierleiter@sklangen.de',
    description='A GUI editor for the fide approved tournament report format: trf',
    license='GPLv3+',
    keywords=['trf', 'fide', 'chess', 'tournaments'],
    packages=['trfedit'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/sklangen/trfedit',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Topic :: Utilities',
    ],
)