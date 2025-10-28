"""
MailMind Agent Orchestrator
Coordinates all AI agents in the system with comprehensive orchestration and automation
"""

from typing import Dict, Any, List, Optional
import asyncio
import logging
from datetime import datetime
from dataclasses import dataclass

# Import all agents
from .agents.base_agent import BaseAgent, AgentTask as BaseAgentTask, AgentResult, TaskPriority
from .agents.email_classifier import EmailClassifierAgent
from .agents.search_agent import SearchAgent
from .agents.tagging_agent import TaggingAgent
from .agents.summary_agent import SummaryAgent
from .agents.response_agent import ResponseAgent
from .agents.workflow_orchestration_agent import WorkflowOrchestrationAgent
from .agents.task_automation_agent import TaskAutomationAgent
from .agents.notification_agent import NotificationAgent
from .agents.scheduling_agent import SchedulingAgent

@dataclass
class AgentTask:
    """Legacy task format for backward compatibility"""
    agent_name: str
    task_type: str
    payload: Dict[str, Any]
    priority: int = 5

class AgentOrchestrator:
    """
    Enhanced central coordinator for all MailMind AI agents
    
    Features:
    - Comprehensive agent management and registration
    - Intelligent workflow orchestration
    - Real-time notifications and scheduling
    - Task automation and rule processing
    - Performance monitoring and health checks
    - Event-driven architecture with pub/sub
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.agents: Dict[str, BaseAgent] = {}
        self.task_queue = asyncio.Queue()
        self.results_cache = {}
        self.event_subscribers = {}
        
        self.logger = logging.getLogger("mailmind.orchestrator")
        self._setup_logging()
        
        # Initialize all agents
        self._initialize_agents()
        
        # Start background tasks
        self._start_background_tasks()
    
    def _setup_logging(self):
        """Setup logging for the orchestrator"""
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - Orchestrator - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
    
    def _initialize_agents(self):
        """Initialize and register all agents"""
        try:
            # Core processing agents
            self.register_agent("email_classifier", EmailClassifierAgent(self.config.get("classifier", {})))
            self.register_agent("search_agent", SearchAgent(self.config.get("search", {})))
            self.register_agent("tagging_agent", TaggingAgent(self.config.get("tagging", {})))
            self.register_agent("summary_agent", SummaryAgent(self.config.get("summary", {})))
            self.register_agent("response_agent", ResponseAgent(self.config.get("response", {})))
            
            # Orchestration and automation agents
            workflow_agent = WorkflowOrchestrationAgent(self.config.get("workflow", {}))
            self.register_agent("workflow_orchestration", workflow_agent)
            
            automation_agent = TaskAutomationAgent(self.config.get("automation", {}))
            self.register_agent("task_automation", automation_agent)
            
            notification_agent = NotificationAgent(self.config.get("notification", {}))
            self.register_agent("notification_agent", notification_agent)
            
            scheduling_agent = SchedulingAgent(self.config.get("scheduling", {}))
            self.register_agent("scheduling_agent", scheduling_agent)
            
            # Register agents with each other for cross-agent communication
            workflow_agent.register_agent("email_classifier", self.agents["email_classifier"])
            workflow_agent.register_agent("tagging_agent", self.agents["tagging_agent"])
            workflow_agent.register_agent("search_agent", self.agents["search_agent"])
            workflow_agent.register_agent("summary_agent", self.agents["summary_agent"])
            workflow_agent.register_agent("response_agent", self.agents["response_agent"])
            workflow_agent.register_agent("notification_agent", notification_agent)
            workflow_agent.register_agent("task_automation", automation_agent)
            
            scheduling_agent.register_agent("email_classifier", self.agents["email_classifier"])
            scheduling_agent.register_agent("notification_agent", notification_agent)
            scheduling_agent.register_agent("task_automation", automation_agent)
            
            self.logger.info("All agents initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Error initializing agents: {e}")
            raise
    
    def _start_background_tasks(self):
        """Start background processing tasks"""
        asyncio.create_task(self._task_processor())
        asyncio.create_task(self._health_monitor())
    
    def register_agent(self, name: str, agent_instance: BaseAgent):
        """Register an agent with the orchestrator"""
        self.agents[name] = agent_instance
        self.logger.info(f"Registered agent: {name}")
    
    def subscribe_event(self, event_type: str, callback: callable):
        """Subscribe to orchestrator events"""
        if event_type not in self.event_subscribers:
            self.event_subscribers[event_type] = []
        self.event_subscribers[event_type].append(callback)
    
    async def publish_event(self, event_type: str, event_data: Dict[str, Any]):
        """Publish an event to subscribers"""
        if event_type in self.event_subscribers:
            for callback in self.event_subscribers[event_type]:
                try:
                    await callback(event_data)
                except Exception as e:
                    self.logger.error(f"Error in event callback: {e}")
    
    async def process_email(self, email_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process an email through the complete AI pipeline
        
        Enhanced with workflow orchestration, automation rules, and notifications
        """
        email_id = email_data.get("id", "unknown")
        self.logger.info(f"Processing email: {email_id}")
        
        try:
            # Publish email received event
            await self.publish_event("email_received", email_data)
            
            # Step 1: Apply automation rules first
            automation_result = await self._execute_agent_task(
                "task_automation", "apply_rules", {"email_data": email_data}
            )
            
            # Step 2: Execute new email processing workflow
            workflow_result = await self._execute_agent_task(
                "workflow_orchestration", "execute_workflow", {
                    "template_id": "new_email_processing",
                    "workflow_data": email_data
                }
            )
            
            # Step 3: Check for notification triggers
            await self._execute_agent_task(
                "notification_agent", "check_notification_rules", {
                    "event_data": {
                        **email_data,
                        "event_type": "email_received",
                        "processing_results": workflow_result.data if workflow_result.success else {}
                    }
                }
            )
            
            # Consolidate results
            results = {
                "email_id": email_id,
                "processing_timestamp": datetime.utcnow().isoformat(),
                "automation": automation_result.data if automation_result.success else {"error": automation_result.error_message},
                "workflow": workflow_result.data if workflow_result.success else {"error": workflow_result.error_message},
                "success": automation_result.success and workflow_result.success
            }
            
            # Cache results
            self.results_cache[email_id] = results
            
            # Publish processing complete event
            await self.publish_event("email_processed", results)
            
            return results
            
        except Exception as e:
            self.logger.error(f"Error processing email {email_id}: {e}")
            error_result = {
                "email_id": email_id,
                "error": str(e),
                "success": False,
                "processing_timestamp": datetime.utcnow().isoformat()
            }
            
            await self.publish_event("email_processing_failed", error_result)
            return error_result
    
    async def _execute_agent_task(self, agent_name: str, task_type: str, payload: Dict[str, Any]) -> AgentResult:
        """Execute a task on a specific agent"""
        agent = self.agents.get(agent_name)
        if not agent:
            return AgentResult(
                success=False,
                data={},
                confidence=0.0,
                processing_time=0.0,
                error_message=f"Agent {agent_name} not found"
            )
        
        task = BaseAgentTask(
            task_id=f"{agent_name}_{task_type}_{datetime.utcnow().timestamp()}",
            task_type=task_type,
            payload=payload,
            priority=TaskPriority.NORMAL
        )
        
        return await agent.execute_task(task)
    
    async def execute_workflow(self, workflow_id: str, workflow_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a specific workflow"""
        workflow_agent = self.agents.get("workflow_orchestration")
        if not workflow_agent:
            return {"success": False, "error": "Workflow orchestration agent not available"}
        
        result = await self._execute_agent_task(
            "workflow_orchestration", "execute_workflow", {
                "template_id": workflow_id,
                "workflow_data": workflow_data
            }
        )
        
        return result.data if result.success else {"success": False, "error": result.error_message}
    
    async def create_reminder(self, email_id: str, user_id: str, reminder_time: str, message: str) -> Dict[str, Any]:
        """Create a reminder for an email"""
        result = await self._execute_agent_task(
            "scheduling_agent", "create_reminder", {
                "reminder_data": {
                    "email_id": email_id,
                    "user_id": user_id,
                    "reminder_time": reminder_time,
                    "message": message,
                    "reminder_type": "custom"
                }
            }
        )
        
        return result.data if result.success else {"success": False, "error": result.error_message}
    
    async def send_notification(self, notification_data: Dict[str, Any]) -> Dict[str, Any]:
        """Send a notification"""
        result = await self._execute_agent_task(
            "notification_agent", "send_notification", notification_data
        )
        
        return result.data if result.success else {"success": False, "error": result.error_message}
    
    async def get_smart_reply(self, email_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a smart reply for an email"""
        result = await self.execute_workflow("smart_reply", email_data)
        return result
    
    async def summarize_thread(self, thread_data: Dict[str, Any]) -> Dict[str, Any]:
        """Summarize an email thread"""
        result = await self.execute_workflow("thread_summary", thread_data)
        return result
    
    async def _task_processor(self):
        """Background task processor"""
        while True:
            try:
                # Process any queued tasks
                if not self.task_queue.empty():
                    task = await self.task_queue.get()
                    await self._process_queued_task(task)
                
                await asyncio.sleep(1)
                
            except Exception as e:
                self.logger.error(f"Error in task processor: {e}")
                await asyncio.sleep(5)
    
    async def _process_queued_task(self, task: AgentTask):
        """Process a queued task"""
        try:
            agent = self.agents.get(task.agent_name)
            if agent:
                # Convert to BaseAgentTask format
                base_task = BaseAgentTask(
                    task_id=f"queued_{task.agent_name}_{datetime.utcnow().timestamp()}",
                    task_type=task.task_type,
                    payload=task.payload,
                    priority=TaskPriority.NORMAL
                )
                
                result = await agent.execute_task(base_task)
                self.logger.info(f"Queued task completed: {task.agent_name}.{task.task_type}")
            else:
                self.logger.error(f"Agent not found for queued task: {task.agent_name}")
                
        except Exception as e:
            self.logger.error(f"Error processing queued task: {e}")
    
    async def _health_monitor(self):
        """Monitor agent health"""
        while True:
            try:
                for agent_name, agent in self.agents.items():
                    health = agent.get_health_status()
                    
                    if health.get("status") == "error":
                        self.logger.warning(f"Agent {agent_name} is in error state")
                        
                        # Send system alert
                        await self._execute_agent_task(
                            "notification_agent", "send_notification", {
                                "type": "system_alert",
                                "title": "Agent Health Alert",
                                "message": f"Agent {agent_name} is experiencing issues",
                                "priority": "high",
                                "channels": ["in_app", "email"],
                                "metadata": {"agent_health": health}
                            }
                        )
                
                await asyncio.sleep(60)  # Check every minute
                
            except Exception as e:
                self.logger.error(f"Error in health monitor: {e}")
                await asyncio.sleep(60)
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get overall system status"""
        agent_statuses = {}
        
        for agent_name, agent in self.agents.items():
            try:
                agent_statuses[agent_name] = agent.get_health_status()
            except Exception as e:
                agent_statuses[agent_name] = {
                    "status": "error",
                    "error": str(e)
                }
        
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "agents": agent_statuses,
            "queue_size": self.task_queue.qsize(),
            "cache_size": len(self.results_cache)
        }
    
    async def shutdown(self):
        """Graceful shutdown of the orchestrator"""
        self.logger.info("Shutting down orchestrator...")
        
        # Shutdown all agents
        for agent_name, agent in self.agents.items():
            try:
                await agent.shutdown()
                self.logger.info(f"Agent {agent_name} shut down")
            except Exception as e:
                self.logger.error(f"Error shutting down agent {agent_name}: {e}")
        
        self.logger.info("Orchestrator shutdown complete")
