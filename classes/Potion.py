class Potion:
    def __init__(self, x, y, width, height, doses):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.doses = doses
        self.values = [x, y, width, height, doses]

    def __repr__(self):
        return 'Potion(x={0}, y={1}, width={2}, height={3}, doses={4})'\
            .format(self.x, self.y, self.width, self.height, self.doses)

    def __getitem__(self, key):
        return self.values[key]