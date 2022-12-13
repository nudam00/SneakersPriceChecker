import json


class Size:
    # Converts sizes to the right format
    def __init__(self, size, sku):
        self.size = str(size)
        self.sku = sku

    def stockx(self):
        return self.size

    def restocks(self):
        json_file = open("restocks.json")
        sizes = json.load(json_file)

        for size in sizes['Y']:
            sizes['Y'][size] = sizes['Y'][size].replace("Â˝", '½')

        for size in sizes['W']:
            sizes['W'][size] = sizes['W'][size].replace("Â˝", '½')

        for size in sizes['M']:
            sizes['M'][size] = sizes['M'][size].replace("Â˝", '½')

        for size in sizes['c']:
            sizes['c'][size] = sizes['c'][size].replace("Â˝", '½')

        for size in sizes['New_balance']:
            sizes['New_balance'][size] = sizes['New_balance'][size].replace(
                "Â˝", '½')

        t = 0
        for size in sizes['Adidas']:
            t += 1
            if t == 2:
                sizes['Adidas'][size] = sizes['Adidas'][size].replace(
                    "â…”", '⅔')
            if t == 3:
                sizes['Adidas'][size] = sizes['Adidas'][size].replace(
                    "â…“", '⅓')
                t = 0

        if "-" in self.sku:
            if "Y" in self.size:
                return sizes['Y'][self.size]
            if "W" in self.size:
                return sizes['W'][self.size]
            if "c" in self.size:
                return sizes['c'][self.size]
            return sizes['M'][self.size]

        if "BB" in self.sku or "GSB" in self.sku:
            return sizes['New_balance'][self.size]

        return sizes['Adidas'][self.size]

    def sizes(self):
        return [self.stockx(), self.restocks()]
