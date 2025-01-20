"""
Redis
"""

import rq
from redis import Redis

from ..settings import REDIS_URL, TASK_QUEUE

redis = Redis.from_url(REDIS_URL)
task_queue = rq.Queue(TASK_QUEUE, connection=redis, default_timeout=1920)
