# What is this?

This repository holds the Dockerfile for the avian docker-in-docker
codebuild base (known affectionately as dnd).  We gratefully cribbed off
of the official curated docker images.  For more information on codebuild,
please refer to [the AWS CodeBuild User Guide](http://docs.aws.amazon.com/codebuild/latest/userguide/build-env-ref.html).
You can find the latest official releases from AWS [here](https://github.com/aws/aws-codebuild-docker-images/releases)

# What all is included

By default, this container will include the following:

*  python 3.7
*  docker & docker-compose
*  git
*  node & npm
*  chrome
*  firefox 

![Build Status](https://codebuild.us-east-2.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoiYnJoNmVCUmxwQnFienlpc0xFcmp4ODhoYmFZWmJ3QXphNVNSL0lqcVEyUDVIaVBSS1BlSEpmMWJDZ3hZNGJKaFZZUFV4ajZPSkk3MFQ1cXorNklJYmNjPSIsIml2UGFyYW1ldGVyU3BlYyI6InJIOU8rUGh6aitCV2ZCMHkiLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=master)

The master branch will sometimes have changes that are still in the process 
of being released.

### How to build Docker images

Steps to build 

* Run `git clone https://github.com/crazy-penguins/dnd.git`
* Run `docker build -t crazy-penguins/dnd .` to build Docker image locally

To poke around in the image interactively, build it and run:
`docker run -it --entrypoint sh  crazy-penguins/dnd -c bash`

To let the Docker daemon start up in the container, build it and run:
`docker run -it --privileged  crazy-penguins/dnd bash`

```
$ git clone https://github.com/crazy-penguins/dnd
$ cd dnd
$ docker build -t  crazy-penguins/dnd .
$ docker run -it --entrypoint sh  crazy-penguins/dnd -c bash
```

