class Response:
    def __init__(self, result: dict = {}, failed: list = [], start_time: float = 0.0, end_time: float = 0.0):
        self.result: dict = result
        self.failed: list = failed
        self.start_time: float = start_time
        self.end_time: float = end_time

    @property
    def run_time(self):
        return self.end_time - self.start_time

    def __repr__(self):
        return f"Response(result={self.result}, failed={self.failed}, run_time={self.run_time:.3f})"
