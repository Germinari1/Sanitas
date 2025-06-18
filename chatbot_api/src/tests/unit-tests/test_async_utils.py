import pytest
import asyncio
from utils.async_utils import async_retry

# helper coroutine that fails twice then returns "OK"
class Counter:
    def __init__(self): self.count=0

counter = Counter()

@async_retry(max_retries=3, delay=0)
async def sometimes_fails(x):
    counter.count += 1
    if counter.count < 3:
        raise ValueError("fail")
    return f"got {x}"

@pytest.mark.asyncio
async def test_retry_success():
    result = await sometimes_fails("test")
    assert result == "got test"
    assert counter.count == 3

@async_retry(max_retries=2, delay=0)
async def always_fails():
    raise RuntimeError("nope")

@pytest.mark.asyncio
async def test_retry_exhausted():
    with pytest.raises(RuntimeError):
        await always_fails()
