#!/usr/bin/env bash
if [ "$TRAVIS_BRANCH" != "dev" ]; then
    exit 0;
fi

export GIT_COMMITTER_EMAIL="giusepper11@gmail.com"
export GIT_COMMITTER_NAME="Giuseppe Rosa"

git fetch --depth=1 git@github.com:prefeiturasp/SME-Indice_IDEP-API.git refs/heads/other-branch:refs/remotes/origin/other-branch
git checkout homolog || exit
git merge "$TRAVIS_COMMIT" || exit
git push