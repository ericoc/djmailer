from mailbox import MMDF

from .generic import GenericFileMailbox


class MMDFTransport(GenericFileMailbox):
    _variant = MMDF
