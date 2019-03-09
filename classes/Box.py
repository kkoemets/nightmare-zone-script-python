class Box:
    def __init__(self, box):
        self.box = box

    def x(self):
        return self.box[0]

    def y(self):
        return self.box[1]

    def width(self):
        return self.box[2]

    def height(self):
        return self.box[3]
