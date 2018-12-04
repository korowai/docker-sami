#!/bin/bash -eu

versions="7.1 7.2";
oses="alpine";

generated_warning() {
cat <<-EOH
#
# NOTE: FILE GENERATED VIA "update.sh"
#
# PLEASE DO NOT EDIT IT DIRECTLY
#
EOH
}

substitute() {
  sed -e "s:%%DOCKER_FROM_TAG%%:${dockerFromTag}:g" \
      -e "s:%%VERSION%%:${projectVersion}:g"
}

projectVersion=`cat VERSION`;

for version in $versions; do
  for os in $oses; do
    targetDir="$version/$os";
    [ -d  "$targetDir" ] || mkdir -p "$targetDir";
    targetFile="$targetDir/Dockerfile";
    dockerFromTag="${version}-${os}";
    ( generated_warning ; cat "Dockerfile.in" ) |  substitute > "$targetDir/Dockerfile";
    [ -d "$targetDir/hooks" ] || mkdir -p "$targetDir/hooks";
    cat "hooks/build.in" | substitute > "$targetDir/hooks/build"
    rm -rf "$targetDir/bin" && cp -r bin "$targetDir/";
    rm -rf "$targetDir/etc" && cp -r etc "$targetDir/";
  done
done
