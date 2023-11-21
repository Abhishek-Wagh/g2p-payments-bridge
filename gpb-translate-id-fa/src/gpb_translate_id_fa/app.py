from openg2p_fastapi_common.app import Initializer

from .services import G2PConnectIdTranslateService


class Initializer(Initializer):
    def initialize(self, **kwargs):
        # Initialize all Services, Controllers, any utils here.
        G2PConnectIdTranslateService()
