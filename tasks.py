####
#  invoke task list
####

import os
import subprocess
from invoke import task


class Builder:
    name = None
    ref = None
    version = None

    @property
    def is_tag(self):
        return self.ref.startswith('tag/')

    @property
    def is_branch(self):
        return self.ref.startswith('branch/')

    def __init__(self):
        with open('NAME', 'r') as f:
            self.name = f.read()
            self.name = self.name.strip()

        self.ref = os.environ.get('CODEBUILD_WEBHOOK_TRIGGER', 'branch/master')
        self.version = ref.rsplit('/', 1)[-1].strip()
        if self.is_tag and self.version.startswith('v'):
            self.version = self.version[1:]

    @property
    def repository_url(self):
        account_id = os.environ['AWS_ACCOUNT_ID']
        region = os.environ['AWS_DEFAULT_REGION']
        return f'{account_id}.dkr.ecr.{region}.amazonaws.com/{self.name}'

    @property
    def build_tag(self):
        return f'{self.name}/{self.version}'


@task
def build(ctx):
    x = Builder()
    try:
        subprocess.run(
            [ 'docker', 'pull', f'{x.repository_url}:latest', ],
            check=True)
        subprocess.run(
            [ 'docker', 'build', '--cache-from',
              f'{x.repository_url}:latest',
              '-t', f'{x.build_tag}', '.' ],
            check=True)
    except:  # on the first build, we won't have a latest!
        subprocess.run(
            [ 'docker', 'build', '-t', f'{x.build_tag}', '.' ],
            check=True)
    subprocess.run(
        [ 'docker', 'images', ],
        check=True)


@task
def tag_and_push(ctx):
    x = Builder()
    final_tags = [
        f'{x.repository_url}:latest',
    ]
    if x.is_tag:
        final_tags.append(f'{x.repository_url}:{x.version}')
    for tag in final_tags:
        subprocess.run(
            [ 'docker', 'tag', f'{x.build_tag}', tag, ],
            check=True)
        subprocess.run([
            'docker', 'push', tag,
        ], check=True)
