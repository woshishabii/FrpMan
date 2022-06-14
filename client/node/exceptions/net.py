from . import base


class FrpManNoConnection(base.FrpManNodeClientExceptionBase):
    def __init__(self, e):
        super().__init__(
            title='No Connection',
            description='No Connection Error',
            solution='Check your network',
            e=e)
