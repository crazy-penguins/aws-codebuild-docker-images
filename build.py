####
#  Tags and pushes our docker image to ecr
####

import os
import subprocess


with open('NAME', 'r') as f:
    image_name = f.read()
    image_name = image_name.strip()
ref = os.environ.get('CODEBUILD_WEBHOOK_TRIGGER', 'branch/master')
is_tag = ref.startswith('tag/')
is_branch = ref.startswith('branch/')
version = ref.rsplit('/', 1)[-1].strip()
if is_tag and version.startswith('v'):
    version = version[1:]
account_id = os.environ['AWS_ACCOUNT_ID']
region = os.environ['AWS_DEFAULT_REGION']
registry_url = f'{account_id}.dkr.ecr.{region}.amazonaws.com'
try:
    subprocess.run(
        [ 'docker', 'pull', f'{registry_url}/{image_name}:latest', ],
        check=True)
    subprocess.run(
        [ 'docker', 'build', '--cache-from',
          f'{registry_url}/{image_name}:latest',
          '-t', f'{image_name}:{version}', '.' ],
        check=True)
except:  # on the first build, we won't have a latest!
    subprocess.run(
        [ 'docker', 'build', '-t', f'{image_name}:{version}', '.' ],
        check=True)
subprocess.run(
    [ 'docker', 'images', ],
    check=True)
