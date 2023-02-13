class Size:
    # Converts sizes to the right format
    def __init__(self, size, sku):
        self.size = str(size)
        self.sku = sku

    def stockx(self):
        return self.size

    def alias(self):
        if 'W' in self.size:
            return self.size.replace('W', '')
        elif 'Y' in self.size:
            return self.size.replace('Y', '')
        elif 'C' in self.size:
            return self.size.replace('C', '')
        else:
            return self.size
