from mailbox import MH

from .generic import GenericFileMailbox


class MHTransport(GenericFileMailbox):
    _variant = MH
