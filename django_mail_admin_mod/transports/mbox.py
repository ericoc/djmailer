from mailbox import mbox

from .generic import GenericFileMailbox


class MboxTransport(GenericFileMailbox):
    _variant = mbox
