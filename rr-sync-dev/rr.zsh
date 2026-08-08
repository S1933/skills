# shellcheck shell=bash disable=SC1091,SC2296,SC2298
# Compatibility shim for installations that sourced the pre-private path.
source "${${(%):-%N}:A:h}/../private-skills/rr-sync-dev/rr.zsh"
