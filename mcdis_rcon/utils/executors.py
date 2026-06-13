import asyncio
import threading
from collections.abc import Callable


async def execute_and_wait(
    function: Callable[..., object],
    *,
    args: tuple[object, ...] = (),
    kwargs: dict[str, object] | None = None,
) -> None:
    task = threading.Thread(target=function, args=args, kwargs=kwargs or {})
    task.start()

    while task.is_alive():
        await asyncio.sleep(1)
