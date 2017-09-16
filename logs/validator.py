import abc
import os

class AbstractValidator(object):
    __metaclass__  = abc.ABCMeta
    @abc.abstractmethod
    def validate(self, to_be_validated):
        """validate the input"""

class InputFileValidator(AbstractValidator):
    def __init__(self, to_be_validated):
        self.filename = to_be_validated
    def validate(self):
        if  not self._file_exist():
            raise NotSuchFile()
        elif not self._file_empty():
            raise FileIsEmpty()
        else:
            return True
    def _file_exist(self):
        return os.path.isfile(self.filename)
    def _file_empty(self):
        return os.stat(self.filename).st_size

class NotSuchFile(Exception):
    pass

class FileIsEmpty(Exception):
    pass
