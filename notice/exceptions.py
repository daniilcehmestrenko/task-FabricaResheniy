class StatusResponseException(Exception):
    def __str__(self) -> str:
        return 'Response status != 200'


class MailinglistTimeOutException(Exception):
    def __str__(self) -> str:
        return 'Posting time is over'


class CircuitBreakerException(Exception):
    def __str__(self) -> str:
        return 'Circuit open, service not responding'