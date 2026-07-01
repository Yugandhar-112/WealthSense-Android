"""
Labeled dataset: merchant/payee text -> spending category.

This is the single source of truth for training data. Each entry is text
roughly as it would appear after the app's regex extracts a "merchant" name
from a payment notification (so includes realistic noise: suffixes like
PVT LTD, trailing numbers, all-caps, etc.)

Categories were chosen to cover common Indian digital-payment spending
patterns. Extend this list with more real examples over time (e.g. export
your own transaction history) to improve accuracy.
"""

DATA = [
    # ---- Food ----
    ("SWIGGY", "Food"), ("SWIGGY BANGALORE", "Food"), ("SWIGGY LIMITED", "Food"),
    ("ZOMATO", "Food"), ("ZOMATO ONLINE", "Food"), ("ZOMATO LTD", "Food"),
    ("UBER EATS", "Food"), ("DOMINOS PIZZA", "Food"), ("DOMINOS", "Food"),
    ("MCDONALDS", "Food"), ("MC DONALDS INDIA", "Food"), ("KFC", "Food"),
    ("BURGER KING", "Food"), ("STARBUCKS", "Food"), ("STARBUCKS COFFEE", "Food"),
    ("CAFE COFFEE DAY", "Food"), ("CCD", "Food"), ("BARBEQUE NATION", "Food"),
    ("HALDIRAM", "Food"), ("HALDIRAMS", "Food"), ("FAASOS", "Food"),
    ("BEHROUZ BIRYANI", "Food"), ("SUBWAY", "Food"), ("EATSURE", "Food"),
    ("RESTAURANT", "Food"), ("HOTEL FOOD PLAZA", "Food"), ("BAKERY", "Food"),

    # ---- Groceries ----
    ("BLINKIT", "Groceries"), ("BLINKIT GROFERS INDIA", "Groceries"),
    ("ZEPTO", "Groceries"), ("ZEPTO MARKETPLACE", "Groceries"),
    ("INSTAMART", "Groceries"), ("SWIGGY INSTAMART", "Groceries"),
    ("BIGBASKET", "Groceries"), ("BIG BASKET", "Groceries"),
    ("DMART", "Groceries"), ("D MART READY", "Groceries"),
    ("RELIANCE FRESH", "Groceries"), ("RELIANCE SMART", "Groceries"),
    ("MORE SUPERMARKET", "Groceries"), ("SPENCERS", "Groceries"),
    ("NATURE BASKET", "Groceries"), ("JIOMART", "Groceries"),
    ("LOCAL KIRANA STORE", "Groceries"), ("GENERAL STORE", "Groceries"),

    # ---- Shopping ----
    ("AMAZON", "Shopping"), ("AMAZON SELLER SERVICES", "Shopping"),
    ("AMAZON PAY", "Shopping"), ("FLIPKART", "Shopping"),
    ("FLIPKART INTERNET PVT LTD", "Shopping"), ("MYNTRA", "Shopping"),
    ("MYNTRA DESIGNS", "Shopping"), ("AJIO", "Shopping"),
    ("NYKAA", "Shopping"), ("NYKAA FASHION", "Shopping"),
    ("MEESHO", "Shopping"), ("SNAPDEAL", "Shopping"),
    ("TATA CLIQ", "Shopping"), ("DECATHLON", "Shopping"),
    ("IKEA", "Shopping"), ("LIFESTYLE STORES", "Shopping"),
    ("SHOPPERS STOP", "Shopping"), ("CROMA", "Shopping"),
    ("RELIANCE DIGITAL", "Shopping"), ("VIJAY SALES", "Shopping"),

    # ---- Transport ----
    ("UBER", "Transport"), ("UBER INDIA SYSTEMS", "Transport"),
    ("OLA", "Transport"), ("OLA CABS", "Transport"), ("ANI TECHNOLOGIES", "Transport"),
    ("RAPIDO", "Transport"), ("RAPIDO BIKE TAXI", "Transport"),
    ("IRCTC", "Transport"), ("INDIAN RAILWAYS", "Transport"),
    ("REDBUS", "Transport"), ("METRO RAIL", "Transport"),
    ("NAMMA METRO", "Transport"), ("PETROL PUMP", "Transport"),
    ("INDIAN OIL", "Transport"), ("HP PETROL", "Transport"),
    ("FASTAG RECHARGE", "Transport"), ("PARKING FEE", "Transport"),
    ("YULU BIKE", "Transport"), ("INDRIVE", "Transport"),

    # ---- Bills & Utilities ----
    ("AIRTEL", "Bills"), ("BHARTI AIRTEL", "Bills"), ("AIRTEL PREPAID RECHARGE", "Bills"),
    ("JIO", "Bills"), ("RELIANCE JIO", "Bills"), ("JIO RECHARGE", "Bills"),
    ("VODAFONE IDEA", "Bills"), ("VI RECHARGE", "Bills"),
    ("BESCOM", "Bills"), ("ELECTRICITY BOARD", "Bills"), ("ELECTRICITY BILL", "Bills"),
    ("TATA POWER", "Bills"), ("WATER BOARD BILL", "Bills"),
    ("GAS CYLINDER BOOKING", "Bills"), ("INDANE GAS", "Bills"),
    ("ACT FIBERNET", "Bills"), ("BROADBAND BILL", "Bills"),
    ("LIC PREMIUM", "Bills"), ("LIFE INSURANCE CORPORATION", "Bills"),
    ("HDFC CREDIT CARD BILL", "Bills"), ("SBI CARD PAYMENT", "Bills"),

    # ---- Entertainment ----
    ("NETFLIX", "Entertainment"), ("NETFLIX COM", "Entertainment"),
    ("SPOTIFY", "Entertainment"), ("SPOTIFY INDIA", "Entertainment"),
    ("HOTSTAR", "Entertainment"), ("DISNEY HOTSTAR", "Entertainment"),
    ("PRIME VIDEO", "Entertainment"), ("AMAZON PRIME", "Entertainment"),
    ("BOOKMYSHOW", "Entertainment"), ("BOOK MY SHOW", "Entertainment"),
    ("PVR CINEMAS", "Entertainment"), ("INOX", "Entertainment"),
    ("YOUTUBE PREMIUM", "Entertainment"), ("SONY LIV", "Entertainment"),
    ("ZEE5", "Entertainment"), ("GAMING ZONE", "Entertainment"),
    ("STEAM GAMES", "Entertainment"), ("PLAYSTATION STORE", "Entertainment"),

    # ---- Health ----
    ("APOLLO PHARMACY", "Health"), ("APOLLO HOSPITALS", "Health"),
    ("PHARMEASY", "Health"), ("PHARM EASY", "Health"),
    ("PRACTO", "Health"), ("PRACTO TECHNOLOGIES", "Health"),
    ("NETMEDS", "Health"), ("1MG", "Health"), ("TATA 1MG", "Health"),
    ("FORTIS HOSPITAL", "Health"), ("MANIPAL HOSPITAL", "Health"),
    ("MEDPLUS PHARMACY", "Health"), ("DIAGNOSTIC CENTRE", "Health"),
    ("CULT FIT", "Health"), ("CULTFIT HEALTHIFYME", "Health"),
    ("HEALTHIFYME", "Health"), ("DENTIST CLINIC", "Health"),

    # ---- Miscellaneous (fallback bucket - unclear / other) ----
    ("ATM CASH WITHDRAWAL", "Miscellaneous"), ("UNKNOWN MERCHANT", "Miscellaneous"),
    ("BANK TRANSFER", "Miscellaneous"), ("SELF TRANSFER", "Miscellaneous"),
    ("RANDOM PERSON NAME", "Miscellaneous"), ("MISC PAYMENT", "Miscellaneous"),
    ("DONATION", "Miscellaneous"), ("TEMPLE DONATION", "Miscellaneous"),
    ("RENT PAYMENT", "Miscellaneous"), ("SALARY CREDIT REVERSAL", "Miscellaneous"),
]

CATEGORIES = ["Food", "Groceries", "Shopping", "Transport", "Bills", "Entertainment", "Health", "Miscellaneous"]

if __name__ == "__main__":
    from collections import Counter
    counts = Counter(c for _, c in DATA)
    print(f"Total examples: {len(DATA)}")
    for cat in CATEGORIES:
        print(f"  {cat}: {counts.get(cat, 0)}")
