class MessageService:
    events = []

    def publish_event(self, event):
      self.events.append(event)