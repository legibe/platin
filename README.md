# Platin 

Set of utility libs

# Build RPM

    python setup.py bdist_rpm

For more options see the documentation at [Creating RPM Packages](http://docs.python.org/2.0/dist/creating-rpms.html)

# Build RPMs for CentOS SCL 

## Dependencies
    yum install centos-release-SCL
    yum install ruby ruby-devel rubygems
    yum install python-{devel,setuptools} python27-python-{devel,setuptools} python33-python-{devel,setuptools}
    gem install fpm

Short:

    make rpm-scl

Long: 

    ./build.py requirements27.json setup.py

Usage: 

    build.py [-h] [-d DESTINATION] [-v] data packages [packages ...]

For more info check [ds-build-python](https://github.com/datasift/ds-build-python)
