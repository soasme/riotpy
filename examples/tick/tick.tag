<tick>
    <button onpress="{ press }">{ count }</button>

    def init(self, opts):
        self.count = 0

    def press(self, event):
        self.count += 1
<tick>
