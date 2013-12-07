from setuptools import setup, find_packages
from cinch import VERSION


setup(
    name='django-cinch',
    version=VERSION,
    description='Modular, class-based settings for Django',
    long_description=(open('README.rst').read() + '\n\n' +
                      open('COLOPHON.rst').read()),
    url='http://github.com/hipikat/django-cinch/',
    license='BSD 2-Clause',
    author='Adam Wright',
    author_email='adam@hipikat.org',
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 2 :: Only',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
