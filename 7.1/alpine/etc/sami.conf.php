<?php

use Sami\Sami;
use Symfony\Component\Finder\Finder;

function env($var, $default=false)
{
  $env = getenv($var);
  return $env ? $env : $default;
}

$srcdir = env('SAMI_SOURCE_DIR', 'src:packages/*');
$builddir = env('SAMI_BUILD_DIR', 'docs/build/html/api');
$cachedir = env('SAMI_CACHE_DIR', 'docs/cache/html/api');
$title = env('SAMI_PROJECT_TITLE', 'API Documentation');
$theme = env('SAMI_THEME', 'default');

$iterator = Finder::create()
  ->files()
  ->name("*.php")
  ->exclude("Tests")
  ->exclude("tests")
  ->exclude("tests-nocov")
  ->exclude("Resources")
  ->exclude("Behat")
  ->exclude("vendor")
  ->in(explode(':', $srcdir));

return new Sami($iterator, array(
  'theme'     => $theme,
  'title'     => $title,
  'build_dir' => $builddir,
  'cache_dir' => $cachedir,
));
