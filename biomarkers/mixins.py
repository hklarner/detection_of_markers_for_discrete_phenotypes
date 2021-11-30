

import json
import logging

log = logging.getLogger(__name__)


class ToJsonMixin:
    def to_json(self, fname: str):
        with open(fname, "w") as fp:
            json.dump(obj=self.dict(), fp=fp, sort_keys=True)

        log.info(f"created json file: fname={fname}")
