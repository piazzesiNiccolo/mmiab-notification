import logging
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import wait

from mib import create_app
from mib.events.callbacks import add_notify
from mib.events.channels import SUBSCRIBE_CHANNEL_ADD_MESSAGE_NOTIFICATIONS
from mib.events.redis_setup import get_redis


class EventSubscribers:  # pragma: no cover
    @classmethod
    def recipient_deleter(cls, app):
        redis_c = get_redis(app)
        p = redis_c.pubsub()
        p.subscribe(SUBSCRIBE_CHANNEL_ADD_MESSAGE_NOTIFICATIONS)
        logging.debug(f"subscribed on channel {SUBSCRIBE_CHANNEL_ADD_MESSAGE_NOTIFICATIONS}")
        for message in p.listen():
            with app.app_context():
                add_notify(message)


event_subscribers = [{"subscriber": EventSubscribers.recipient_deleter}]


def init_subscribers():  # pragma: no cover
    app = create_app()
    logging.info("setting up subscribers...")
    with ThreadPoolExecutor(max_workers=8) as ex:
        futures = [ex.submit(sub["subscriber"], app) for sub in event_subscribers]
    wait(futures)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(init_subscribers())
