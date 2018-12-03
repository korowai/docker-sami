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

for version in $versions; do
  for os in $oses; do
    targetDir="$version/$os";
    [ -d  "$targetDir" ] || mkdir -p "$targetDir";
    targetFile="$targetDir/Dockerfile";
    dockerFromTag="${version}-${os}";
    ( generated_warning ; cat "Dockerfile.in") | sed \
      -e "s:%%DOCKER_FROM_TAG%%:${dockerFromTag}:g" \
    > "${targetFile}";
    rm -rf "$targetDir/bin" && cp -r bin "$targetDir/";
    rm -rf "$targetDir/etc" && cp -r etc "$targetDir/";
  done
done
