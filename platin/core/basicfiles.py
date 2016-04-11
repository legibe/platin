#--------------------------------------------------------------------------------
# Author: Claude Gibert
#
#--------------------------------------------------------------------------------
import os


def cleanSave(filename, data):
    f = open('%s.tmp' % filename, 'w')
    f.write(data)
    f.close()
    os.rename('%s.tmp' % filename, filename)


def directoryList(path, extension=None):
    result = []
    if os.path.exists(path):
        files = os.listdir(path)
        if extension is None:
            result = files
        else:
            for file in files:
                l = file.split('.')
                if l[-1] == extension:
                    result.append(file)
    return result


def mkdir(dir):
    try:
        os.makedirs(dir)
    except OSError:
        pass


class FileWatcher(object):
    def __init__(self, file):
        self.file = file
        self.latest = os.stat(file).st_mtime

    def __call__(self):
        current = os.stat(self.file).st_mtime
        if current != self.latest:
            self.latest = current
            return True
        return False


class FileBrowser(object):
    def __init__(self, path, extension=None):
        self._path = path
        self._extension = extension

    def __call__(self, visitor):
        files = directoryList(self._path, self._extension)
        for filename in files:
            fullpath = '%s/%s' % (self._path, filename)
            visitor(self, fullpath, filename)

    def deleteFile(self, fullpath):
        os.unlink(fullpath)

    def moveFile(self, fullpath, destination):
        os.rename(fullpath, destination)

def freeSpaceFS(pathname):
    "Get the free space of the filesystem containing pathname"
    stat= os.statvfs(pathname)
    # use f_bfree for superuser, or f_bavail if filesystem
    # has reserved space for superuser
    return stat.f_bfree*stat.f_bsize
