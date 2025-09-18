class Printer:
    def __init__(self):
        self.sink = None

    def set_sink(self, sink):
        self.sink = sink

    def print_label(self, variety, grade):
        if self.sink:
            self.sink.print_label(variety, grade)
        else:
            print(f"Variety: {variety}, Grade: {grade}")