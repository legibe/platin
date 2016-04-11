#!/usr/bin/env python

from __future__ import print_function, unicode_literals

import argparse
import json
import os.path
import subprocess


def default(*values):
    for value in values:
        if value is not None:
            return value
    raise Exception("All values were None")


class Package(object):
    def __init__(self, name, version, release=1, epoch=0,
                 options=None, depends=None):
        self.name = name
        self.epoch = epoch
        self.version = version
        self.release = release

        self.options = default(options, dict())
        self.depends = default(depends, list())

    def _build_command(self, python, prefix, verbose):
        return (
            'fpm -s python -t rpm {verbose} '
            '--python-bin {python} --python-package-name-prefix {prefix} '
            '--epoch {epoch} --version {version} --iteration {release} '
            '{options}{module}'
        ).format(
            module=self.name, epoch=self.epoch, version=self.version,
            release=self.release, python=python, prefix=prefix,
            verbose=('--verbose ' if verbose >= 2 else ''),
            options=(' '.join(self.options) + ' '))

    def _build_environment(self, python):
        return {
            'python2.6': ['bash', '-c'],
            'python2.7': ['scl', 'enable', 'python27'],
            'python3.3': ['scl', 'enable', 'python33']
        }[python]

    def build(self, python='python2.6', prefix='python',
              environment=['bash', '-c'], destination='dist', verbose=False):
        # The command is made of an environment command that is then passed the
        # command used to run FPM, allowing this to be run inside the CentOS
        # SCL sandboxes
        command = environment + [self._build_command(python, prefix, verbose)]

        if verbose >= 1:
            print('$', command[-1])

        # Build the package
        if not os.path.exists(destination):
            os.makedirs(destination)
        process = subprocess.Popen(command)
        process.wait()
        subprocess.call('mv *.rpm %s' % destination, shell=True)



class PackageBuilder(object):
    def __init__(self, settings, packages):
        self.settings = dict(settings)
        self.packages = dict((k, Package(k, **v)) for k, v in packages.items())

    def _select_packages(self, package_list, names):
        for name in names:
            if name not in package_list:
                package_list.append(self.packages[name].name)
            self._select_packages(package_list, self.packages[name].depends)
        return package_list

    def select_packages(self, names):
        return [self.packages[n] for n in self._select_packages(list(), names)]

    def build_packages(self, names, destination, verbose):
        for package in self.select_packages(names):
            package.build(
                destination=destination, verbose=verbose, **self.settings)


parser = argparse.ArgumentParser()
parser.add_argument(
    '-d', '--destination', default='dist/',
    help="the directory to place packages in")
parser.add_argument(
    '-v', '--verbose', action='count',
    help="output addtional information")
parser.add_argument('data', help="A file containing package information")
parser.add_argument('packages', nargs='+', help="The main packages to build")


def main():
    args = parser.parse_args()

    with open(args.data, 'r') as file:
        builder = PackageBuilder(**json.load(file))

    builder.build_packages(args.packages, args.destination, args.verbose)

if __name__ == '__main__':
    main()
