from typing import Dict, List, Any
from shared.protocol import AgentCard, AgentSkill

class Registry:
    def __init__(self):
        self.agents: Dict[str, AgentCard] = {}

    def register_agent(self, agent: AgentCard):
        self.agents[agent.name] = agent
        print(f"Registered agent: {agent.name} with skills: {[s.name for s in agent.skills]}")

    def get_all_skills(self) -> List[AgentSkill]:
        skills = []
        for agent in self.agents.values():
            for skill in agent.skills:
                skills.append(skill)
        return skills

registry = Registry()
