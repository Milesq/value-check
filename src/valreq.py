import operator
from dataclasses import dataclass
from typing import Callable, Optional, Union, Any

from .checkable import Checkable


class SkipOp:
    def __eq__(self, obj) -> bool:
        return isinstance(obj, SkipOp)


skip_op = SkipOp()


@dataclass
class ValReq(Checkable):
    # pylint: disable=invalid-name
    ne: Optional[int] = skip_op
    eq: Optional[int] = skip_op

    lt: Optional[int] = skip_op
    gt: Optional[int] = skip_op

    le: Optional[int] = skip_op
    ge: Optional[int] = skip_op

    cast: Union[type, Callable] = lambda x: x

    def __repr__(self) -> str:
        name = type(self).__name__

        attrs = self.__dict__.items()
        args = [f'{k}={v}' for k,
                v in attrs if v is not skip_op and k != 'cast']

        return f"{name}({', '.join(args)})"

    def check(self, value: Any) -> bool:
        operators = ['ne', 'eq', 'lt', 'gt', 'le', 'ge']
        val = self.cast(value)

        for op_to_check in operators:
            constraint = getattr(self, op_to_check)
            if constraint == skip_op:
                continue

            current_op = getattr(operator, op_to_check)

            if not current_op(val, constraint):
                return False

        return True
