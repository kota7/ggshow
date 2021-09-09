# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='ggwrap',
    version='0.0.1',
    description="Draw graphs using R's ggplot2 from Python script and Jupyter notebook",
    author='Kota Mori',
    author_email='kmori05@gmail.com',
    #url='',
    #download_url='',

    #packages=find_packages(),
    py_modules=['ggwrap'],    
    install_requires=[],
    #test_require=['pytest'],
    package_data={},
    entry_points={},
    
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Pick your license as you wish (should match "license" above)
         'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ]
)
