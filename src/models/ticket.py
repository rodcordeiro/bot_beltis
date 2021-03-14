
class Ticket:
    def __init__(self, ticket):
        self.ticket_id = ticket['id']
        self.title = ticket['name']
        self.description = ticket['content']
