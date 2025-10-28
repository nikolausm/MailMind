"""
Workflow Orchestration Agent
Manages complex email processing workflows and coordinates multiple agents
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import asyncio
import uuid
from enum import Enum

from .base_agent import BaseAgent, AgentTask, AgentResult, TaskPriority

class WorkflowStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class StepStatus(Enum):
    WAITING = "waiting"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"

@dataclass
class WorkflowStep:
    """Individual step in a workflow"""
    step_id: str
    agent_name: str
    task_type: str
    payload: Dict[str, Any]
    dependencies: List[str] = None  # step_ids that must complete first
    retry_count: int = 3
    timeout: int = 300
    status: StepStatus = StepStatus.WAITING
    result: Optional[AgentResult] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []

@dataclass
class Workflow:
    """Complete workflow definition"""
    workflow_id: str
    name: str
    description: str
    steps: List[WorkflowStep]
    status: WorkflowStatus = WorkflowStatus.PENDING
    created_at: datetime = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.metadata is None:
            self.metadata = {}

class WorkflowOrchestrationAgent(BaseAgent):
    """
    Orchestrates complex email processing workflows
    
    Features:
    - Multi-step workflow execution
    - Dependency management between steps
    - Parallel execution where possible
    - Error handling and retry logic
    - Workflow state persistence
    - Performance monitoring
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__("workflow_orchestration", config)
        self.active_workflows: Dict[str, Workflow] = {}
        self.workflow_templates: Dict[str, Workflow] = {}
        self.agent_registry: Dict[str, BaseAgent] = {}
        self._initialize_default_templates()
    
    def _initialize_default_templates(self):
        """Initialize common workflow templates"""
        
        # New Email Processing Workflow
        new_email_workflow = Workflow(
            workflow_id="new_email_processing",
            name="New Email Processing",
            description="Complete processing pipeline for new emails",
            steps=[
                WorkflowStep(
                    step_id="classify",
                    agent_name="email_classifier",
                    task_type="classify_email",
                    payload={}
                ),
                WorkflowStep(
                    step_id="tag",
                    agent_name="tagging_agent",
                    task_type="generate_tags",
                    payload={},
                    dependencies=["classify"]
                ),
                WorkflowStep(
                    step_id="embed",
                    agent_name="search_agent",
                    task_type="generate_embedding",
                    payload={},
                    dependencies=["classify"]
                ),
                WorkflowStep(
                    step_id="notify",
                    agent_name="notification_agent",
                    task_type="send_notification",
                    payload={},
                    dependencies=["classify", "tag"]
                )
            ]
        )
        
        # Email Thread Summary Workflow
        thread_summary_workflow = Workflow(
            workflow_id="thread_summary",
            name="Email Thread Summary",
            description="Generate comprehensive thread summary with action items",
            steps=[
                WorkflowStep(
                    step_id="gather_thread",
                    agent_name="search_agent",
                    task_type="get_thread_emails",
                    payload={}
                ),
                WorkflowStep(
                    step_id="summarize",
                    agent_name="summary_agent",
                    task_type="summarize_thread",
                    payload={},
                    dependencies=["gather_thread"]
                ),
                WorkflowStep(
                    step_id="extract_actions",
                    agent_name="task_automation",
                    task_type="extract_action_items",
                    payload={},
                    dependencies=["summarize"]
                ),
                WorkflowStep(
                    step_id="schedule_followup",
                    agent_name="scheduling_agent",
                    task_type="schedule_followup",
                    payload={},
                    dependencies=["extract_actions"]
                )
            ]
        )
        
        # Smart Reply Workflow
        smart_reply_workflow = Workflow(
            workflow_id="smart_reply",
            name="Smart Reply Generation",
            description="Generate contextual email replies",
            steps=[
                WorkflowStep(
                    step_id="analyze_context",
                    agent_name="email_classifier",
                    task_type="analyze_reply_context",
                    payload={}
                ),
                WorkflowStep(
                    step_id="get_similar",
                    agent_name="search_agent",
                    task_type="find_similar_emails",
                    payload={},
                    dependencies=["analyze_context"]
                ),
                WorkflowStep(
                    step_id="generate_reply",
                    agent_name="response_agent",
                    task_type="generate_smart_reply",
                    payload={},
                    dependencies=["analyze_context", "get_similar"]
                )
            ]
        )
        
        self.workflow_templates = {
            "new_email_processing": new_email_workflow,
            "thread_summary": thread_summary_workflow,
            "smart_reply": smart_reply_workflow
        }
    
    def register_agent(self, agent_name: str, agent: BaseAgent):
        """Register an agent for workflow execution"""
        self.agent_registry[agent_name] = agent
        self.logger.info(f"Registered agent: {agent_name}")
    
    async def process_task(self, task: AgentTask) -> AgentResult:
        """Process workflow orchestration tasks"""
        try:
            if task.task_type == "execute_workflow":
                return await self._execute_workflow(task.payload)
            elif task.task_type == "create_workflow":
                return await self._create_workflow(task.payload)
            elif task.task_type == "get_workflow_status":
                return await self._get_workflow_status(task.payload)
            elif task.task_type == "cancel_workflow":
                return await self._cancel_workflow(task.payload)
            else:
                raise ValueError(f"Unknown task type: {task.task_type}")
                
        except Exception as e:
            return AgentResult(
                success=False,
                data={},
                confidence=0.0,
                processing_time=0.0,
                error_message=str(e)
            )
    
    def get_supported_task_types(self) -> List[str]:
        """Return supported task types"""
        return [
            "execute_workflow",
            "create_workflow", 
            "get_workflow_status",
            "cancel_workflow"
        ]
    
    async def _execute_workflow(self, payload: Dict[str, Any]) -> AgentResult:
        """Execute a workflow from template or definition"""
        template_id = payload.get("template_id")
        workflow_data = payload.get("workflow_data", {})
        
        if template_id and template_id in self.workflow_templates:
            # Create workflow from template
            template = self.workflow_templates[template_id]
            workflow = self._create_workflow_from_template(template, workflow_data)
        else:
            # Create workflow from payload
            workflow = self._parse_workflow_from_payload(payload)
        
        # Execute the workflow
        result = await self._run_workflow(workflow)
        
        return AgentResult(
            success=result["success"],
            data=result,
            confidence=1.0,
            processing_time=0.0
        )
    
    def _create_workflow_from_template(self, template: Workflow, data: Dict[str, Any]) -> Workflow:
        """Create a workflow instance from template"""
        workflow_id = str(uuid.uuid4())
        
        # Deep copy template
        workflow = Workflow(
            workflow_id=workflow_id,
            name=template.name,
            description=template.description,
            steps=[]
        )
        
        # Copy and customize steps
        for step in template.steps:
            new_step = WorkflowStep(
                step_id=f"{workflow_id}_{step.step_id}",
                agent_name=step.agent_name,
                task_type=step.task_type,
                payload={**step.payload, **data},
                dependencies=[f"{workflow_id}_{dep}" for dep in step.dependencies],
                retry_count=step.retry_count,
                timeout=step.timeout
            )
            workflow.steps.append(new_step)
        
        return workflow
    
    def _parse_workflow_from_payload(self, payload: Dict[str, Any]) -> Workflow:
        """Parse workflow definition from payload"""
        workflow_id = payload.get("workflow_id", str(uuid.uuid4()))
        
        workflow = Workflow(
            workflow_id=workflow_id,
            name=payload.get("name", "Custom Workflow"),
            description=payload.get("description", ""),
            steps=[]
        )
        
        for step_data in payload.get("steps", []):
            step = WorkflowStep(
                step_id=step_data["step_id"],
                agent_name=step_data["agent_name"],
                task_type=step_data["task_type"],
                payload=step_data.get("payload", {}),
                dependencies=step_data.get("dependencies", []),
                retry_count=step_data.get("retry_count", 3),
                timeout=step_data.get("timeout", 300)
            )
            workflow.steps.append(step)
        
        return workflow
    
    async def _run_workflow(self, workflow: Workflow) -> Dict[str, Any]:
        """Execute a complete workflow"""
        self.active_workflows[workflow.workflow_id] = workflow
        workflow.status = WorkflowStatus.RUNNING
        workflow.started_at = datetime.utcnow()
        
        self.logger.info(f"Starting workflow: {workflow.name} ({workflow.workflow_id})")
        
        try:
            # Execute steps according to dependencies
            completed_steps = set()
            
            while len(completed_steps) < len(workflow.steps):
                # Find ready steps (dependencies met)
                ready_steps = []
                for step in workflow.steps:
                    if (step.status == StepStatus.WAITING and 
                        all(dep in completed_steps for dep in step.dependencies)):
                        ready_steps.append(step)
                
                if not ready_steps:
                    # Check for failed dependencies
                    failed_steps = [s for s in workflow.steps if s.status == StepStatus.FAILED]
                    if failed_steps:
                        workflow.status = WorkflowStatus.FAILED
                        break
                    # Wait a bit and try again
                    await asyncio.sleep(0.1)
                    continue
                
                # Execute ready steps in parallel
                tasks = []
                for step in ready_steps:
                    task = self._execute_step(workflow, step)
                    tasks.append(task)
                
                # Wait for all parallel steps to complete
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
                # Process results
                for i, result in enumerate(results):
                    step = ready_steps[i]
                    if isinstance(result, Exception):
                        step.status = StepStatus.FAILED
                        self.logger.error(f"Step {step.step_id} failed: {result}")
                    else:
                        if result.success:
                            step.status = StepStatus.COMPLETED
                            completed_steps.add(step.step_id)
                        else:
                            step.status = StepStatus.FAILED
                            
                        step.result = result
                        step.completed_at = datetime.utcnow()
            
            # Check final status
            if workflow.status != WorkflowStatus.FAILED:
                workflow.status = WorkflowStatus.COMPLETED
            
            workflow.completed_at = datetime.utcnow()
            
            self.logger.info(f"Workflow {workflow.workflow_id} completed with status: {workflow.status}")
            
            return {
                "success": workflow.status == WorkflowStatus.COMPLETED,
                "workflow_id": workflow.workflow_id,
                "status": workflow.status.value,
                "steps": [
                    {
                        "step_id": step.step_id,
                        "status": step.status.value,
                        "result": step.result.__dict__ if step.result else None
                    }
                    for step in workflow.steps
                ]
            }
            
        except Exception as e:
            workflow.status = WorkflowStatus.FAILED
            workflow.completed_at = datetime.utcnow()
            self.logger.error(f"Workflow {workflow.workflow_id} failed: {e}")
            
            return {
                "success": False,
                "workflow_id": workflow.workflow_id,
                "status": WorkflowStatus.FAILED.value,
                "error": str(e)
            }
    
    async def _execute_step(self, workflow: Workflow, step: WorkflowStep) -> AgentResult:
        """Execute a single workflow step"""
        step.status = StepStatus.RUNNING
        step.started_at = datetime.utcnow()
        
        self.logger.info(f"Executing step: {step.step_id} using {step.agent_name}")
        
        agent = self.agent_registry.get(step.agent_name)
        if not agent:
            return AgentResult(
                success=False,
                data={},
                confidence=0.0,
                processing_time=0.0,
                error_message=f"Agent {step.agent_name} not found"
            )
        
        # Create task for the agent
        task = AgentTask(
            task_id=f"{workflow.workflow_id}_{step.step_id}",
            task_type=step.task_type,
            payload=step.payload,
            timeout=step.timeout
        )
        
        # Execute with retries
        for attempt in range(step.retry_count):
            try:
                result = await agent.execute_task(task)
                if result.success:
                    return result
                else:
                    self.logger.warning(f"Step {step.step_id} attempt {attempt + 1} failed: {result.error_message}")
                    if attempt < step.retry_count - 1:
                        await asyncio.sleep(2 ** attempt)  # Exponential backoff
            except Exception as e:
                self.logger.error(f"Step {step.step_id} attempt {attempt + 1} error: {e}")
                if attempt < step.retry_count - 1:
                    await asyncio.sleep(2 ** attempt)
        
        # All retries failed
        return AgentResult(
            success=False,
            data={},
            confidence=0.0,
            processing_time=0.0,
            error_message=f"Step failed after {step.retry_count} attempts"
        )
    
    async def _create_workflow(self, payload: Dict[str, Any]) -> AgentResult:
        """Create a new workflow template"""
        try:
            workflow = self._parse_workflow_from_payload(payload)
            self.workflow_templates[workflow.workflow_id] = workflow
            
            return AgentResult(
                success=True,
                data={"workflow_id": workflow.workflow_id},
                confidence=1.0,
                processing_time=0.0
            )
        except Exception as e:
            return AgentResult(
                success=False,
                data={},
                confidence=0.0,
                processing_time=0.0,
                error_message=str(e)
            )
    
    async def _get_workflow_status(self, payload: Dict[str, Any]) -> AgentResult:
        """Get status of an active workflow"""
        workflow_id = payload.get("workflow_id")
        
        if workflow_id in self.active_workflows:
            workflow = self.active_workflows[workflow_id]
            
            return AgentResult(
                success=True,
                data={
                    "workflow_id": workflow.workflow_id,
                    "status": workflow.status.value,
                    "steps": [
                        {
                            "step_id": step.step_id,
                            "status": step.status.value,
                            "started_at": step.started_at.isoformat() if step.started_at else None,
                            "completed_at": step.completed_at.isoformat() if step.completed_at else None
                        }
                        for step in workflow.steps
                    ]
                },
                confidence=1.0,
                processing_time=0.0
            )
        else:
            return AgentResult(
                success=False,
                data={},
                confidence=0.0,
                processing_time=0.0,
                error_message=f"Workflow {workflow_id} not found"
            )
    
    async def _cancel_workflow(self, payload: Dict[str, Any]) -> AgentResult:
        """Cancel a running workflow"""
        workflow_id = payload.get("workflow_id")
        
        if workflow_id in self.active_workflows:
            workflow = self.active_workflows[workflow_id]
            workflow.status = WorkflowStatus.CANCELLED
            workflow.completed_at = datetime.utcnow()
            
            return AgentResult(
                success=True,
                data={"workflow_id": workflow_id, "status": "cancelled"},
                confidence=1.0,
                processing_time=0.0
            )
        else:
            return AgentResult(
                success=False,
                data={},
                confidence=0.0,
                processing_time=0.0,
                error_message=f"Workflow {workflow_id} not found"
            )