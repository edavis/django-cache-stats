from setuptools import setup, find_packages

setup(
    name='django-cache-stats',
    version="0.1-dev",
    description="Monitor your memcached servers",
    long_description=open('README.rst').read(),
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Django",
        "Environment :: Web Environment",
    ],
    keywords='memcached,django',
    author='Eric Davis',
    author_email='ed@npri.org',
    url='http://github.com/edavis/django-cache-stats/',
    license='BSD',
    packages=find_packages(),
    zip_safe=False,
    install_requires=['setuptools'],
    include_package_data=True,
)
