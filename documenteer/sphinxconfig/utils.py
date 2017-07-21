"""Utilities for sphinx configuration."""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import re

import os
import git


TICKET_BRANCH_PATTERN = re.compile('^tickets/([A-Z]+-[0-9]+)$')

# does it start with vN and look like a version tag?
TAG_PATTERN = re.compile('^v\d')


def read_git_branch():
    """Obtain the current branch name from the Git repository. If on Travis CI,
    use the ``TRAVIS_BRANCH`` environment variable.
    """
    if os.getenv('TRAVIS'):
        return os.getenv('TRAVIS_BRANCH')
    else:
        try:
            repo = git.repo.base.Repo(search_parent_directories=True)
            return repo.active_branch.name
        except:
            return ''


def read_git_commit_timestamp(repo_path=None):
    """Obtain the timestamp from the current head commit of a Git repository.

    Parameters
    ----------
    repo_path : `str`, optional
        Path to the Git repository. Leave as `None` to use the current working
        directory.

    Returns
    -------
    commit_timestamp : `datetime.datetime`
        The datetime of the head commit.
    """
    repo = git.repo.base.Repo(path=repo_path, search_parent_directories=True)
    head_commit = repo.head.commit
    return head_commit.committed_datetime


def read_git_commit_timestamp_for_file(filepath, repo_path=None):
    """Obtain the timestamp for the most recent commit to a given file in a
    Git repository.

    Parameters
    ----------
    filepath : `str`
        Repository-relative path for a file.
    repo_path : `str`, optional
        Path to the Git repository. Leave as `None` to use the current working
        directory.

    Returns
    -------
    commit_timestamp : `datetime.datetime`
        The datetime of a the most recent commit to the given file.

    Raises
    ------
    IOError
        Raised if the ``filepath`` does not exist in the Git repository.
    """
    repo = git.repo.base.Repo(path=repo_path, search_parent_directories=True)
    head_commit = repo.head.commit

    # most recent commit datetime of the given file
    for commit in head_commit.iter_parents(filepath):
        return commit.committed_datetime

    # Only get here if git could not find the file path in the history
    raise IOError('File {} not found'.format(filepath))


def form_ltd_edition_name(git_ref_name=None):
    """Form the LSST the Docs edition name for this branch, using the same
    logic as LTD Keeper does for transforming branch names into edition names.

    Parameters
    ----------
    git_ref_name : `str`
       Name of the git branch (or git ref, in general, like a tag) that.

    Notes
    -----
    The LTD Keeper (github.com/lsst-sqre/ltd-keeper) logic is being replicated
    here because Keeper is server side code and this is client-side and it's
    not yet clear this warrants being refactored into a common dependency.

    See ``keeper.utils.auto_slugify_edition``.
    """
    if git_ref_name is None:
        name = read_git_branch()
    else:
        name = git_ref_name

    # First, try to use the JIRA ticket number
    m = TICKET_BRANCH_PATTERN.match(name)
    if m is not None:
        return m.group(1)

    # Or use a tagged version
    m = TAG_PATTERN.match(name)
    if m is not None:
        return name

    if name == 'master':
        # using this terminology for LTD Dasher
        name = 'Current'

    # Otherwise, reproduce the LTD slug
    name = name.replace('/', '-')
    name = name.replace('_', '-')
    name = name.replace('.', '-')
    return name
