"""Fail fast when the canonical council is incomplete or unsafe."""

from al_mehdi.catalog import build_catalog


def main() -> None:
    agents = build_catalog()
    assert len(agents) == 100
    assert len({agent.agent_id for agent in agents}) == 100
    assert len({agent.team for agent in agents}) == 10
    assert all(agent.action_scope == "recommend_only" for agent in agents)
    print("Verified: 100 unique recommendation-only agents across 10 teams.")


if __name__ == "__main__":
    main()

