"""
Base Scrum Agent
Foundation for all Scrum-based agents in the Minicon eG system
"""

from typing import Dict, Any, List, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import asyncio
import logging
from abc import abstractmethod

from ..base_agent import BaseAgent, AgentTask, AgentResult, TaskPriority


class SprintPhase(Enum):
    PLANNING = "planning"
    EXECUTION = "execution"
    REVIEW = "review"
    RETROSPECTIVE = "retrospective"
    CLOSED = "closed"


class StoryStatus(Enum):
    BACKLOG = "backlog"
    READY = "ready"
    IN_PROGRESS = "in_progress"
    IN_REVIEW = "in_review"
    TESTING = "testing"
    DONE = "done"
    BLOCKED = "blocked"


class StoryPriority(Enum):
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4
    TRIVIAL = 5


@dataclass
class UserStory:
    """Represents a user story in the Scrum framework"""
    story_id: str
    title: str
    description: str
    acceptance_criteria: List[str]
    story_points: Optional[int] = None
    priority: StoryPriority = StoryPriority.MEDIUM
    status: StoryStatus = StoryStatus.BACKLOG
    assigned_to: Optional[str] = None
    sprint_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    blocked_reason: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    subtasks: List[str] = field(default_factory=list)
    
    def update_status(self, new_status: StoryStatus):
        """Update story status with timestamp"""
        self.status = new_status
        self.updated_at = datetime.utcnow()
        if new_status == StoryStatus.DONE:
            self.completed_at = datetime.utcnow()


@dataclass
class Sprint:
    """Represents a Sprint in the Scrum framework"""
    sprint_id: str
    name: str
    goal: str
    start_date: datetime
    end_date: datetime
    phase: SprintPhase = SprintPhase.PLANNING
    velocity: Optional[float] = None
    committed_points: int = 0
    completed_points: int = 0
    stories: List[str] = field(default_factory=list)
    team_members: List[str] = field(default_factory=list)
    daily_standups: List[Dict[str, Any]] = field(default_factory=list)
    impediments: List[Dict[str, Any]] = field(default_factory=list)
    retrospective_items: List[Dict[str, Any]] = field(default_factory=list)
    
    @property
    def duration_days(self) -> int:
        """Calculate sprint duration in days"""
        return (self.end_date - self.start_date).days
    
    @property
    def progress_percentage(self) -> float:
        """Calculate sprint progress percentage"""
        if self.committed_points == 0:
            return 0.0
        return (self.completed_points / self.committed_points) * 100


@dataclass
class TeamMember:
    """Represents a team member in the Scrum team"""
    member_id: str
    name: str
    email: str
    skills: Set[str]
    capacity_hours_per_sprint: float
    current_sprint_availability: float = 1.0  # 0.0 to 1.0
    assigned_stories: List[str] = field(default_factory=list)
    velocity_history: List[float] = field(default_factory=list)
    specializations: List[str] = field(default_factory=list)
    
    @property
    def average_velocity(self) -> float:
        """Calculate average velocity over historical sprints"""
        if not self.velocity_history:
            return 0.0
        return sum(self.velocity_history) / len(self.velocity_history)


