#!/bin/sh
#
# Install the hooks in this directory as hooks for the current repository.
# Your existing hooks will be moved to `hooks.bak`.

repo_dir=`git rev-parse --show-toplevel`
hook_dir=`git rev-parse --git-path hooks`
mv "$hook_dir" "$hook_dir/../hooks.bak"
ln -s "$repo_dir/git_hooks/" "$hook_dir"
