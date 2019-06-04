#!/usr/bin/env bash
if [ "$TRAVIS_BRANCH" != "dev" ]; then
    exit 0;
fi

export GIT_COMMITTER_EMAIL="giusepper11@gmail.com"
export GIT_COMMITTER_NAME="Giuseppe Rosa"

git pull
echo "antes"
git branch -lall
git fetch --depth=1 git@github.com:prefeiturasp/SME-Indice_IDEP-API.git refs/heads/homolog:refs/remotes/origin/homolog
echo "depois"
git branch -lall
git reset --hard HEAD
git checkout remotes/origin/homolog || exit
git merge "$TRAVIS_COMMIT" || exit
git push origin HEAD:homolog