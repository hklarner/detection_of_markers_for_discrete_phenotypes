

import logging
from typing import List, Optional

from pydantic import BaseModel

from biomarkers.mixins import ToJsonMixin

log = logging.getLogger(__name__)


class Markers(BaseModel, ToJsonMixin):
    indices: List[List[int]]
    component_names: Optional[List[str]]

    def __len__(self) -> int:
        return len(self.indices)

    def unique_indices(self) -> List[int]:
        return sorted(set(x for markers in self.indices for x in markers))

    def to_csv(self, fname: str, enable_header: bool = False):
        if enable_header:
            if self.component_names:
                lines = [[self.component_names[x] for x in self.unique_indices()]]
                lines += [[self.component_names[x] for x in markers] for markers in self.indices]
            else:
                lines = [str(x) for x in self.unique_indices()]
                lines += [[str(x) for x in markers] for markers in self.indices]
        else:
            if self.component_names:
                lines = [[self.component_names[x] for x in markers] for markers in self.indices]
            else:
                lines = [[str(x) for x in markers] for markers in self.indices]

        with open(fname, "w") as fp:
            fp.write('\n'.join(', '.join(line) for line in lines))

        log.info(f"created csv file: {fname=}")
