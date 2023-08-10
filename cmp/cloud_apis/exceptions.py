# -*- coding: utf-8 -*-
from cmp.exceptions import BlueException


class RewriteException(BlueException):
    """
    an exception class deals with unimplemented methods.
    """

    def __init__(self, err=u"方法需要重写"):
        super(RewriteException, self).__init__(err)

    def __str__(self):
        return self.message.encode("utf8")
