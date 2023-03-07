from pydantic import (
    BaseModel,
    StrictBytes,
    StrictBool,
    StrictInt,
    ValidationError,
    confloat,
)

class StrictIntModel(BaseModel):
    strict_int: StrictInt

try:
    StrictIntModel(strict_int=3.1415)
except ValidationError as e:
    print(e)

