# korowai/docker-sami

Docker container with [sami](https://github.com/FriendsOfPHP/Sami/)
documentation generator. The container is designed to build PHP API
documentation for [Korowai](https://github.com/korowai/korowai/) and
[Korowai Framework](https://github.com/korowai/framework/) out of the
box. It may be easily adjusted to support other projects.

## Features

With this container you can:

  - build documentation once and exit,
  - build documentation once and then serve it with http server,
  - build documentation continuously (rebuilding when sources change),
  - build documentation continuously and serve it at the same time.

The default behavior is to build continuously and serve at the same
time.

## Quick example

Assume we have the following file hierarchy (the essential here is
assumption that php source files are found under `src`, also we expect
the documentation to be written-out somewhere under `docs`)

```console
user@pc:$ tree .
.
|-- docs
`-- src
    `-- Foo
        `-- Bar.php
```

### Running with docker

Run it as
follows

```console
user@pc:$ docker run -v "$(pwd):/home/sami/project" -p 8001:8001 --rm korowai/sami
```

### Running with docker-compose

In the top level directory create `docker-compose.yml` containing the
following

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
         - ./:/home/sami/project
```

Then run

```console
user@pc:$ docker-compose up sami
```

### Results

Whatever method you chose to run the container, you shall see two new
directories

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

Several parameters can be changed via environment variables, for
example

```console
user@pc:$ docker run -v "$(pwd):/home/sami/project" -p 8001:8001 --rm -e SAMI_BUILD_DIR=/tmp/build korowai/sami
```

## Details

### Volume mount points exposed

  - `/home/sami/project` - bind top level directory of your project
    here.

### Working directory

  - `/home/sami/project`

### User running the commands

Commands are executed within container by container's internal user
called `sami`. By default it has `UID=1000` and `GID=1000`, thus all the
generated files will have owner with `UID=1000` and `GID=1000`.

The container may be rebuilt with custom UID and GID by setting build
arguments `SAMI_UID` and `SAMI_GID`.

### Files inside container

#### In `/usr/local/bin`

  - scripts which may be used as container's command:
      - `sami-autobuild` - builds documentation continuously (watches
        source directory for changes),
      - `sami-autoserve` - builds documentation continuously and runs
        http server,
      - `sami-build` - builds documentation once and exits,
      - `sami-serve` - builds source once and starts http server,
  - other files
      - `sami-defaults` - initializes `SAMI_xxx` variables (default
        values),
      - `sami-entrypoint` - provides an entry point for docker.

#### In `/home/sami`

  - `sami.conf.php` - default configuration file for sami.

### Build arguments & environment variables

The container defines several build arguments which are copied to
corresponding environment variables within the running container. All
the arguments/variables have names starting with `SAMI_` prefix. All the
`sami-*` scripts, and the configuration file `sami.conf.php` respect
these variables, so the easiest way to adjust the container to your
needs is to set environment variables (`-e` flag to
[docker](https://docker.com/)). There are three exceptions currently --
`SAMI_UID`, `SAMI_GID` and `SAMI_PORT` must be defined at build time, so
they may only be changed via docker's build
arguments.

| Argument             | Default Value            | Description                                            |
| -------------------- | ------------------------ | ------------------------------------------------------ |
| SAMI\_UID            | 1000                     | UID of the user running commands within the container. |
| SAMI\_GID            | 1000                     | GID of the user running commands within the container. |
| SAMI\_CONFIG         | /home/sami/sami.conf.php | Path to the config file for sami.                      |
| SAMI\_PROJECT\_TITLE | API Documentation        | Title for the generated documentation.                 |
| SAMI\_SOURCE\_DIR    | src                      | Top-level directory with the PHP source files.         |
| SAMI\_BUILD\_DIR     | docs/build/html/api      | Where to output the generated documentation.           |
| SAMI\_CACHE\_DIR     | docs/cache/html/api      | Where to write cache files.                            |
| SAMI\_SERVER\_PORT   | 8001                     | Port numer (within container) for the http server.     |
| SAMI\_SOURCE\_REGEX  | `\.\(php\\|txt\\|rst\)$` | Regular expression for source files' discovery.        |

### Software included

  - [php](https://php.net/)
  - [git](https://git-scm.com/)
  - [sami](https://github.com/FriendsOfPHP/Sami/)

## LICENSE

Copyright (c) 2018 by Paweł Tomulik \<<ptomulik@meil.pw.edu.pl>\>

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE
