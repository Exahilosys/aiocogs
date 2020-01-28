import setuptools

with open('README.md') as file:

    readme = file.read()

name = 'aiocogs'

version = '1.3.6'

author = 'Exahilosys'

url = f'https://github.com/{author}/{name}'

download_url = f'{url}/archive/v{version}.tar.gz'

setuptools.setup(
    name = name,
    version = version,
    author = author,
    author_email = 'exahilosys@gmail.com',
    url = url,
    download_url = download_url,
    packages = setuptools.find_packages(),
    license = 'MIT',
    description = 'Utilities for asyncio.',
    long_description = readme,
    long_description_content_type = 'text/markdown'
)
