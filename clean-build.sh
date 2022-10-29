#!/bin/sh
/usr/local/bin/sam build
cd .aws-sam/build/PinfluencerFunction || exit
rm -fr clean-build.sh tests events env.json README.md samconfig.toml template.yaml requirements.txt


