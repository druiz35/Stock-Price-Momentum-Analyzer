from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='stock-momentum-analyzer',
    version='1.0.0',
    description='A financial analysis tool for identifying momentum patterns in stock prices using sliding window techniques',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Financial Analysis Team',
    python_requires='>=3.8',
    packages=find_packages(),
    install_requires=[
        'numpy>=1.21.0',
        'pandas>=1.3.0',
    ],
    entry_points={
        'console_scripts': [
            'stock-analyzer=src.cli:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Financial and Insurance Industry',
        'Topic :: Office/Business :: Financial :: Investment',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
