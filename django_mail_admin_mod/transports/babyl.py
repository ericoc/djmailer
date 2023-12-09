from mailbox import Babyl

from generic import GenericFileMailbox


class BabylTransport(GenericFileMailbox):
    _variant = Babyl
