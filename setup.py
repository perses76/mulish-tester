from distutils.core import setup

setup(
    name='MulishTester',
    version='0.1.0',
    author='Wadim Ovcharenko',
    author_email='wadim@veles-soft.com',
    packages=['mulishtester', 'mulishtester.test'],
    scripts=[],
    url='https://github.com/perses76/mulish-tester',
    license='MIT',
    description='Test data object generator. Fixture replacement',
    long_description=open('README.rst').read(),
    keywords=['factory', 'test', 'fixtures', 'generators'],
    install_requires=[
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)