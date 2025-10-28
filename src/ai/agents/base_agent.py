"""
Base Agent Class
Provides common functionality for all MailMind AI agents
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime
import logging
import asyncio
from enum import Enum

class AgentStatus(Enum):
    IDLE = "idle"
    PROCESSING = "processing"
    ERROR = "error"
    MAINTENANCE = "maintenance"

class TaskPriority(Enum):
    CRITICAL = 1
    HIGH = 2
    NORMAL = 3
    LOW = 4

@dataclass
class AgentResult:
    """Standardized result format for all agents"""
    success: bool
    data: Dict[str, Any]
    confidence: float
    processing_time: float
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = None

@dataclass
class AgentTask:
    """Task representation for agent processing"""
    task_id: str
    task_type: str
    payload: Dict[str, Any]
    priority: TaskPriority = TaskPriority.NORMAL
    created_at: datetime = None
    timeout: int = 300  # seconds

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()

class BaseAgent(ABC):
    """
    Abstract base class for all MailMind AI agents
    
    Provides common functionality:
    - Task processing framework
    - Error handling and logging
    - Performance monitoring
    - Health checks
    - Configuration management
    """
    
    def __init__(self, agent_name: str, config: Dict[str, Any] = None):
        self.agent_name = agent_name
        self.config = config or {}
        self.status = AgentStatus.IDLE
        self.logger = logging.getLogger(f"mailmind.agent.{agent_name}")
        self.task_queue = asyncio.Queue()
        self.metrics = {
            "tasks_processed": 0,
            "tasks_failed": 0,
            "average_processing_time": 0.0,
            "last_activity": None
        }
        self._setup_logging()
    
    def _setup_logging(self):
        """Configure logging for the agent"""
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            f'%(asctime)s - {self.agent_name} - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
    
    @abstractmethod
    async def process_task(self, task: AgentTask) -> AgentResult:
        """
        Process a single task
        
        Args:
            task: The task to process
            
        Returns:
            AgentResult with processing results
        """
        pass
    
    @abstractmethod
    def get_supported_task_types(self) -> List[str]:
        """
        Return list of task types this agent can handle
        
        Returns:
            List of supported task type strings
        """
        pass
    
    async def execute_task(self, task: AgentTask) -> AgentResult:
        """
        Execute a task with full error handling and metrics
        
        Args:
            task: The task to execute
            
        Returns:
            AgentResult with execution results
        """
        start_time = datetime.utcnow()
        self.status = AgentStatus.PROCESSING
        
        try:
            self.logger.info(f"Starting task {task.task_id} of type {task.task_type}")
            
            # Validate task type
            if task.task_type not in self.get_supported_task_types():
                raise ValueError(f"Unsupported task type: {task.task_type}")
            
            # Process with timeout
            result = await asyncio.wait_for(
                self.process_task(task),
                timeout=task.timeout
            )
            
            # Update metrics
            processing_time = (datetime.utcnow() - start_time).total_seconds()
            result.processing_time = processing_time
            
            self.metrics["tasks_processed"] += 1
            self.metrics["last_activity"] = datetime.utcnow()
            self._update_average_processing_time(processing_time)
            
            self.logger.info(f"Completed task {task.task_id} in {processing_time:.2f}s")
            self.status = AgentStatus.IDLE
            
            return result
            
        except asyncio.TimeoutError:
            error_msg = f"Task {task.task_id} timed out after {task.timeout}s"
            self.logger.error(error_msg)
            self.metrics["tasks_failed"] += 1
            self.status = AgentStatus.ERROR
            
            return AgentResult(
                success=False,
                data={},
                confidence=0.0,
                processing_time=(datetime.utcnow() - start_time).total_seconds(),
                error_message=error_msg
            )
            
        except Exception as e:
            error_msg = f"Error processing task {task.task_id}: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            self.metrics["tasks_failed"] += 1
            self.status = AgentStatus.ERROR
            
            return AgentResult(
                success=False,
                data={},
                confidence=0.0,
                processing_time=(datetime.utcnow() - start_time).total_seconds(),
                error_message=error_msg
            )
    
    def _update_average_processing_time(self, processing_time: float):
        """Update rolling average processing time"""
        current_avg = self.metrics["average_processing_time"]
        total_tasks = self.metrics["tasks_processed"]
        
        if total_tasks == 1:
            self.metrics["average_processing_time"] = processing_time
        else:
            # Rolling average calculation
            self.metrics["average_processing_time"] = (
                (current_avg * (total_tasks - 1) + processing_time) / total_tasks
            )
    
    def get_health_status(self) -> Dict[str, Any]:
        """
        Get agent health and performance metrics
        
        Returns:
            Dictionary containing health status and metrics
        """
        return {
            "agent_name": self.agent_name,
            "status": self.status.value,
            "supported_tasks": self.get_supported_task_types(),
            "metrics": self.metrics.copy(),
            "config": self.config.copy()
        }
    
    def update_config(self, new_config: Dict[str, Any]):
        """
        Update agent configuration
        
        Args:
            new_config: New configuration dictionary
        """
        self.config.update(new_config)
        self.logger.info(f"Configuration updated: {new_config}")
    
    async def shutdown(self):
        """Graceful shutdown of the agent"""
        self.status = AgentStatus.MAINTENANCE
        self.logger.info(f"Agent {self.agent_name} shutting down...")
        
        # Wait for current tasks to complete (with timeout)
        try:
            await asyncio.wait_for(self._wait_for_idle(), timeout=30)
        except asyncio.TimeoutError:
            self.logger.warning("Shutdown timeout - forcing stop")
        
        self.logger.info(f"Agent {self.agent_name} shutdown complete")
    
    async def _wait_for_idle(self):
        """Wait for agent to become idle"""
        while self.status == AgentStatus.PROCESSING:
            await asyncio.sleep(0.1)