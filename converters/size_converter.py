import json


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

    def restocks(self):
        json_file = open("converters/restocks.json")
        sizes = json.load(json_file)

        for size in sizes['Y']:
            sizes['Y'][size] = sizes['Y'][size].replace("Â˝", '½')

        for size in sizes['W']:
            sizes['W'][size] = sizes['W'][size].replace("Â˝", '½')

        for size in sizes['M']:
            sizes['M'][size] = sizes['M'][size].replace("Â˝", '½')

        for size in sizes['C']:
            sizes['C'][size] = sizes['C'][size].replace("Â˝", '½')

        for size in sizes['New_balance']:
            sizes['New_balance'][size] = sizes['New_balance'][size].replace(
                "Â˝", '½')

        t = 0
        for size in sizes['Adidas']:
            t += 1
            if t == 2:
                sizes['Adidas'][size] = sizes['Adidas'][size].replace(
                    "â…”", '⅔')
            elif t == 3:
                sizes['Adidas'][size] = sizes['Adidas'][size].replace(
                    "â…“", '⅓')
                t = 0

        if "-" in self.sku:
            if "Y" in self.size:
                return sizes['Y'][self.size]
            elif "W" in self.size:
                if len(self.sku) == 11:
                    return sizes['UGG'][self.size]
                else:
                    return sizes['W'][self.size]
            elif "C" in self.size:
                return sizes['C'][self.size]
            else:
                return sizes['M'][self.size]

        if "BB" in self.sku or "GSB" in self.sku:
            return sizes['New_balance'][self.size]

        return sizes['Adidas'][self.size]

    def klekt(self):
        if 'W' in self.size:
            return 'US'+self.size.replace('W', '')
        elif 'Y' in self.size:
            return self.size
        elif 'C' in self.size:
            return self.size
        elif 'GSB' in self.sku:
            return self.size.replace('Y', '')
        else:
            return 'US'+self.size

    def wethenew(self):
        json_file = open("converters/wethenew.json")
        sizes = json.load(json_file)

        if "-" in self.sku:
            if "Y" in self.size:
                return sizes['Y'][self.size]
            elif "W" in self.size:
                if len(self.sku) == 11:
                    return sizes['UGG'][self.size]
                else:
                    return sizes['W'][self.size]
            elif "C" in self.size:
                return sizes['C'][self.size]
            else:
                return sizes['M'][self.size]

        if "BB" in self.sku or "GSB" in self.sku:
            return sizes['New_balance'][self.size]

        return sizes['Adidas'][self.size]

    def sizes(self):
        return [self.stockx(), self.alias(), self.restocks(), self.klekt(), self.wethenew()]
