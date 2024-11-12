import st7789


class train:
    def __init__(self, train_class, train_time, train_destination, train_length):
        self.train_class = train_class
        self.train_time = train_time
        self.train_destination = train_destination
        self.train_length = train_length

    def convert_class_to_led(self):
        if self.train_class == "普通":
            return "000", [st7789.WHITE, st7789.BLACK]
        elif self.train_class == "快速":
            return "123", [st7789.RED, st7789.WHITE]
        elif self.train_class == "各駅停車":
            return "VWX", [st7789.BLACK, st7789.YELLOW]
        elif self.train_class == "中央特快":
            return "\]^", [st7789.WHITE, st7789.BLUE]
        elif self.train_class == "回送":
            return "bcd", [st7789.WHITE, st7789.BLACK]
        else:
            return "000", [st7789.WHITE, st7789.BLACK]

    def convert_class_to_led_eng(self):
        if self.train_class == "普通":
            return "000", [st7789.WHITE, st7789.BLACK]
        elif self.train_class == "快速":
            return "456", [st7789.RED, st7789.WHITE]
        elif self.train_class == "各駅停車":
            return "YZ[", [st7789.BLACK, st7789.YELLOW]
        elif self.train_class == "中央特快":
            return "_`a", [st7789.WHITE, st7789.BLUE]
        elif self.train_class == "回送":
            return "bcd", [st7789.WHITE, st7789.BLACK]
        else:
            return "000", [st7789.WHITE, st7789.BLACK]

    def convert_destination_to_led(self):
        if self.train_destination == "東京":
            return "708", [st7789.WHITE, st7789.BLACK]
        elif self.train_destination == "新宿":
            return "E0F", [st7789.WHITE, st7789.BLACK]
        elif self.train_destination == "三鷹":
            return "@0A", [st7789.WHITE, st7789.BLACK]
        elif self.train_destination == "JR":
            return "hi0", [st7789.GREEN, st7789.BLACK]
        else:
            return "000", [st7789.WHITE, st7789.BLACK]

    def convert_destination_to_led_eng(self):
        if self.train_destination == "東京":
            return "9:;", [st7789.WHITE, st7789.BLACK]
        elif self.train_destination == "新宿":
            return "GHI", [st7789.WHITE, st7789.BLACK]
        elif self.train_destination == "三鷹":
            return "BCD", [st7789.WHITE, st7789.BLACK]
        elif self.train_destination == "JR":
            return "hi0", [st7789.GREEN, st7789.BLACK]
        else:
            return "000", [st7789.WHITE, st7789.BLACK]

    def convert_length_to_led(self):
        if self.train_length == 10:
            return "<>", [st7789.WHITE, st7789.BLACK]
        elif self.train_length == 12:
            return "R>", [st7789.GREEN, st7789.BLACK]
        else:
            return "00", [st7789.WHITE, st7789.BLACK]

    def convert_length_to_led_eng(self):
        if self.train_length == 10:
            return "=?", [st7789.WHITE, st7789.BLACK]
        elif self.train_length == 12:
            return "R?", [st7789.GREEN, st7789.BLACK]
        else:
            return "00", [st7789.WHITE, st7789.BLACK]
