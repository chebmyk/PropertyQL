#todo enum
class Topic:
    LOG="LOG"
    EXEC="EXEC"


class Message:
    topic: str
    body: {}

    def __init__(self, topic, body):
        self.topic = topic
        self.body = body


class LogMessage:
    def info(self, message) -> Message:
        msg = Message(Topic.LOG, {'logLevel': "INFO",'message': message})
        return msg

    def warning(self, message) -> Message:
        msg = Message(Topic.LOG, {'logLevel': "WARNING",'message': message})
        return msg

    def error(self, message) -> Message:
        msg = Message(Topic.LOG, {'logLevel': "ERROR",'message': message})
        return msg


logMsg = LogMessage()


class Observer:
    def update(self, message: Message):
        pass


class ConsoleLogObserver(Observer):
    def update(self, message: Message):
        if message.topic == Topic.LOG:
            print(f"{message.body['logLevel']}: {message.body['message']}")