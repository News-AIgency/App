import matplotlib.pyplot as plt

# Data for the graph
fuels = [
    "Benzín natural 95",
    "Benzín natural 98",
    "Motorová nafta",
    "Prémiová nafta",
    "Prémiový benzín 98",
]
prices = [1.506, 1.716, 1.480, 1.686, 1.714]

# Create a bar graph
plt.bar(fuels, prices, color=["blue", "green", "orange", "red", "purple"])
plt.xlabel("Druh pohonných látok")
plt.ylabel("Cena za liter (EUR)")
plt.title("Priemerné ceny pohonných látok v SR – 12. týždeň 2025")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
