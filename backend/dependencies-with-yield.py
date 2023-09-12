"""
Dependencies with yield

FastAPI supports dependencies that do some extra steps after finishing.

To do this, use `yield` instead of `return`, and write the extra 
steps after.

---

Tip

Make sure to `yield` one single time.

---

Technical Details

Any function that is valid to use with:
    - @contextlib.contextmanager
    - @contextlib.asynccontextmanager

would be valid to use as a FastAPI dependency.

In fact, FastAPI uses those two decorators internally.

-----

A database dependency with `yield`

For example, you could use this to create a database session and 
close it after finishing.

Only the code prior to and including the `yield` statement 
is executed before sending a response:

    async def get_db():
        db = DBSession()
        try:
            yield db
        finally:
            db.close()

The yielded value is what is injected into Path Operations and other 
dependencies.

The code following the `yield` statement is executed after the response 
has been delivered.

---

Tip

You can use async or normal functions.

FastAPI will do the right thing with each, the same as 
with normal dependencies.

-----

A dependency with `yield` and `try`.

If you use a `try` block in a dependency with `yield`, you'll receive 
any exception that was thrown when using the dependency. 

For example, if some code at some point in the middle, in another 
dependency or in a Path Operation, made a database transaction 
"rollback" or create any other error, you will receive the exception 
in your dependency.

So, you can look for that specific exception inside the dependency 
with `except SomeException`.

In the same way, you can use `finally` to make sure the exit steps are 
executed, no matter if there was an exception or not.

    async def get_db():
        db = DBSession()
        try:
            tield db
        finally:
            db.close()

-----

Sub-dependencies with `yield`

You can have sub-dependencies and "trees" of sub-dependencies of any size and shape, and any 
or all of them can use `yield`.

FastAPI will make sure that the "exit code" in each dependency with `yield` is 
run in the correct order.

For example, `dependency_c` can have a dependency on `dependency_b`, and 
`dependency_b` on `dependency_a`:
"""

from fastapi import Depends
from typing_extensions import Annotated

async def dependency_a():
    dep_a = generate_dep_a()
    try:
        yield dep_a
    finally:
        dep_a.close()

async dependency_b(dep_a: Annotated[DepA, Depends(dependency_a)]):
    dep_b = generate_dep_b()
    try:
        yield dep_b
    finally:
        dep_b.close(dep_a)

async def dependency_c(dep_b: Annotated[DepB, Depends(dependency_b)]):
    dep_c = generated_dep_c()
    try:
        yield dep_c
    finally:
        dep_c.close(dep_b)

"""
All of them can use `yield`.

In this case `dependency_c`, to execute its exit code, needs the value 
from `dependency_b` (here named `dep_b`) to still be available.

And, in turn, `dependency_b` needs the value from `dependency_a` (here named `dep_a`)
to be available for its exit code.

The same way, you could have dependencies with `yield` and `return` mixed.

And you could have a single dependency that requires several other dependencies with 
`yield`, etc.

You can have any combinations of dependencies that you want.

FastAPI will make sure everything is run in the correct order.

---

Technical Details

This works thanks to Python's Context Managers.
FastAPI uses them internally to achieve this.

-----

Dependencies with `yield` and `HTTPException`

You saw that you can use dependencies with `yield` 
and have `try` blocks that catch exceptions.

It might be tempting to raise an HTTPException or similar in the exit 
code, after the `yield`. But it won't work.

The exit code in dependencies with `yield` is executed after 
the response is sent, so Exception Handlers will have already 
run. There's nothing catching exceptions thrown by your 
dependencies in the exit code (after the `yield`).

So, if you raise an `HTTPException` after the `yield`, the default (or any 
custom) exception handler that catches `HTTPException`s and returns an 
HTTP 400 response won't be there to catch that exception anymore.

This is what allows anything set in the dependency (e.g., a DB session) 
to, for example, be used by background tasks.

Background tasks are run after the response has been sent. So there's 
no way to raise an `HTTPException` because there's not even a way to 
change the response that is already sent. 

But if a background task creates a DB error, at least you can rollback or cleanly 
close the session in the dependency with `yield`, and maybe log the error 
or report it to a remote tracking system.

If you have some code that you know could raise an exception, do the most 
normal/"Pythonic" thing and add a `try` block in that section of the code.

If you have custom exceptions that you would like to handle before 
returning the response and possibly modifying the response, maybe even 
raising an `HTTPException` create a Custom Exception Handler.

---

Tip

You can still raise exceptions including HTTPException before the `yield`. But not after.

---

Context Managers

What are "Context Managers"?

"Context Managers" are any of those Python objects that you can use 
in a `with` statement.

For example, you can use `with` to read a file:

    with open("./somefile.txt") as f:
        contents = f.read()
        print(contents)

Underneath, the `open("./somefile.txt")` creates an object that is called a 
"Context Manager".

When the `with` block finishes, it makes sure to close the file, even if there 
were exceptions.

When you create a dependency with `yield`, FastAPI will internally convert 
it to a context manager, and combine it with some other related tools.

-----

Using context managers in dependencies with `yield`

---

Warning

This is, more or less, an "advanced" idea.

If you are just starting with FastAPI you might want to skip it for now.

---

In Python, you can create Context Managers by creating a 
class with two methods: __enter__() and __exit__().

You can also use them inside of FastAPI dependencies with `yield` 
by using `with` or `async with` statements inside of the dependency 
function:
"""


class MySuperContextManager:
    def __init__(self):
        self.db = DBSession()

    def __enter__(self):
        return self.db

    def __exit__(self, exc_type, exc_value, traceback):
        self.db.close()


async def get_db():
    with MySuperContextManager() as db:
        yield db

"""
Tip

Another way to create a context manager is with:
    - @contextlib.contextmanager
    - @contextlib.asynccontextmanager

using them to decorate a function with a single `yield`.

That's what FastAPI uses internally for dependencies with `yield`.

But you don't have to use the decorators for FastAPI dependencies 
(and you shouldn't).

FastAPI will do it for you internally.
"""
