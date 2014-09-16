import distutils.core

distutils.core.setup(
    name='Ymir',
    author='Karl Dubost',
    author_email='karl+ymir@la-grange.net',
    version='0.1dev',
    packages=['ymir', ],
    license='LICENSE.txt',
    url='http://pypi.python.org/pypi/Ymir/',
    description='script to manage La Grange blog http://www.la-grange.net/',
    long_description=open('README.txt').read(),
)
