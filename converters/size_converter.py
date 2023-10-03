import json


class Size:
    # Converts sizes to the right format
    def __init__(self, size, sku):
        self.size = str(size)
        self.sku = sku

    def stockx(self):
        return self.size

    def alias(self):
        if "W" in self.size:
            return self.size.replace("W", "")
        elif "Y" in self.size:
            return self.size.replace("Y", "")
        elif "C" in self.size:
            return self.size.replace("C", "")
        else:
            return self.size

    def hypeboost(self, name):
        json_file = open("converters/hypeboost.json")
        sizes = json.load(json_file)

        for size in sizes["Nike"]:
            sizes["Nike"][size] = sizes["Nike"][size].replace("Â˝", "½")

        for size in sizes["New_balance"]:
            sizes["New_balance"][size] = sizes["New_balance"][size].replace("Â˝", "½")

        t = 0
        for size in sizes["Adidas"]:
            t += 1
            if t == 2:
                sizes["Adidas"][size] = sizes["Adidas"][size].replace("â…”", "⅔")
            elif t == 3:
                sizes["Adidas"][size] = sizes["Adidas"][size].replace("â…“", "⅓")
                t = 0

        if "new balance" in name:
            return sizes["New_balance"][self.size]
        elif "adidas" in name:
            return sizes["Adidas"][self.size]
        elif "nike" in name or "jordan" in name:
            return sizes["Nike"][self.size]
        elif "ugg" in name:
            return sizes["UGG"][self.size]

    def klekt(self):
        if "W" in self.size:
            return "US" + self.size.replace("W", "")
        elif "GSB" in self.sku:
            return self.size.replace("Y", "")
        elif "Y" in self.size:
            return self.size
        elif "C" in self.size:
            return self.size
        else:
            return "US" + self.size

    def wethenew(self, name):
        json_file = open("converters/wethenew.json")
        sizes = json.load(json_file)

        if "new balance" in name:
            return sizes["New_balance"][self.size]
        elif "adidas" in name:
            return sizes["Adidas"][self.size]
        elif "nike" in name or "jordan" in name:
            return sizes["Nike"][self.size]
        elif "ugg" in name:
            return sizes["UGG"][self.size]

    def sneakit(self, name):
        json_file = open("converters/sneakit.json")
        sizes = json.load(json_file)

        t = 0
        for size in sizes["Adidas"]:
            t += 1
            if t == 2:
                sizes["Adidas"][size] = sizes["Adidas"][size].replace("â…”", "⅔")
            elif t == 3:
                sizes["Adidas"][size] = sizes["Adidas"][size].replace("â…“", "⅓")
                t = 0

        if "new balance" in name:
            return sizes["New_balance"][self.size]
        elif "adidas" in name:
            return sizes["Adidas"][self.size]
        elif "nike" in name or "jordan" in name:
            return sizes["Nike"][self.size]
        elif "ugg" in name:
            return sizes["UGG"][self.size]
