from dataclasses import dataclass, field
from typing import Union, Any

from .checkable import Checkable

@dataclass
class ValCheck(Checkable):
    schema: dict[str, Union[Checkable, Any]] = field(default_factory=dict)

    def check(self, value: dict[str, str]) -> bool:
        for key, expected_value in self.schema.items():
            if key not in value:
                return False

            current_value = value[key]

            is_checkable = isinstance(expected_value, Checkable)

            if is_checkable:
                if not expected_value.check(current_value):
                    return False
            elif current_value != expected_value:
                return False

        return True
