import setuptools

setuptools.setup(
    name='remote_eval',
    version='0.0.0',
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        'Flask',
    ],
)
