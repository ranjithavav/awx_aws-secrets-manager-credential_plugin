#!/usr/bin/env python
from setuptools import setup
requirements = ["boto3", "botocore" ] 
setup(
    name='awx_aws-secrets-manager-credential_plugin',
    version='0.1',
    author='Ansible, Inc.',
    author_email='info@ansible.com',
    description='',
    long_description='',
    license='Apache License 2.0',
    keywords='ansible',
    url='',
    packages=['awx_aws-secrets-manager-credential_plugin'],
    include_package_data=True,
    zip_safe=False,
    setup_requires=[],
    install_requires=requirements,
    entry_points = {
        'awx.credential_plugins': [
            'aws_cred_role_plugin = awx_aws-secrets-manager-credential_plugin:aws_cred_role_plugin',
        ]
    }
)
