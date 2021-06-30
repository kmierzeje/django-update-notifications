import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    author='Kamil Mierzejewski',
    name='django-update-notifications',
    version='0.1.5',
    description='A framework for sending e-mail notifications about model updates.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    install_requires=['django>=3.0.8'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
    ],
)
