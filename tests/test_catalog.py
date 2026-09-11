import unittest

from al_mehdi.catalog import build_catalog


class CatalogTests(unittest.TestCase):
    def test_catalog_contains_exactly_100_unique_agents(self) -> None:
        agents = build_catalog()
        self.assertEqual(len(agents), 100)
        self.assertEqual(len({agent.agent_id for agent in agents}), 100)
        self.assertEqual(len({agent.name for agent in agents}), 100)

    def test_catalog_contains_ten_balanced_teams(self) -> None:
        agents = build_catalog()
        counts: dict[str, int] = {}
        for agent in agents:
            counts[agent.team] = counts.get(agent.team, 0) + 1
        self.assertEqual(len(counts), 10)
        self.assertTrue(all(count == 10 for count in counts.values()))

    def test_every_agent_is_recommendation_only(self) -> None:
        self.assertTrue(all(agent.action_scope == "recommend_only" for agent in build_catalog()))


if __name__ == "__main__":
    unittest.main()

