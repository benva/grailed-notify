import sys, os
sys.path.append(os.path.join(sys.path[0],'src'))

from grailednotify import GrailedNotify

# Proper, full names surrounded by quotes and separated by a comma
# e.g. ["Rick Owens", "Raf Simons", "Julius"]
designers = ["Rick Owens",
            "Raf Simons",
            "Julius"]

# Must be a proper category of Grailed surrounded by quotes and separated by a comma
# Case does not matter
# e.g. ["Tops", "Bottoms", "Outerwear", "Footwear", "Tailoring", "Accessories"]
categories =    ["Bottoms",
                "Footwear"]

# Place sizes for respective category in quotes, separated by commas
# e.g. ["Bottoms & Pants", "29", "30", "31"]
sizes =     [["Tops & Outerwear"],
            ["Bottoms & Pants"],
            ["Footwear", "10", "10.5", "11"],
            ["Tailoring"],
            ["Accessories"]]

# First value is the minimum price (set to 0 for no minimum), second is maximum price
# prices = [min, max]
# e.g. [100, 300]
prices = [100, 300]

bot = GrailedNotify(designers, categories, sizes, prices)
