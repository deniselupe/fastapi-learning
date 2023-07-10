"""
Extra Data Types

Up to now, you have been using common data types, like:
    - int
    - float
    - str
    - bool

But you can also use more complex data types.

And you will still have the same features as seen up to now:
    - Great editor support.
    - Data conversion from incoming requests.
    - Data conversion for response data.
    - Data validation.
    - Automatic annotation and documentation.


Other Data Types

Here are some of the additional data types you can use:
- UUID:
    - A standard "Universally Unique Identifier", common as an ID in 
      many databases and systems.
    - In requests and responses will be represented as a `str`.
- datetime.datetime:
    - A Python `datetime.datetime`.
    - In requests and responses will be represented as a `str` in ISO 8601
      format, like: `2008-09-15T15:53:00+05:00`.
- datetime.date:
    - Python `datetime.date`.
    - In requests and responses will be represented as a `str` in ISO 8601 
      format, like: `2008-09-15`.
- datetime.time:
    - A Python `datetime.time`.
    - In requests and responses will be represented as a `str` in ISO 8601 
      format, like: `14:23:55.003`.
- datetime.timedelta:
    - A Python `datetime.timedelta`.
    - In requets and responses will be represented as a `float` of total seconds.
    - Pydantic also allows representing it as a "ISO 8601 time diff encoding".
- frozenset:
    - In requests and respones, treated the same as a `set`:
        - In requests, a list will be read, elimintating duplicates and converting 
          it to a `set`.
        - In responses, the `set` will be converted to a `list`.
        - The generated schema will specify that the `set` values are unique (using 
          JSON Schema's `uniqueItems`).
- bytes:
    - Standard Python `bytes`.
    - In requests and responses will be treated as `str`.
    - The generated schema will specify that it's a `str` with `binary` "format".
- Decimal
    - Standard Pytho `Decimal`.
    - In requests and respones, handled the same as a `float`.

You can check all the valid Pydantic data types here:
https://docs.pydantic.dev/latest/usage/types/
"""

"""
Example

Here's an example Path Operation with parameters using some of the 
above types.
"""

from fastapi import Body, FastAPI
from datetime import datetime, time, timedelta
from uuid import UUID
from typing import Union
from typing_extensions import Annotated

app = FastAPI()

@app.put("/v1/items/{item_id}")
async def read_items(
    item_id: UUID,
    start_datetime: Annotated[Union[datetime, None], Body()] = None,
    end_datetime: Annotated[Union[datetime, None], Body()] = None,
    repeat_at: Annotated[Union[time, None], Body()] = None,
    process_after: Annotated[Union[timedelta, None], Body()] = None
):
    # Note that the parameters inside the function have their natural data type, and you can
    # for example, perform normal data manipulations, like:
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "repeat_at": repeat_at,
        "process_after": process_after,
        "start_process": start_process,
        "duration": duration
    }
