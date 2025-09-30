# [misc] Imageception &mdash; Write Up

First, pull the image from Docker Hub.

```bash
docker pull react16/litectfchallenge
```

## Peeking inside the container

Running

```bash
docker run -it --entrypoint /bin/sh react16/litectfchallenge
```

gives us an interactive terminal with the Docker image. If we run `ls`, we see a file named `flag.png`

But how do we get it out of the container?

## Option 1: Exporting the running container

```bash
docker export --output="imageception.tar" "<CONTAINER_ID>"
```

would give us a tarball of the Docker container.

## Option 2: Saving the image

```bash
docker image save --output="imageception.tar" react16/litectfchallenge
```

would similarly give us a tarball of the Docker container.

## Getting the flag

Extract the tarball and look for `flag.png`. You will be able to open `flag.png` locally.

## Concluding

There are probably other, crazier ways of getting the PNG file out of the container. But these two are pretty straightforward in my opinion.
