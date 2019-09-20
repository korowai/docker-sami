# korowai/docker-sami

[![](https://img.shields.io/docker/stars/korowai/sami.svg)](https://hub.docker.com/r/korowai/sami/ "Docker Stars")
[![](https://img.shields.io/docker/pulls/korowai/sami.svg)](https://hub.docker.com/r/korowai/sami/ "Docker Pulls")

Docker container with [sami](https://github.com/FriendsOfPHP/Sami/)
documentation generator. The container is designed to build PHP API
documentation for [Korowai](https://github.com/korowai/korowai/) and
[Korowai Framework](https://github.com/korowai/framework/) out of the
box. It may be easily adjusted to support other projects.

## Image versions

  - [![](https://images.microbadger.com/badges/version/korowai/sami.svg)](https://microbadger.com/images/korowai/sami "Get your own version badge on microbadger.com") [![](https://images.microbadger.com/badges/image/korowai/sami.svg)](https://microbadger.com/images/korowai/sami "Get your own image badge on microbadger.com")
  - [![](https://images.microbadger.com/badges/version/korowai/sami:7.2-alpine.svg)](https://microbadger.com/images/korowai/sami:7.2-alpine "Get your own version badge on microbadger.com") [![](https://images.microbadger.com/badges/image/korowai/sami:7.2-alpine.svg)](https://microbadger.com/images/korowai/sami:7.2-alpine "Get your own image badge on microbadger.com")
  - [![](https://images.microbadger.com/badges/version/korowai/sami:7.1-alpine.svg)](https://microbadger.com/images/korowai/sami:7.1-alpine "Get your own version badge on microbadger.com") [![](https://images.microbadger.com/badges/image/korowai/sami:7.1-alpine.svg)](https://microbadger.com/images/korowai/sami:7.1-alpine "Get your own image badge on microbadger.com")

## Features

With this container you can:

  - build documentation once and exit,
  - build documentation once and then serve it with http server,
  - build documentation continuously (rebuilding when sources change),
  - build documentation continuously and serve it at the same time.

The default behavior is to build continuously and serve at the same time.

## Quick example

Assume we have the following file hierarchy (the essential here is assumption
that php source files are found under `src`, also we expect the documentation
to be written-out somewhere under `docs`)

```console
user@pc:$ tree .
.
|-- docs
`-- src
    `-- Foo
        `-- Bar.php
```

### Running with docker

Run it as follows

```console
user@pc:$ docker run --rm -it -v "$(pwd):/code" -p 8001:8001 korowai/sami
```

### Running with docker-compose

In the top level directory create `docker-compose.yml` containing the following

```yaml
version: '3'
# ....
services:
   # ...
   sami:
      image: korowai/sami
      ports:
         - "8001:8001"
      volumes:
         - ./:/code
```

Then run

```console
user@pc:$ docker-compose up sami
```

### Results

Whatever method you chose to run the container, you shall see two new directories

```console
user@pc:$ ls -d docs/*
docs/build docs/cache
```

The documentation is written to `docs/build/html/api`

```console
user@pc:$ find docs -name 'index.html'
docs/build/html/api/index.html
```

As long as the container is running, the documentation is available at

  - <http://localhost:8001>.

## Customizing

Several parameters can be changed via environment variables, for example we can
change build to ``build/docs/api`` dir as follows

```console
user@pc:$ docker run --rm -it -v "$(pwd):/code" -p 8001:8001 -e SAMI_BUILD_DIR=build/docs/api korowai/sami
```

## Details

### Volume mount points exposed

  - `/code` - bind top level directory of your project here.

### Working directory

  - `/code`

### Files inside container

#### In `/usr/local/bin`

  - scripts which may be used as container's command:
      - `autobuild` - builds documentation continuously (watches
        source directory for changes),
      - `autoserve` - builds documentation continuously and runs
        http server,
      - `build` - builds documentation once and exits,
      - `serve` - builds source once and starts http server,
  - other files
      - `sami-defaults` - sets `DEFAULT_SAMI_xxx` variables (default
      - `sami-env` - initializes `SAMI_xxx` variables,
      - `sami-entrypoint` - provides an entry point for docker.

#### In `/etc/sami`

  - `sami.conf.php` - default configuration file for sami.

### Build arguments & environment variables

The container defines several build arguments which are copied to corresponding
environment variables within the running container. Most of the arguments/variables
have names starting with `SAMI_` prefix. All the `sami-*` scripts, and the
configuration file `sami.conf.php` respect these variables, so the easiest way
to adjust the container to your needs is to set environment variables (`-e`
flag to [docker](https://docker.com/)).  `KRW_CODE` and `SAMI_PORT` are
exceptions, they must be defined at build time, so they may only be changed via
docker's build arguments.

| Argument             | Default Value            | Description                                            |
| -------------------- | ------------------------ | ------------------------------------------------------ |
| KRW\_CODE            | /code                    | Volume mount point and default working directory.      |
| SAMI\_CONFIG         | /etc/sami/sami.conf.php  | Path to the config file for sami.                      |
| SAMI\_PROJECT\_TITLE | API Documentation        | Title for the generated documentation.                 |
| SAMI\_SOURCE\_DIR    | src                      | Top-level directory with the PHP source files.         |
| SAMI\_BUILD\_DIR     | docs/build/html/api      | Where to output the generated documentation.           |
| SAMI\_CACHE\_DIR     | docs/cache/html/api      | Where to write cache files.                            |
| SAMI\_FLAGS          | -v --force               | Commandline flags passed to sami.                      |
| SAMI\_SERVER\_PORT   | 8001                     | Port numer (within container) for the http server.     |
| SAMI\_SOURCE\_REGEX  | `\.\(php\\|txt\\|rst\)$` | Regular expression for source files' discovery.        |
| SAMI\_THEME          | default                  | Sami theme.                                            |

### Software included

  - [php](https://php.net/)
  - [git](https://git-scm.com/)
  - [sami](https://github.com/FriendsOfPHP/Sami/)

## LICENSE

Copyright (c) 2018 by Paweł Tomulik <ptomulik@meil.pw.edu.pl>

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE
