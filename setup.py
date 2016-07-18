from setuptools import setup, find_packages

setup(
    name = 'recast-search',
    description = 'service to sync db and elastic search instance',
    url = 'https://github.com/cbora/recast-search/',
    author = 'Christian Bora',
    author_email = 'christian.bora@cern.ch',
    packages = find_packages(),
    include_package_data = True,
    install_requires = [
        'pyyaml',
        'recast-api',
        'pyelasticsearch'
    ],
    entry_points = {
        'console_scripts': [
            'recast-search = recastsearch.searchcli:start',
        ]
    },
    dependency_links = [
        'https://github.com/cbora/recast-api/tarball/master#egg=recast-api-0.0.1'
    ]
)
        
   
