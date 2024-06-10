
from setuptools import setup, find_packages

setup(
    name='aim_stats_commune',
    version='0.1.0',
    description='Commune stats collector for AIM',
    author='rohjar.ai',
    author_email='rohjar.ai@gmail.com',
    url='https://github.com/rohjar-ai/rohjar-ai.github.io',
    packages=find_packages(exclude=['tests*']),
    install_requires=[
        line.strip() for line in open('requirements.txt')
    ],
    entry_points={
        'console_scripts': [
            'aim-stats=aim_stats_commune.app:main',
        ],
    },
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Specify the Python versions supported
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.9',
)
