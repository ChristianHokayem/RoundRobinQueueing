class TokenBucket:
    def __init__(self, tokens):
        self.capacity = int(tokens)
        self.available_tokens = int(tokens)

    def consume(self, number_of_tokens):
        if number_of_tokens <= self.available_tokens:
            self.available_tokens -= number_of_tokens
            return True
        return False

    def return_resource(self, number_of_tokens):
        self.available_tokens += number_of_tokens
