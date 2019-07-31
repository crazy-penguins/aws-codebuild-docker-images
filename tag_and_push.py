####
#  Builds our docker image
####

import os
import subprocess
import boto3


with open('NAME', 'r') as f:
    image_name = f.read()
    image_name = image_name.strip()
ref = os.environ['CODEBUILD_WEBHOOK_TRIGGER']
sts = boto3.client('sts')
response = sts.get_caller_identity()
account_id = response['Account']
# account_id = os.environ['CODEBUILD_BUILD_ARN'].rsplit('/', 1)[0]
# account_id = account_id.split(':')[-2]
region = os.environ['AWS_DEFAULT_REGION']
is_tag = ref.startswith('tag/')
is_branch = ref.startswith('branch/')
version = ref.rsplit('/', 1)[-1].strip()
registry_url = f'${account_id}.dkr.ecr.${region}.amazonaws.com'
if is_tag and version.startswith('v'):
    version = version[1:]
final_tags = [
    f'${registry_url}/{image_name}:latest',
]
if is_tag:
    final_tags.append(f'${registry_url}/{image_name}:{version}')
for x in final_tags:
    subprocess.run(
        [ 'docker', 'tag', f'{image_name}:{version}', x, ],
        check=True)
    subprocess.run([
        'docker', 'push', x,
    ], check=True)
