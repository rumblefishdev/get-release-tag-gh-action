#!/usr/bin/env python3

from github import Github, Auth
import os

# Settings
wanted_release = os.getenv('type')
repository = os.getenv('repository')
token = os.getenv('token', None)
package = os.getenv('package')

# Init class
auth = Auth.Token(token)
G = Github(auth=auth)
repo = G.get_repo(repository)
releases = repo.get_releases()

# Output formatting function
def output(release):
    print('::set-output name=release::{}'.format(release.tag_name))
    print('::set-output name=release_id::{}'.format(release.id))
    assets = release.get_assets()
    dl_url = assets[0].browser_download_url if assets.totalCount > 0 else '""'
    print('::set-output name=browser_download_url::{}'.format(dl_url))


# Releases parsing
found = False
for release in releases:
    print(f'Checking release: {release.tag_name}')  # Debugging log
    if package in release.tag_name:
        if wanted_release == 'stable' and not release.prerelease and not release.draft:
            output(release)
            found = True
            break
        elif wanted_release == 'prerelease' and release.prerelease:
            output(release)
            found = True
            break
        elif wanted_release == 'latest':
            output(release)
            found = True
            break
        elif wanted_release == 'nodraft' and not release.draft:
            output(release)
            found = True
            break

if not found:
    print('Can\'t get release')

