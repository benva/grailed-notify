import sys, os
sys.path.append(os.path.join(sys.path[0],'src'))

from grailednotify import GrailedNotify

# Proper, full names surrounded by quotes and separated by a comma
# Must be a designer on Grailed
# e.g. ["Rick Owens", "Raf Simons"]
designers = ["Rick Owens",
            "Julius"]

# Must be a proper category of Grailed surrounded by quotes and separated by a comma
# Must be a filter on Grailed, case does not matter
# e.g. ["Tops", "Bottoms", "Outerwear", "Footwear", "Tailoring", "Accessories"]
categories =    ["Outerwear",
                "Footwear"]

# Place sizes for respective category in quotes, separated by commas
# Must be a filter on Grailed, case does matter
# e.g. ["Tops & Outerwear", "XS", "S", "M"]
# e.g. ["Bottoms & Pants", "29", "30", "31"]
# e.g. ["Footwear", "11.5", "12"]
sizes =     [["Tops & Outerwear", "L", "XL"],
            ["Bottoms & Pants"],
            ["Footwear", "10", "10.5", "11"],
            ["Tailoring"],
            ["Accessories"]]

# First value is the minimum price (set to 0 for no minimum), second is maximum price
# [min, max]
# e.g. [0, 500]
prices = [100, 200]

# Your email address
# e.g. "someone@site.com"
address = "grailed.notify@gmail.com"

# Your operating system
# e.g. "linux32"
# e.g. "linux64"
# e.g. "mac"
# e.g. "windows"
os = "mac"

# Time to wait until refreshing the page
# Must be placed after `os` argument in `bot` call
# Optional, defaults to 300 seconds (5 minutes)
# refresh_time = 600

bot = GrailedNotify(designers, categories, sizes, prices, address, os)

try:
    bot.main()
except KeyboardInterrupt:
    print " Exit detected"
