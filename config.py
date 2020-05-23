import itertools

__version__ = '0.3.3'

def xrepr(arg):
    if isinstance(arg, str):
        return "'%s'" % arg
    else:
        return repr(arg)

def generated_warning(php, os):
    return """\
#############################################################################
# NOTE: FILE GENERATED AUTOMATICALLY, DO NOT EDIT!!!
#############################################################################
"""

def sami_params(php, os):
    """Configuration parameters for sami with their default values"""
    return {'KRW_CODE': '/code',
            'SAMI_CONFIG': '/etc/sami/sami.conf.php',
            'SAMI_PROJECT_TITLE': 'API Documentation',
            'SAMI_SOURCE_DIR': 'src:packages',
            'SAMI_BUILD_DIR': 'docs/build/html/api',
            'SAMI_CACHE_DIR': 'docs/cache/html/api',
            'SAMI_FLAGS': '-v --force',
            'SAMI_SERVER_PORT': 8001,
            'SAMI_SOURCE_REGEX': r'\.\(php\|txt\|rst\)$',
            'SAMI_THEME': 'default'}


def sami_env_defaults_str(php, os):
    items = sami_params(php, os).items()
    return '\n'.join(("DEFAULT_%s=%s" % (k, xrepr(v)) for k, v in items))


def sami_env_settings_str(php, os):
    params = list(sami_params(php, os))
    return '\n'.join(('%s=${%s-$DEFAULT_%s}' % (k, k, k) for k in params))


def docker_sami_args_str(php, os):
    items = sami_params(php, os).items()
    return '\n'.join(('ARG %s=%s' % (k, xrepr(v)) for k, v in items))


def docker_sami_env_str(php, os):
    params = list(sami_params(php, os))
    return 'ENV ' + ' \\\n    '.join(('%s=$%s' % (k, k) for k in params))


def context_id(php, os, sep):
    return sep.join((php, os))


def context_dir(php, os, sep='/'):
    return context_id(php, os, sep)


def context_tag(php, os, sep='-'):
    return context_id(php, os, sep)


def context_files(php, os):
    return {'Dockerfile.in': 'Dockerfile',
            'etc/sami.conf.php.in': 'etc/sami.conf.php',

            'bin/autobuild.in': 'bin/autobuild',
            'bin/autoserve.in': 'bin/autoserve',
            'bin/build.in': 'bin/build',
            'bin/build_once.in': 'bin/build_once',
            'bin/sami-defaults.in': 'bin/sami-defaults',
            'bin/sami-entrypoint.in': 'bin/sami-entrypoint',
            'bin/sami-env.in': 'bin/sami-env',
            'bin/serve.in': 'bin/serve',
            'hooks/build.in': 'hooks/build'}


def context_subst(php, os):
    return dict({'GENERATED_WARNING': generated_warning(php, os),
                 'SAMI_ENV_DEFAULTS': sami_env_defaults_str(php, os),
                 'SAMI_ENV_SETTINGS': sami_env_settings_str(php, os),
                 'DOCKER_FROM_TAG': context_tag(php, os),
                 'DOCKER_SAMI_ARGS': docker_sami_args_str(php, os),
                 'DOCKER_SAMI_ENV': docker_sami_env_str(php, os),
                 'VERSION': __version__}, **sami_params(php, os))


def context(php, os):
    return {'dir': context_dir(php, os),
            'files': context_files(php, os),
            'subst': context_subst(php, os)}


phps = ['7.1', '7.2']
oses = ['alpine']
contexts = [context(php, os) for (php, os) in itertools.product(phps, oses)]
del phps
del oses
