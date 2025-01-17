from typing import List

from g2p_payments_bridge_core.services import IdTranslateService
from openg2p_common_g2pconnect_id_mapper.models.common import MapperValue
from openg2p_common_g2pconnect_id_mapper.service.resolve import (
    MapperResolveService as IDMapperResolveService,
)
from openg2p_fastapi_common.errors import BaseAppException


class G2PConnectIdTranslateService(IdTranslateService):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._id_mapper_service = IDMapperResolveService.get_component()

    @property
    def id_mapper_service(self):
        if not self._id_mapper_service:
            self._id_mapper_service = IDMapperResolveService.get_component()
        return self._id_mapper_service

    async def translate(self, ids: List[str]) -> List[str]:
        res = await self.id_mapper_service.resolve_request_sync(
            [MapperValue(id=id) for id in ids]
        )
        if not res:
            raise BaseAppException(
                "GPB-IMS-300",
                "ID Mapper Resolve Id: No response received",
            )
        if not res.refs:
            raise BaseAppException(
                "G2P-IMS-301",
                "ID Mapper Resolve Id: Invalid Txn without any requests received",
            )
        return [res.refs[key].fa for key in res.refs]
