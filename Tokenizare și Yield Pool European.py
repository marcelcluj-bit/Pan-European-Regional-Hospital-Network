import json
import dataclasses
from typing import List, Dict

@dataclasses.dataclass
class HospitalNode:
    node_id: str
    country: str
    city: str
    valuation_eur: float  # Real estate and medical asset valuation
    ai_labs_active: int   # Number of active AI electron microscope labs
    stake_weight: float = 0.0

class EUHealthTokenPool:
    """
    Management of the Unified RWA (Real World Assets) Tokenization Pool
    for 81 Regional Hospitals across 27 EU Member States.
    """
    def __init__(self, token_symbol: str = "MEDINFRA", total_supply: float = 500_000_000):
        self.token_symbol = token_symbol
        self.total_supply = total_supply
        self.hospitals: List[HospitalNode] = []
        self.total_network_valuation = 0.0

    def register_hospital(self, node: HospitalNode):
        """Registers a regional hospital in the unified European pool."""
        self.hospitals.append(node)
        self.total_network_valuation += node.valuation_eur
        self._recalculate_weights()

    def _recalculate_weights(self):
        """Recalculates each hospital's share in the common pool based on its valuation."""
        for h in self.hospitals:
            h.stake_weight = h.valuation_eur / self.total_network_valuation

    def calculate_token_backing(self) -> Dict:
        """Calculates the guaranteed backing value per token (RWA Asset Backing)."""
        val_per_token = self.total_network_valuation / self.total_supply
        return {
            "total_hospitals": len(self.hospitals),
            "total_network_tvl_eur": self.total_network_valuation,
            "token_supply": self.total_supply,
            "eur_value_per_token": round(val_per_token, 4)
        }

    def simulate_yield_distribution(self, total_annual_revenue_eur: float, apy_target: float = 0.10) -> Dict:
        """
        Simulates the distribution of generated revenues (medical services, hospitalization, equipment leasing)
        to token holders across the entire European network.
        """
        pool_yield = total_annual_revenue_eur * apy_target
        yield_per_token = pool_yield / self.total_supply
        
        distribution_by_country = {}
        for h in self.hospitals:
            if h.country not in distribution_by_country:
                distribution_by_country[h.country] = 0.0
            distribution_by_country[h.country] += pool_yield * h.stake_weight

        return {
            "total_revenue_simulated_eur": total_annual_revenue_eur,
            "total_yield_distributed_eur": pool_yield,
            "yield_per_token_eur": round(yield_per_token, 4),
            "allocation_per_country_eur": {k: round(v, 2) for k, v in distribution_by_country.items()}
        }

if __name__ == "__main__":
    eu_pool = EUHealthTokenPool(token_symbol="MEDINFRA", total_supply=500_000_000)

    sample_nodes = [
        HospitalNode("RO-01", "Romania", "Iasi", 500_000_000, 1),
        HospitalNode("RO-02", "Romania", "Cluj-Napoca", 500_000_000, 1),
        HospitalNode("RO-03", "Romania", "Craiova", 500_000_000, 1),
        HospitalNode("DE-01", "Germany", "Leipzig", 800_000_000, 1),
        HospitalNode("DE-02", "Germany", "Nuremberg", 750_000_000, 1),
        HospitalNode("PL-01", "Poland", "Krakow", 600_000_000, 1),
        HospitalNode("FR-01", "France", "Lyon", 850_000_000, 1),
    ]

    for node in sample_nodes:
        eu_pool.register_hospital(node)

    print("=== EU TOKENIZATION POOL METRICS ===")
    print(json.dumps(eu_pool.calculate_token_backing(), indent=2, ensure_ascii=False))

    print("\n=== ANNUAL YIELD DISTRIBUTION SIMULATION ===")
    simulation = eu_pool.simulate_yield_distribution(total_annual_revenue_eur=1_200_000_000, apy_target=0.10)
    print(json.dumps(simulation, indent=2, ensure_ascii=False))
