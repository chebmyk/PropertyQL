from mql.model.messaging.messages import Message, Observer


class MessageService:
    subscribers = set()

    def publish(self, message: Message):
        for subscriber in self.subscribers:
            subscriber.update(message)

    def subscribe(self, observer: Observer):
        self.subscribers.add(observer)

    def unsubscribe(self, observer: Observer):
        self.subscribers.remove(observer)