class BaseScrumAgent(BaseAgent):
    """
    Base class for all Scrum-based agents
    
    Provides common functionality for Scrum processes including:
    - Sprint management
    - Story tracking
    - Team collaboration
    - Metrics collection
    - Integration with other Scrum agents
    """
    
    def __init__(self, agent_name: str, config: Dict[str, Any] = None):
        super().__init__(agent_name, config)
        
        # Scrum-specific attributes
        self.current_sprint: Optional[Sprint] = None
        self.sprints: Dict[str, Sprint] = {}
        self.stories: Dict[str, UserStory] = {}
        self.team_members: Dict[str, TeamMember] = {}
        self.product_backlog: List[str] = []  # Story IDs in priority order
        
        # Inter-agent communication
        self.scrum_agents: Dict[str, 'BaseScrumAgent'] = {}
        self.event_subscribers: Dict[str, List[callable]] = {}
        
        # Metrics and analytics
        self.sprint_metrics: Dict[str, Dict[str, Any]] = {}
        self.team_metrics: Dict[str, Dict[str, Any]] = {}
        
        self._setup_scrum_logging()
    
    def _setup_scrum_logging(self):
        """Setup Scrum-specific logging"""
        self.scrum_logger = logging.getLogger(f"minicon.scrum.{self.agent_name}")
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            f'%(asctime)s - {self.agent_name} [SCRUM] - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.scrum_logger.addHandler(handler)
        self.scrum_logger.setLevel(logging.INFO)
    
    def register_scrum_agent(self, agent_name: str, agent: 'BaseScrumAgent'):
        """Register another Scrum agent for collaboration"""
        self.scrum_agents[agent_name] = agent
        self.scrum_logger.info(f"Registered Scrum agent: {agent_name}")
    
    def subscribe_to_event(self, event_type: str, callback: callable):
        """Subscribe to Scrum events"""
        if event_type not in self.event_subscribers:
            self.event_subscribers[event_type] = []
        self.event_subscribers[event_type].append(callback)
    
    async def publish_event(self, event_type: str, event_data: Dict[str, Any]):
        """Publish a Scrum event to subscribers"""
        if event_type in self.event_subscribers:
            for callback in self.event_subscribers[event_type]:
                try:
                    await callback(event_data)
                except Exception as e:
                    self.scrum_logger.error(f"Error in event callback: {e}")
    
    # Sprint Management
    
    def create_sprint(self, sprint_data: Dict[str, Any]) -> Sprint:
        """Create a new sprint"""
        sprint = Sprint(
            sprint_id=sprint_data["sprint_id"],
            name=sprint_data["name"],
            goal=sprint_data["goal"],
            start_date=sprint_data["start_date"],
            end_date=sprint_data["end_date"],
            team_members=sprint_data.get("team_members", [])
        )
        
        self.sprints[sprint.sprint_id] = sprint
        self.scrum_logger.info(f"Created sprint: {sprint.name}")
        
        return sprint
    
    def start_sprint(self, sprint_id: str) -> bool:
        """Start a sprint"""
        if sprint_id not in self.sprints:
            return False
        
        sprint = self.sprints[sprint_id]
        sprint.phase = SprintPhase.EXECUTION
        self.current_sprint = sprint
        
        self.scrum_logger.info(f"Started sprint: {sprint.name}")
        
        # Publish sprint started event
        asyncio.create_task(self.publish_event("sprint_started", {
            "sprint_id": sprint_id,
            "sprint_name": sprint.name,
            "team_members": sprint.team_members
        }))
        
        return True
    
    def end_sprint(self, sprint_id: str) -> bool:
        """End a sprint and move to review phase"""
        if sprint_id not in self.sprints:
            return False
        
        sprint = self.sprints[sprint_id]
        sprint.phase = SprintPhase.REVIEW
        
        # Calculate final metrics
        sprint.completed_points = sum(
            self.stories[story_id].story_points or 0
            for story_id in sprint.stories
            if self.stories[story_id].status == StoryStatus.DONE
        )
        
        self.scrum_logger.info(f"Ended sprint: {sprint.name}")
        
        return True
    
    # Story Management
    
    def create_story(self, story_data: Dict[str, Any]) -> UserStory:
        """Create a new user story"""
        story = UserStory(
            story_id=story_data["story_id"],
            title=story_data["title"],
            description=story_data["description"],
            acceptance_criteria=story_data.get("acceptance_criteria", []),
            story_points=story_data.get("story_points"),
            priority=StoryPriority(story_data.get("priority", StoryPriority.MEDIUM.value)),
            tags=story_data.get("tags", []),
            dependencies=story_data.get("dependencies", [])
        )
        
        self.stories[story.story_id] = story
        self.product_backlog.append(story.story_id)
        
        self.scrum_logger.info(f"Created story: {story.title}")
        
        return story
    
    def assign_story(self, story_id: str, member_id: str) -> bool:
        """Assign a story to a team member"""
        if story_id not in self.stories or member_id not in self.team_members:
            return False
        
        story = self.stories[story_id]
        member = self.team_members[member_id]
        
        story.assigned_to = member_id
        member.assigned_stories.append(story_id)
        story.update_status(StoryStatus.IN_PROGRESS)
        
        self.scrum_logger.info(f"Assigned story {story.title} to {member.name}")
        
        return True
    
    def update_story_status(self, story_id: str, new_status: StoryStatus, reason: Optional[str] = None) -> bool:
        """Update story status"""
        if story_id not in self.stories:
            return False
        
        story = self.stories[story_id]
        old_status = story.status
        story.update_status(new_status)
        
        if new_status == StoryStatus.BLOCKED:
            story.blocked_reason = reason
        
        self.scrum_logger.info(f"Updated story {story.title} from {old_status.value} to {new_status.value}")
        
        # Publish status change event
        asyncio.create_task(self.publish_event("story_status_changed", {
            "story_id": story_id,
            "old_status": old_status.value,
            "new_status": new_status.value,
            "reason": reason
        }))
        
        return True
    
    # Team Management
    
    def add_team_member(self, member_data: Dict[str, Any]) -> TeamMember:
        """Add a team member"""
        member = TeamMember(
            member_id=member_data["member_id"],
            name=member_data["name"],
            email=member_data["email"],
            skills=set(member_data.get("skills", [])),
            capacity_hours_per_sprint=member_data["capacity_hours_per_sprint"],
            specializations=member_data.get("specializations", [])
        )
        
        self.team_members[member.member_id] = member
        
        self.scrum_logger.info(f"Added team member: {member.name}")
        
        return member
    
    def get_team_capacity(self) -> Dict[str, float]:
        """Calculate team capacity for current sprint"""
        capacity = {}
        
        for member_id, member in self.team_members.items():
            available_hours = member.capacity_hours_per_sprint * member.current_sprint_availability
            capacity[member_id] = available_hours
        
        return capacity
    
    # Metrics and Analytics
    
    def calculate_sprint_velocity(self, sprint_id: str) -> float:
        """Calculate velocity for a specific sprint"""
        if sprint_id not in self.sprints:
            return 0.0
        
        sprint = self.sprints[sprint_id]
        completed_points = sum(
            self.stories[story_id].story_points or 0
            for story_id in sprint.stories
            if self.stories[story_id].status == StoryStatus.DONE
        )
        
        return completed_points
    
    def get_burndown_data(self, sprint_id: str) -> List[Dict[str, Any]]:
        """Get burndown chart data for a sprint"""
        if sprint_id not in self.sprints:
            return []
        
        sprint = self.sprints[sprint_id]
        burndown_data = []
        
        # This is a simplified version - in reality, you'd track daily progress
        total_days = sprint.duration_days
        points_per_day = sprint.committed_points / total_days if total_days > 0 else 0
        
        for day in range(total_days + 1):
            ideal_remaining = sprint.committed_points - (points_per_day * day)
            burndown_data.append({
                "day": day,
                "ideal_remaining": max(0, ideal_remaining),
                "actual_remaining": sprint.committed_points - sprint.completed_points  # Simplified
            })
        
        return burndown_data
    
    def get_team_velocity_trend(self) -> Dict[str, List[float]]:
        """Get velocity trend for each team member"""
        velocity_trend = {}
        
        for member_id, member in self.team_members.items():
            velocity_trend[member_id] = member.velocity_history[-5:]  # Last 5 sprints
        
        return velocity_trend
    
    # Abstract methods for specific agent implementations
    
    @abstractmethod
    async def handle_sprint_event(self, event_type: str, event_data: Dict[str, Any]) -> AgentResult:
        """Handle sprint-related events"""
        pass
    
    @abstractmethod
    async def collaborate_with_agent(self, agent_name: str, message: Dict[str, Any]) -> AgentResult:
        """Collaborate with another Scrum agent"""
        pass
    
    # Integration with base agent
    
    def get_supported_task_types(self) -> List[str]:
        """Return supported task types for Scrum operations"""
        return [
            "create_sprint",
            "start_sprint",
            "end_sprint",
            "create_story",
            "update_story",
            "assign_story",
            "add_team_member",
            "get_metrics",
            "handle_event",
            "collaborate"
        ]
    
    async def process_task(self, task: AgentTask) -> AgentResult:
        """Process Scrum-related tasks"""
        try:
            if task.task_type == "create_sprint":
                sprint = self.create_sprint(task.payload)
                return AgentResult(
                    success=True,
                    data={"sprint_id": sprint.sprint_id, "sprint": sprint.__dict__},
                    confidence=1.0,
                    processing_time=0.0
                )
            
            elif task.task_type == "create_story":
                story = self.create_story(task.payload)
                return AgentResult(
                    success=True,
                    data={"story_id": story.story_id, "story": story.__dict__},
                    confidence=1.0,
                    processing_time=0.0
                )
            
            elif task.task_type == "handle_event":
                return await self.handle_sprint_event(
                    task.payload["event_type"],
                    task.payload["event_data"]
                )
            
            elif task.task_type == "collaborate":
                return await self.collaborate_with_agent(
                    task.payload["agent_name"],
                    task.payload["message"]
                )
            
            else:
                return AgentResult(
                    success=False,
                    data={},
                    confidence=0.0,
                    processing_time=0.0,
                    error_message=f"Unsupported task type: {task.task_type}"
                )
                
        except Exception as e:
            return AgentResult(
                success=False,
                data={},
                confidence=0.0,
                processing_time=0.0,
                error_message=str(e)
            )