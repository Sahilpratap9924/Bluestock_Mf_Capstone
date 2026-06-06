import numpy as np
import matplotlib.pyplot as plt

# Assumptions
current_nav = 100

annual_return = 0.12
annual_volatility = 0.18

years = 5
days = years * 252

simulations = 100

plt.figure(figsize=(12,6))

for i in range(simulations):

    returns = np.random.normal(
        annual_return / 252,
        annual_volatility / np.sqrt(252),
        days
    )

    nav_path = current_nav * np.cumprod(
        1 + returns
    )

    plt.plot(
        nav_path,
        alpha=0.1
    )

plt.title(
    "Monte Carlo Simulation: NAV Projection (5 Years)"
)

plt.xlabel("Trading Days")

plt.ylabel("Projected NAV")

plt.tight_layout()

plt.savefig(
    "reports/monte_carlo_projection.png",
    dpi=150
)

plt.show()