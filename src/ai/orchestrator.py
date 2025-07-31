"""
MailMind Agent Orchestrator
Coordinates all AI agents in the system
"""

from typing import Dict, Any, List
import asyncio
from dataclasses import dataclass

@dataclass
class AgentTask:
    agent_name: str
    task_type: str
    payload: Dict[str, Any]
    priority: int = 5

class AgentOrchestrator:
    """
    Central coordinator for all MailMind AI agents
    """
    
    def __init__(self):
        self.agents = {}
        self.task_queue = asyncio.Queue()
        self.results_cache = {}
        
    def register_agent(self, name: str, agent_instance):
        """Register an agent with the orchestrator"""
        self.agents[name] = agent_instance
        
    async def process_email(self, email_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process an email through all relevant agents
        
        Returns consolidated results from all agents
        """
        tasks = [
            AgentTask("classifier", "classify", email_data, priority=1),
            AgentTask("tagger", "tag", email_data, priority=2),
            AgentTask("embedder", "generate_embedding", email_data, priority=3)
        ]
        
        results = {}
        for task in sorted(tasks, key=lambda x: x.priority):
            agent = self.agents.get(task.agent_name)
            if agent:
                result = await agent.process(task.payload)
                results[task.agent_name] = result
                
        return results
