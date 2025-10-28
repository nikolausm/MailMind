"""
Scheduling Agent
Handles time-based operations, reminders, and scheduled tasks for email management
"""

from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import asyncio
import json
import uuid
from croniter import croniter

from .base_agent import BaseAgent, AgentTask, AgentResult, TaskPriority

class ScheduleType(Enum):
    ONE_TIME = "one_time"
    RECURRING = "recurring"
    CRON = "cron"
    INTERVAL = "interval"

class TaskStatus(Enum):
    SCHEDULED = "scheduled"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    PAUSED = "paused"

class RecurrencePattern(Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"
    WEEKDAYS = "weekdays"
    WEEKENDS = "weekends"

@dataclass
class ScheduledTask:
    """Represents a scheduled task"""
    task_id: str
    name: str
    description: str
    schedule_type: ScheduleType
    target_agent: str
    target_task_type: str
    payload: Dict[str, Any]
    
    # Scheduling parameters
    scheduled_time: Optional[datetime] = None
    recurrence_pattern: Optional[RecurrencePattern] = None
    cron_expression: Optional[str] = None
    interval_seconds: Optional[int] = None
    
    # Execution tracking
    status: TaskStatus = TaskStatus.SCHEDULED
    created_at: datetime = field(default_factory=datetime.utcnow)
    last_executed: Optional[datetime] = None
    next_execution: Optional[datetime] = None
    execution_count: int = 0
    max_executions: Optional[int] = None
    
    # Error handling
    retry_count: int = 3
    retry_delay_seconds: int = 60
    current_retries: int = 0
    last_error: Optional[str] = None
    
    # Metadata
    user_id: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ReminderTask:
    """Special type of scheduled task for reminders"""
    reminder_id: str
    email_id: str
    reminder_type: str  # "followup", "deadline", "custom"
    reminder_time: datetime
    message: str
    user_id: str
    completed: bool = False
    snoozed_until: Optional[datetime] = None
    snooze_count: int = 0
    created_at: datetime = field(default_factory=datetime.utcnow)

class SchedulingAgent(BaseAgent):
    """
    Handles time-based operations and scheduling for MailMind
    
    Features:
    - One-time and recurring task scheduling
    - Cron-based scheduling with flexible patterns
    - Email reminders and follow-ups
    - Deadline tracking and notifications
    - Task retry logic with exponential backoff
    - Integration with other agents for task execution
    - Performance monitoring and optimization
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__("scheduling_agent", config)
        self.scheduled_tasks: Dict[str, ScheduledTask] = {}
        self.reminders: Dict[str, ReminderTask] = {}
        self.agent_registry: Dict[str, BaseAgent] = {}
        self.running_tasks: Dict[str, asyncio.Task] = {}
        
        # Start the scheduler background task
        self._scheduler_task = asyncio.create_task(self._scheduler_loop())
        
        # Initialize default reminder templates
        self._initialize_reminder_templates()
    
    def _initialize_reminder_templates(self):
        """Initialize default reminder templates"""
        self.reminder_templates = {
            "followup": {
                "title": "Follow-up Reminder",
                "message": "Don't forget to follow up on: {subject}",
                "default_delay_hours": 24
            },
            "deadline": {
                "title": "Deadline Reminder",
                "message": "Deadline approaching: {subject} - Due: {deadline}",
                "default_delay_hours": 2
            },
            "meeting": {
                "title": "Meeting Reminder",
                "message": "Meeting reminder: {subject} at {meeting_time}",
                "default_delay_hours": 1
            },
            "custom": {
                "title": "Reminder",
                "message": "Reminder: {message}",
                "default_delay_hours": 24
            }
        }
    
    def register_agent(self, agent_name: str, agent: BaseAgent):
        """Register an agent for task execution"""
        self.agent_registry[agent_name] = agent
        self.logger.info(f"Registered agent for scheduling: {agent_name}")
    
    async def process_task(self, task: AgentTask) -> AgentResult:
        """Process scheduling tasks"""
        try:
            if task.task_type == "schedule_task":
                return await self._schedule_task(task.payload)
            elif task.task_type == "cancel_task":
                return await self._cancel_task(task.payload)
            elif task.task_type == "pause_task":
                return await self._pause_task(task.payload)
            elif task.task_type == "resume_task":
                return await self._resume_task(task.payload)
            elif task.task_type == "get_scheduled_tasks":
                return await self._get_scheduled_tasks(task.payload)
            elif task.task_type == "create_reminder":
                return await self._create_reminder(task.payload)
            elif task.task_type == "snooze_reminder":
                return await self._snooze_reminder(task.payload)
            elif task.task_type == "get_reminders":
                return await self._get_reminders(task.payload)
            elif task.task_type == "schedule_followup":
                return await self._schedule_followup(task.payload)
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
            "schedule_task",
            "cancel_task",
            "pause_task",
            "resume_task",
            "get_scheduled_tasks",
            "create_reminder",
            "snooze_reminder",
            "get_reminders",
            "schedule_followup"
        ]
    
    async def _schedule_task(self, payload: Dict[str, Any]) -> AgentResult:
        """Schedule a new task"""
        try:
            task_data = payload.get("task_data", {})
            
            scheduled_task = ScheduledTask(
                task_id=task_data.get("task_id", str(uuid.uuid4())),
                name=task_data["name"],
                description=task_data.get("description", ""),
                schedule_type=ScheduleType(task_data["schedule_type"]),
                target_agent=task_data["target_agent"],
                target_task_type=task_data["target_task_type"],
                payload=task_data.get("payload", {}),
                scheduled_time=self._parse_datetime(task_data.get("scheduled_time")),
                recurrence_pattern=RecurrencePattern(task_data["recurrence_pattern"]) if task_data.get("recurrence_pattern") else None,
                cron_expression=task_data.get("cron_expression"),
                interval_seconds=task_data.get("interval_seconds"),
                max_executions=task_data.get("max_executions"),
                retry_count=task_data.get("retry_count", 3),
                retry_delay_seconds=task_data.get("retry_delay_seconds", 60),
                user_id=task_data.get("user_id"),
                tags=task_data.get("tags", []),
                metadata=task_data.get("metadata", {})
            )
            
            # Calculate next execution time
            scheduled_task.next_execution = self._calculate_next_execution(scheduled_task)
            
            if not scheduled_task.next_execution:
                return AgentResult(
                    success=False,
                    data={},
                    confidence=0.0,
                    processing_time=0.0,
                    error_message="Could not calculate next execution time"
                )
            
            self.scheduled_tasks[scheduled_task.task_id] = scheduled_task
            
            self.logger.info(f"Scheduled task {scheduled_task.task_id}: {scheduled_task.name}")
            
            return AgentResult(
                success=True,
                data={
                    "task_id": scheduled_task.task_id,
                    "next_execution": scheduled_task.next_execution.isoformat(),
                    "message": "Task scheduled successfully"
                },
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
    
    def _parse_datetime(self, dt_str: Optional[str]) -> Optional[datetime]:
        """Parse datetime string to datetime object"""
        if not dt_str:
            return None
        
        try:
            if isinstance(dt_str, str):
                return datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
            elif isinstance(dt_str, datetime):
                return dt_str
            else:
                return None
        except ValueError:
            self.logger.error(f"Invalid datetime format: {dt_str}")
            return None
    
    def _calculate_next_execution(self, scheduled_task: ScheduledTask) -> Optional[datetime]:
        """Calculate the next execution time for a task"""
        now = datetime.utcnow()
        
        if scheduled_task.schedule_type == ScheduleType.ONE_TIME:
            if scheduled_task.scheduled_time and scheduled_task.scheduled_time > now:
                return scheduled_task.scheduled_time
            else:
                return None
        
        elif scheduled_task.schedule_type == ScheduleType.RECURRING:
            if not scheduled_task.recurrence_pattern:
                return None
            
            base_time = scheduled_task.last_executed or scheduled_task.scheduled_time or now
            
            if scheduled_task.recurrence_pattern == RecurrencePattern.DAILY:
                return base_time + timedelta(days=1)
            elif scheduled_task.recurrence_pattern == RecurrencePattern.WEEKLY:
                return base_time + timedelta(weeks=1)
            elif scheduled_task.recurrence_pattern == RecurrencePattern.MONTHLY:
                return base_time + timedelta(days=30)  # Approximate
            elif scheduled_task.recurrence_pattern == RecurrencePattern.YEARLY:
                return base_time + timedelta(days=365)  # Approximate
            elif scheduled_task.recurrence_pattern == RecurrencePattern.WEEKDAYS:
                next_time = base_time + timedelta(days=1)
                while next_time.weekday() >= 5:  # Skip weekends
                    next_time += timedelta(days=1)
                return next_time
            elif scheduled_task.recurrence_pattern == RecurrencePattern.WEEKENDS:
                next_time = base_time + timedelta(days=1)
                while next_time.weekday() < 5:  # Skip weekdays
                    next_time += timedelta(days=1)
                return next_time
        
        elif scheduled_task.schedule_type == ScheduleType.CRON:
            if not scheduled_task.cron_expression:
                return None
            
            try:
                cron = croniter(scheduled_task.cron_expression, now)
                return cron.get_next(datetime)
            except Exception as e:
                self.logger.error(f"Invalid cron expression: {scheduled_task.cron_expression} - {e}")
                return None
        
        elif scheduled_task.schedule_type == ScheduleType.INTERVAL:
            if not scheduled_task.interval_seconds:
                return None
            
            base_time = scheduled_task.last_executed or now
            return base_time + timedelta(seconds=scheduled_task.interval_seconds)
        
        return None
    
    async def _scheduler_loop(self):
        """Main scheduler loop that runs scheduled tasks"""
        while True:
            try:
                now = datetime.utcnow()
                
                # Find tasks ready for execution
                ready_tasks = []
                for task in self.scheduled_tasks.values():
                    if (task.status == TaskStatus.SCHEDULED and 
                        task.next_execution and 
                        task.next_execution <= now):
                        ready_tasks.append(task)
                
                # Execute ready tasks
                for task in ready_tasks:
                    if (task.max_executions is None or 
                        task.execution_count < task.max_executions):
                        asyncio.create_task(self._execute_scheduled_task(task))
                
                # Check reminders
                await self._check_reminders()
                
                # Sleep for a short time before next check
                await asyncio.sleep(10)  # Check every 10 seconds
                
            except Exception as e:
                self.logger.error(f"Error in scheduler loop: {e}")
                await asyncio.sleep(30)  # Wait longer on error
    
    async def _execute_scheduled_task(self, scheduled_task: ScheduledTask):
        """Execute a scheduled task"""
        scheduled_task.status = TaskStatus.RUNNING
        scheduled_task.last_executed = datetime.utcnow()
        
        self.logger.info(f"Executing scheduled task: {scheduled_task.name}")
        
        try:
            # Get target agent
            agent = self.agent_registry.get(scheduled_task.target_agent)
            if not agent:
                raise Exception(f"Agent {scheduled_task.target_agent} not found")
            
            # Create task for execution
            task = AgentTask(
                task_id=f"scheduled_{scheduled_task.task_id}_{scheduled_task.execution_count}",
                task_type=scheduled_task.target_task_type,
                payload=scheduled_task.payload,
                priority=TaskPriority.NORMAL
            )
            
            # Execute task
            result = await agent.execute_task(task)
            
            if result.success:
                scheduled_task.execution_count += 1
                scheduled_task.current_retries = 0
                scheduled_task.last_error = None
                
                # Calculate next execution for recurring tasks
                if scheduled_task.schedule_type != ScheduleType.ONE_TIME:
                    scheduled_task.next_execution = self._calculate_next_execution(scheduled_task)
                    if scheduled_task.next_execution:
                        scheduled_task.status = TaskStatus.SCHEDULED
                    else:
                        scheduled_task.status = TaskStatus.COMPLETED
                else:
                    scheduled_task.status = TaskStatus.COMPLETED
                
                self.logger.info(f"Task {scheduled_task.name} executed successfully")
                
            else:
                # Handle failure with retry logic
                await self._handle_task_failure(scheduled_task, result.error_message)
                
        except Exception as e:
            await self._handle_task_failure(scheduled_task, str(e))
    
    async def _handle_task_failure(self, scheduled_task: ScheduledTask, error_message: str):
        """Handle task execution failure with retry logic"""
        scheduled_task.last_error = error_message
        scheduled_task.current_retries += 1
        
        self.logger.error(f"Task {scheduled_task.name} failed: {error_message}")
        
        if scheduled_task.current_retries < scheduled_task.retry_count:
            # Schedule retry with exponential backoff
            retry_delay = scheduled_task.retry_delay_seconds * (2 ** (scheduled_task.current_retries - 1))
            scheduled_task.next_execution = datetime.utcnow() + timedelta(seconds=retry_delay)
            scheduled_task.status = TaskStatus.SCHEDULED
            
            self.logger.info(f"Scheduling retry {scheduled_task.current_retries} for task {scheduled_task.name} in {retry_delay} seconds")
        else:
            # Max retries reached
            scheduled_task.status = TaskStatus.FAILED
            self.logger.error(f"Task {scheduled_task.name} failed permanently after {scheduled_task.retry_count} retries")
    
    async def _cancel_task(self, payload: Dict[str, Any]) -> AgentResult:
        """Cancel a scheduled task"""
        task_id = payload.get("task_id")
        
        if task_id in self.scheduled_tasks:
            task = self.scheduled_tasks[task_id]
            task.status = TaskStatus.CANCELLED
            
            return AgentResult(
                success=True,
                data={"task_id": task_id, "message": "Task cancelled"},
                confidence=1.0,
                processing_time=0.0
            )
        else:
            return AgentResult(
                success=False,
                data={},
                confidence=0.0,
                processing_time=0.0,
                error_message=f"Task {task_id} not found"
            )
    
    async def _pause_task(self, payload: Dict[str, Any]) -> AgentResult:
        """Pause a scheduled task"""
        task_id = payload.get("task_id")
        
        if task_id in self.scheduled_tasks:
            task = self.scheduled_tasks[task_id]
            if task.status == TaskStatus.SCHEDULED:
                task.status = TaskStatus.PAUSED
                
                return AgentResult(
                    success=True,
                    data={"task_id": task_id, "message": "Task paused"},
                    confidence=1.0,
                    processing_time=0.0
                )
            else:
                return AgentResult(
                    success=False,
                    data={},
                    confidence=0.0,
                    processing_time=0.0,
                    error_message=f"Task {task_id} is not in scheduled state"
                )
        else:
            return AgentResult(
                success=False,
                data={},
                confidence=0.0,
                processing_time=0.0,
                error_message=f"Task {task_id} not found"
            )
    
    async def _resume_task(self, payload: Dict[str, Any]) -> AgentResult:
        """Resume a paused task"""
        task_id = payload.get("task_id")
        
        if task_id in self.scheduled_tasks:
            task = self.scheduled_tasks[task_id]
            if task.status == TaskStatus.PAUSED:
                task.status = TaskStatus.SCHEDULED
                # Recalculate next execution
                task.next_execution = self._calculate_next_execution(task)
                
                return AgentResult(
                    success=True,
                    data={
                        "task_id": task_id,
                        "next_execution": task.next_execution.isoformat() if task.next_execution else None,
                        "message": "Task resumed"
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
                    error_message=f"Task {task_id} is not paused"
                )
        else:
            return AgentResult(
                success=False,
                data={},
                confidence=0.0,
                processing_time=0.0,
                error_message=f"Task {task_id} not found"
            )
    
    async def _get_scheduled_tasks(self, payload: Dict[str, Any]) -> AgentResult:
        """Get scheduled tasks with optional filtering"""
        user_id = payload.get("user_id")
        status_filter = payload.get("status")
        tag_filter = payload.get("tags")
        
        filtered_tasks = []
        
        for task in self.scheduled_tasks.values():
            # Apply filters
            if user_id and task.user_id != user_id:
                continue
            if status_filter and task.status.value != status_filter:
                continue
            if tag_filter and not any(tag in task.tags for tag in tag_filter):
                continue
            
            task_data = {
                "task_id": task.task_id,
                "name": task.name,
                "description": task.description,
                "status": task.status.value,
                "schedule_type": task.schedule_type.value,
                "next_execution": task.next_execution.isoformat() if task.next_execution else None,
                "last_executed": task.last_executed.isoformat() if task.last_executed else None,
                "execution_count": task.execution_count,
                "tags": task.tags
            }
            
            filtered_tasks.append(task_data)
        
        return AgentResult(
            success=True,
            data={"tasks": filtered_tasks, "count": len(filtered_tasks)},
            confidence=1.0,
            processing_time=0.0
        )
    
    async def _create_reminder(self, payload: Dict[str, Any]) -> AgentResult:
        """Create a reminder for an email or task"""
        try:
            reminder_data = payload.get("reminder_data", {})
            
            reminder = ReminderTask(
                reminder_id=reminder_data.get("reminder_id", str(uuid.uuid4())),
                email_id=reminder_data["email_id"],
                reminder_type=reminder_data.get("reminder_type", "custom"),
                reminder_time=self._parse_datetime(reminder_data["reminder_time"]),
                message=reminder_data["message"],
                user_id=reminder_data["user_id"]
            )
            
            if not reminder.reminder_time:
                return AgentResult(
                    success=False,
                    data={},
                    confidence=0.0,
                    processing_time=0.0,
                    error_message="Invalid reminder time"
                )
            
            self.reminders[reminder.reminder_id] = reminder
            
            self.logger.info(f"Created reminder {reminder.reminder_id} for email {reminder.email_id}")
            
            return AgentResult(
                success=True,
                data={
                    "reminder_id": reminder.reminder_id,
                    "reminder_time": reminder.reminder_time.isoformat(),
                    "message": "Reminder created"
                },
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
    
    async def _check_reminders(self):
        """Check for due reminders and trigger notifications"""
        now = datetime.utcnow()
        
        for reminder in self.reminders.values():
            if (not reminder.completed and 
                reminder.reminder_time <= now and
                (not reminder.snoozed_until or reminder.snoozed_until <= now)):
                
                # Trigger notification through notification agent
                notification_payload = {
                    "type": "deadline_reminder",
                    "title": "Email Reminder",
                    "message": reminder.message,
                    "priority": "normal",
                    "channels": ["in_app", "desktop"],
                    "user_id": reminder.user_id,
                    "metadata": {
                        "reminder_id": reminder.reminder_id,
                        "email_id": reminder.email_id,
                        "reminder_type": reminder.reminder_type
                    }
                }
                
                # This would typically be sent to the notification agent
                self.logger.info(f"Reminder due: {reminder.message}")
                
                # Mark as completed for one-time reminders
                if reminder.reminder_type != "recurring":
                    reminder.completed = True
    
    async def _snooze_reminder(self, payload: Dict[str, Any]) -> AgentResult:
        """Snooze a reminder for a specified duration"""
        reminder_id = payload.get("reminder_id")
        snooze_minutes = payload.get("snooze_minutes", 15)
        
        if reminder_id in self.reminders:
            reminder = self.reminders[reminder_id]
            reminder.snoozed_until = datetime.utcnow() + timedelta(minutes=snooze_minutes)
            reminder.snooze_count += 1
            
            return AgentResult(
                success=True,
                data={
                    "reminder_id": reminder_id,
                    "snoozed_until": reminder.snoozed_until.isoformat(),
                    "message": f"Reminder snoozed for {snooze_minutes} minutes"
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
                error_message=f"Reminder {reminder_id} not found"
            )
    
    async def _get_reminders(self, payload: Dict[str, Any]) -> AgentResult:
        """Get reminders for a user"""
        user_id = payload.get("user_id")
        include_completed = payload.get("include_completed", False)
        
        filtered_reminders = []
        
        for reminder in self.reminders.values():
            if user_id and reminder.user_id != user_id:
                continue
            if not include_completed and reminder.completed:
                continue
            
            reminder_data = {
                "reminder_id": reminder.reminder_id,
                "email_id": reminder.email_id,
                "reminder_type": reminder.reminder_type,
                "message": reminder.message,
                "reminder_time": reminder.reminder_time.isoformat(),
                "completed": reminder.completed,
                "snoozed_until": reminder.snoozed_until.isoformat() if reminder.snoozed_until else None,
                "snooze_count": reminder.snooze_count
            }
            
            filtered_reminders.append(reminder_data)
        
        return AgentResult(
            success=True,
            data={"reminders": filtered_reminders, "count": len(filtered_reminders)},
            confidence=1.0,
            processing_time=0.0
        )
    
    async def _schedule_followup(self, payload: Dict[str, Any]) -> AgentResult:
        """Schedule a follow-up reminder for an email"""
        email_id = payload.get("email_id")
        user_id = payload.get("user_id")
        followup_hours = payload.get("followup_hours", 24)
        custom_message = payload.get("message")
        
        if not email_id or not user_id:
            return AgentResult(
                success=False,
                data={},
                confidence=0.0,
                processing_time=0.0,
                error_message="email_id and user_id are required"
            )
        
        # Calculate follow-up time
        followup_time = datetime.utcnow() + timedelta(hours=followup_hours)
        
        # Create reminder
        reminder = ReminderTask(
            reminder_id=str(uuid.uuid4()),
            email_id=email_id,
            reminder_type="followup",
            reminder_time=followup_time,
            message=custom_message or f"Follow up on email: {email_id}",
            user_id=user_id
        )
        
        self.reminders[reminder.reminder_id] = reminder
        
        return AgentResult(
            success=True,
            data={
                "reminder_id": reminder.reminder_id,
                "followup_time": followup_time.isoformat(),
                "message": "Follow-up reminder scheduled"
            },
            confidence=1.0,
            processing_time=0.0
        )
    
    async def shutdown(self):
        """Graceful shutdown of the scheduling agent"""
        self.logger.info("Shutting down scheduling agent...")
        
        # Cancel the scheduler task
        if hasattr(self, '_scheduler_task'):
            self._scheduler_task.cancel()
            try:
                await self._scheduler_task
            except asyncio.CancelledError:
                pass
        
        # Cancel any running tasks
        for task in self.running_tasks.values():
            task.cancel()
        
        await super().shutdown()