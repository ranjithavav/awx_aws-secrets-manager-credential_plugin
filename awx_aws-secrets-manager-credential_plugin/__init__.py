import collections
import boto3
from botocore.exceptions import ClientError
CredentialPlugin = collections.namedtuple('CredentialPlugin', ['name', 'inputs', 'backend'])

def aws_secretsmanager_role_backend(**kwargs):
    iam_role = kwargs.get['iam_role']
    region_name = kwargs.get('region_name')
    secret_name = kwargs.get('secret_name')

    sts_client = boto3.client('sts')
    assumed_role_object = sts_client.assume_role(RoleArn=iam_role, RoleSessionName="AssumeRoleSessionAWX")
    credentials=assumed_role_object['Credentials']
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name, aws_secret_access_key=credentials['SecretAccessKey'], aws_access_key_id=credentials['AccessKeyId'], aws_session_token=credentials['SessionToken'])

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        raise e
    
    if 'SecretString' in get_secret_value_response:
        secret = get_secret_value_response['SecretString']
    else:
        secret = get_secret_value_response['SecretBinary']
    return secret


aws_cred_role_plugin = CredentialPlugin(
    'BF AWS Secrets Lookup',
    inputs={
        'fields': [{
            'id': 'iam_role',
            'label': 'IAM ROLE ARN',
            'type': 'string',
        }],
        'metadata': [
        {
            'id': 'region_name',
            'label': 'AWS Secrets Manager Region',
            'type': 'string',
            'help_text': 'Region which the secrets manager is located',
        },
        {
            'id': 'secret_name',
            'label': 'AWS Secret Name',
            'type': 'string',
        },
        ],
        'required': ['iam_role', 'region_name', 'secret_name'],
    },
    backend = aws_secretsmanager_role_backend
)