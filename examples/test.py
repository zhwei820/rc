# -*- coding: utf-8 -*-
if __name__ == '__main__':
    import sys
    import os
    _LOCAL_PATH_ = os.path.abspath(os.path.dirname(__file__))
    modules_folder = os.path.abspath(_LOCAL_PATH_ + '/..')
    if modules_folder not in sys.path:
        sys.path.append(modules_folder)

import asyncio
from rc import Cache

cache = Cache()

@cache.as_cache()
async def as_test():
    return 'test'

loop = asyncio.get_event_loop()
loop.run_until_complete(as_test())
