"""
Scrum Master Agent
Facilitator and process optimizer for Scrum teams
"""

from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, field
import asyncio
import statistics
from collections import defaultdict

from .base_scrum_agent import BaseScrumAgent, Sprint, SprintPhase, UserStory, StoryStatus
from ..base_agent import AgentTask, AgentResult


@dataclass
class Impediment:
    """Represents an impediment blocking team progress"""
    impediment_id: str
    description: str
    severity: str  # low, medium, high, critical
    affected_stories: List[str]
    affected_members: List[str]
    identified_date: datetime
    resolved_date: Optional[datetime] = None
    resolution: Optional[str] = None
    status: str = "open"  # open, in_progress, resolved


@dataclass
class TeamHealthMetrics:
    """Metrics for team health and performance"""
    velocity_trend: str  # increasing, stable, decreasing
    collaboration_score: float  # 0-100
    impediment_resolution_time: float  # average hours
    sprint_predictability: float  # 0-100
    team_happiness: float  # 0-100
    burnout_risk: float  # 0-100


@dataclass
class RetrospectiveInsight:
    """AI-generated insight from retrospective analysis"""
    insight_id: str
    category: str  # process, technical, team, communication
    description: str
    impact_score: float  # 0-100
    recommended_actions: List[str]
    related_patterns: List[str]
    confidence: float  # 0-1


class ScrumMasterAgent(BaseScrumAgent):
    """
    Scrum Master Agent - Facilitates Scrum processes and removes impediments
    
    Responsibilities:
    - Sprint planning and facilitation
    - Impediment detection and resolution
    - Team velocity tracking and forecasting
    - Retrospective analysis with AI insights
    - Cross-team coordination
    - Process optimization
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__("scrum_master", config)
        
        # Scrum Master specific data
        self.impediments: Dict[str, Impediment] = {}
        self.team_health_history: List[TeamHealthMetrics] = []
        self.retrospective_insights: Dict[str, List[RetrospectiveInsight]] = {}
        self.velocity_forecasts: Dict[str, float] = {}
        
        # Process optimization settings
        self.optimization_rules = self._load_optimization_rules()
        self.facilitation_patterns = self._load_facilitation_patterns()
        
        # Start background monitoring
        asyncio.create_task(self._monitor_team_health())
        asyncio.create_task(self._detect_impediments())
    
    def _load_optimization_rules(self) -> Dict[str, Any]:
        """Load process optimization rules"""
        return {
            "min_story_size": 1,
            "max_story_size": 13,
            "optimal_wip_limit": 3,
            "standup_time_limit": 15,  # minutes
            "retrospective_frequency": 2,  # weeks
            "velocity_buffer": 0.8,  # 80% of average velocity for planning
            "impediment_escalation_hours": 24
        }
    
    def _load_facilitation_patterns(self) -> Dict[str, List[str]]:
        """Load facilitation patterns and techniques"""
        return {
            "sprint_planning": [
                "story_mapping",
                "planning_poker",
                "velocity_based_commitment",
                "risk_assessment"
            ],
            "daily_standup": [
                "walking_the_board",
                "focus_on_blockers",
                "time_boxing",
                "parking_lot"
            ],
            "retrospective": [
                "start_stop_continue",
                "4_ls_technique",
                "sailboat_retrospective",
                "timeline_retrospective"
            ]
        }
    
    async def handle_sprint_event(self, event_type: str, event_data: Dict[str, Any]) -> AgentResult:
        """Handle sprint-related events"""
        try:
            if event_type == "facilitate_planning":
                return await self._facilitate_sprint_planning(event_data)
            elif event_type == "facilitate_daily":
                return await self._facilitate_daily_standup(event_data)
            elif event_type == "facilitate_retrospective":
                return await self._facilitate_retrospective(event_data)
            elif event_type == "impediment_reported":
                return await self._handle_impediment(event_data)
            elif event_type == "velocity_forecast":
                return await self._forecast_velocity(event_data)
            else:
                return AgentResult(
                    success=False,
                    data={},
                    confidence=0.0,
                    processing_time=0.0,
                    error_message=f"Unknown event type: {event_type}"
                )
        except Exception as e:
            return AgentResult(
                success=False,
                data={},
                confidence=0.0,
                processing_time=0.0,
                error_message=str(e)
            )
    
    async def collaborate_with_agent(self, agent_name: str, message: Dict[str, Any]) -> AgentResult:
        """Collaborate with other Scrum agents"""
        try:
            if agent_name == "product_owner":
                return await self._collaborate_with_po(message)
            elif agent_name.startswith("dev_team"):
                return await self._collaborate_with_dev(message)
            else:
                return AgentResult(
                    success=True,
                    data={"response": "Message received", "agent": agent_name},
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
    
    async def _facilitate_sprint_planning(self, planning_data: Dict[str, Any]) -> AgentResult:
        """Facilitate sprint planning session"""
        sprint_id = planning_data["sprint_id"]
        available_capacity = planning_data.get("team_capacity", {})
        
        if sprint_id not in self.sprints:
            return AgentResult(
                success=False,
                data={},
                confidence=0.0,
                processing_time=0.0,
                error_message=f"Sprint {sprint_id} not found"
            )
        
        sprint = self.sprints[sprint_id]
        
        # Calculate recommended velocity based on historical data
        recommended_velocity = self._calculate_recommended_velocity(sprint)
        
        # Analyze story dependencies and risks
        story_analysis = self._analyze_stories_for_sprint(planning_data.get("candidate_stories", []))
        
        # Generate planning recommendations
        recommendations = {
            "recommended_velocity": recommended_velocity,
            "suggested_stories": story_analysis["prioritized_stories"],
            "risk_assessment": story_analysis["risks"],
            "dependency_warnings": story_analysis["dependencies"],
            "capacity_utilization": self._calculate_capacity_utilization(
                story_analysis["total_points"],
                recommended_velocity
            ),
            "facilitation_technique": self._select_facilitation_technique("sprint_planning")
        }
        
        # Update sprint with planning data
        sprint.phase = SprintPhase.PLANNING
        sprint.velocity = recommended_velocity
        
        self.scrum_logger.info(f"Facilitated sprint planning for {sprint.name}")
        
        return AgentResult(
            success=True,
            data=recommendations,
            confidence=0.85,
            processing_time=0.0
        )
    
    async def _facilitate_daily_standup(self, standup_data: Dict[str, Any]) -> AgentResult:
        """Facilitate daily standup meeting"""
        sprint_id = standup_data.get("sprint_id", self.current_sprint.sprint_id if self.current_sprint else None)
        
        if not sprint_id or sprint_id not in self.sprints:
            return AgentResult(
                success=False,
                data={},
                confidence=0.0,
                processing_time=0.0,
                error_message="No active sprint for standup"
            )
        
        sprint = self.sprints[sprint_id]
        
        # Collect status updates from team members
        status_updates = standup_data.get("member_updates", {})
        
        # Detect blockers and impediments
        impediments_detected = self._detect_impediments_from_updates(status_updates)
        
        # Analyze sprint health
        sprint_health = self._analyze_sprint_health(sprint)
        
        # Generate standup summary and action items
        standup_summary = {
            "date": datetime.utcnow().isoformat(),
            "sprint_progress": sprint.progress_percentage,
            "impediments_identified": len(impediments_detected),
            "at_risk_stories": sprint_health["at_risk_stories"],
            "focus_areas": sprint_health["focus_areas"],
            "facilitation_notes": self._generate_facilitation_notes(status_updates),
            "parking_lot_items": self._identify_parking_lot_items(status_updates)
        }
        
        # Record standup in sprint data
        sprint.daily_standups.append(standup_summary)
        
        # Create impediments if detected
        for imp_data in impediments_detected:
            await self._create_impediment(imp_data)
        
        return AgentResult(
            success=True,
            data=standup_summary,
            confidence=0.9,
            processing_time=0.0
        )
    
    async def _facilitate_retrospective(self, retro_data: Dict[str, Any]) -> AgentResult:
        """Facilitate sprint retrospective with AI insights"""
        sprint_id = retro_data["sprint_id"]
        
        if sprint_id not in self.sprints:
            return AgentResult(
                success=False,
                data={},
                confidence=0.0,
                processing_time=0.0,
                error_message=f"Sprint {sprint_id} not found"
            )
        
        sprint = self.sprints[sprint_id]
        
        # Collect retrospective feedback
        feedback = retro_data.get("team_feedback", {})
        
        # Analyze sprint performance
        performance_analysis = self._analyze_sprint_performance(sprint)
        
        # Generate AI insights
        ai_insights = await self._generate_retrospective_insights(sprint, feedback)
        
        # Identify improvement actions
        improvement_actions = self._identify_improvement_actions(ai_insights, feedback)
        
        # Update sprint phase
        sprint.phase = SprintPhase.RETROSPECTIVE
        
        # Store insights for future reference
        self.retrospective_insights[sprint_id] = ai_insights
        
        retrospective_summary = {
            "sprint_id": sprint_id,
            "performance_metrics": performance_analysis,
            "ai_insights": [insight.__dict__ for insight in ai_insights],
            "improvement_actions": improvement_actions,
            "team_health_score": self._calculate_team_health_score(sprint, feedback),
            "facilitation_technique": self._select_facilitation_technique("retrospective")
        }
        
        # Record retrospective items
        sprint.retrospective_items.append(retrospective_summary)
        
        return AgentResult(
            success=True,
            data=retrospective_summary,
            confidence=0.85,
            processing_time=0.0
        )
    
    async def _handle_impediment(self, impediment_data: Dict[str, Any]) -> AgentResult:
        """Handle reported impediment"""
        impediment = Impediment(
            impediment_id=f"imp_{datetime.utcnow().timestamp()}",
            description=impediment_data["description"],
            severity=impediment_data.get("severity", "medium"),
            affected_stories=impediment_data.get("affected_stories", []),
            affected_members=impediment_data.get("affected_members", []),
            identified_date=datetime.utcnow()
        )
        
        self.impediments[impediment.impediment_id] = impediment
        
        # Analyze impediment impact
        impact_analysis = self._analyze_impediment_impact(impediment)
        
        # Generate resolution strategies
        resolution_strategies = await self._generate_resolution_strategies(impediment)
        
        # Escalate if necessary
        if impediment.severity in ["high", "critical"]:
            await self._escalate_impediment(impediment)
        
        return AgentResult(
            success=True,
            data={
                "impediment_id": impediment.impediment_id,
                "impact_analysis": impact_analysis,
                "resolution_strategies": resolution_strategies,
                "escalated": impediment.severity in ["high", "critical"]
            },
            confidence=0.9,
            processing_time=0.0
        )
    
    async def _forecast_velocity(self, forecast_data: Dict[str, Any]) -> AgentResult:
        """Forecast team velocity for future sprints"""
        team_id = forecast_data.get("team_id", "default")
        sprints_ahead = forecast_data.get("sprints_ahead", 3)
        
        # Gather historical velocity data
        historical_velocities = self._get_historical_velocities(team_id)
        
        if len(historical_velocities) < 3:
            return AgentResult(
                success=False,
                data={},
                confidence=0.0,
                processing_time=0.0,
                error_message="Insufficient historical data for forecasting"
            )
        
        # Apply forecasting algorithm
        forecasts = []
        for i in range(sprints_ahead):
            # Simple weighted moving average with trend adjustment
            forecast = self._calculate_velocity_forecast(historical_velocities, i + 1)
            forecasts.append({
                "sprint_offset": i + 1,
                "predicted_velocity": forecast["velocity"],
                "confidence_interval": forecast["confidence_interval"],
                "factors": forecast["factors"]
            })
        
        return AgentResult(
            success=True,
            data={
                "team_id": team_id,
                "forecasts": forecasts,
                "historical_average": statistics.mean(historical_velocities),
                "trend": self._identify_velocity_trend(historical_velocities)
            },
            confidence=0.8,
            processing_time=0.0
        )
    
    # Helper methods
    
    def _calculate_recommended_velocity(self, sprint: Sprint) -> float:
        """Calculate recommended velocity for sprint planning"""
        # Get historical velocities
        historical_velocities = []
        for sprint_id, s in self.sprints.items():
            if s.phase == SprintPhase.CLOSED and s.velocity:
                historical_velocities.append(s.velocity)
        
        if not historical_velocities:
            # Default to team capacity estimate
            return sum(self.get_team_capacity().values()) * 0.6
        
        # Use rolling average with buffer
        avg_velocity = statistics.mean(historical_velocities[-3:])
        return avg_velocity * self.optimization_rules["velocity_buffer"]
    
    def _analyze_stories_for_sprint(self, story_ids: List[str]) -> Dict[str, Any]:
        """Analyze stories for sprint planning"""
        risks = []
        dependencies = []
        prioritized_stories = []
        total_points = 0
        
        for story_id in story_ids:
            if story_id not in self.stories:
                continue
            
            story = self.stories[story_id]
            
            # Check story size
            if story.story_points:
                if story.story_points > self.optimization_rules["max_story_size"]:
                    risks.append(f"Story {story.title} is too large ({story.story_points} points)")
                total_points += story.story_points
            
            # Check dependencies
            if story.dependencies:
                for dep_id in story.dependencies:
                    if dep_id in self.stories and self.stories[dep_id].status != StoryStatus.DONE:
                        dependencies.append(f"Story {story.title} depends on incomplete story {dep_id}")
            
            prioritized_stories.append({
                "story_id": story_id,
                "priority_score": self._calculate_story_priority_score(story),
                "risk_level": "high" if len(story.dependencies) > 2 else "medium" if story.dependencies else "low"
            })
        
        # Sort by priority score
        prioritized_stories.sort(key=lambda x: x["priority_score"], reverse=True)
        
        return {
            "prioritized_stories": prioritized_stories,
            "risks": risks,
            "dependencies": dependencies,
            "total_points": total_points
        }
    
    def _calculate_story_priority_score(self, story: UserStory) -> float:
        """Calculate priority score for a story"""
        base_score = 6 - story.priority.value  # Higher priority = higher score
        
        # Adjust for dependencies
        dependency_penalty = len(story.dependencies) * 0.5
        
        # Adjust for age
        age_days = (datetime.utcnow() - story.created_at).days
        age_bonus = min(age_days * 0.1, 2.0)
        
        return base_score - dependency_penalty + age_bonus
    
    def _calculate_capacity_utilization(self, committed_points: float, capacity: float) -> float:
        """Calculate capacity utilization percentage"""
        if capacity == 0:
            return 0.0
        return (committed_points / capacity) * 100
    
    def _select_facilitation_technique(self, meeting_type: str) -> str:
        """Select appropriate facilitation technique"""
        techniques = self.facilitation_patterns.get(meeting_type, [])
        if not techniques:
            return "standard_facilitation"
        
        # Rotate through techniques for variety
        # In real implementation, this would be more sophisticated
        return techniques[0]
    
    def _detect_impediments_from_updates(self, updates: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Detect impediments from standup updates"""
        impediments = []
        
        blocker_keywords = ["blocked", "stuck", "waiting", "impediment", "can't", "unable"]
        
        for member_id, update in updates.items():
            blockers = update.get("blockers", [])
            yesterday = update.get("yesterday", "")
            
            # Direct blockers
            for blocker in blockers:
                impediments.append({
                    "description": blocker,
                    "affected_members": [member_id],
                    "severity": "high"
                })
            
            # Detect from text
            for keyword in blocker_keywords:
                if keyword in yesterday.lower():
                    impediments.append({
                        "description": f"Potential blocker detected in update: {yesterday[:100]}",
                        "affected_members": [member_id],
                        "severity": "medium"
                    })
                    break
        
        return impediments
    
    def _analyze_sprint_health(self, sprint: Sprint) -> Dict[str, Any]:
        """Analyze current sprint health"""
        at_risk_stories = []
        focus_areas = []
        
        # Check sprint progress vs timeline
        days_elapsed = (datetime.utcnow() - sprint.start_date).days
        expected_progress = (days_elapsed / sprint.duration_days) * 100 if sprint.duration_days > 0 else 0
        actual_progress = sprint.progress_percentage
        
        if actual_progress < expected_progress - 10:
            focus_areas.append("Sprint is behind schedule")
        
        # Check blocked stories
        for story_id in sprint.stories:
            if story_id in self.stories:
                story = self.stories[story_id]
                if story.status == StoryStatus.BLOCKED:
                    at_risk_stories.append(story_id)
                elif story.status == StoryStatus.IN_PROGRESS and days_elapsed > 3:
                    # Story in progress too long
                    at_risk_stories.append(story_id)
        
        # Check impediments
        open_impediments = sum(1 for imp in self.impediments.values() if imp.status == "open")
        if open_impediments > 2:
            focus_areas.append(f"{open_impediments} open impediments need resolution")
        
        return {
            "at_risk_stories": at_risk_stories,
            "focus_areas": focus_areas,
            "health_score": max(0, 100 - len(at_risk_stories) * 10 - len(focus_areas) * 15)
        }
    
    def _generate_facilitation_notes(self, updates: Dict[str, Any]) -> List[str]:
        """Generate facilitation notes from standup updates"""
        notes = []
        
        # Check for common patterns
        if len(updates) > 5:
            notes.append("Consider splitting into smaller groups for more focused discussion")
        
        # Check for missing updates
        missing_updates = []
        for member_id in self.team_members:
            if member_id not in updates:
                missing_updates.append(self.team_members[member_id].name)
        
        if missing_updates:
            notes.append(f"Missing updates from: {', '.join(missing_updates)}")
        
        return notes
    
    def _identify_parking_lot_items(self, updates: Dict[str, Any]) -> List[str]:
        """Identify items for parking lot discussion"""
        parking_lot = []
        
        discussion_keywords = ["discuss", "meeting", "clarify", "question", "design"]
        
        for member_id, update in updates.items():
            today = update.get("today", "")
            
            for keyword in discussion_keywords:
                if keyword in today.lower():
                    parking_lot.append(f"{self.team_members[member_id].name}: {today[:100]}")
                    break
        
        return parking_lot
    
    async def _create_impediment(self, impediment_data: Dict[str, Any]):
        """Create and track an impediment"""
        impediment = Impediment(
            impediment_id=f"imp_{datetime.utcnow().timestamp()}",
            description=impediment_data["description"],
            severity=impediment_data.get("severity", "medium"),
            affected_stories=impediment_data.get("affected_stories", []),
            affected_members=impediment_data.get("affected_members", []),
            identified_date=datetime.utcnow()
        )
        
        self.impediments[impediment.impediment_id] = impediment
        
        # Update affected stories
        for story_id in impediment.affected_stories:
            if story_id in self.stories:
                self.update_story_status(story_id, StoryStatus.BLOCKED, impediment.description)
        
        # Publish impediment event
        await self.publish_event("impediment_created", {
            "impediment": impediment.__dict__,
            "sprint_id": self.current_sprint.sprint_id if self.current_sprint else None
        })
    
    def _analyze_sprint_performance(self, sprint: Sprint) -> Dict[str, Any]:
        """Analyze sprint performance metrics"""
        # Calculate various metrics
        commitment_accuracy = (sprint.completed_points / sprint.committed_points * 100) if sprint.committed_points > 0 else 0
        
        # Story completion rate
        completed_stories = sum(1 for sid in sprint.stories if self.stories[sid].status == StoryStatus.DONE)
        total_stories = len(sprint.stories)
        completion_rate = (completed_stories / total_stories * 100) if total_stories > 0 else 0
        
        # Impediment metrics
        sprint_impediments = [imp for imp in self.impediments.values() 
                            if sprint.start_date <= imp.identified_date <= sprint.end_date]
        avg_resolution_time = self._calculate_avg_impediment_resolution_time(sprint_impediments)
        
        return {
            "velocity_achieved": sprint.completed_points,
            "commitment_accuracy": commitment_accuracy,
            "story_completion_rate": completion_rate,
            "impediments_encountered": len(sprint_impediments),
            "avg_impediment_resolution_hours": avg_resolution_time,
            "team_collaboration_score": self._calculate_collaboration_score(sprint)
        }
    
    def _calculate_avg_impediment_resolution_time(self, impediments: List[Impediment]) -> float:
        """Calculate average impediment resolution time in hours"""
        resolution_times = []
        
        for imp in impediments:
            if imp.resolved_date:
                resolution_time = (imp.resolved_date - imp.identified_date).total_seconds() / 3600
                resolution_times.append(resolution_time)
        
        return statistics.mean(resolution_times) if resolution_times else 0.0
    
    def _calculate_collaboration_score(self, sprint: Sprint) -> float:
        """Calculate team collaboration score"""
        # Simplified calculation based on:
        # - Story handoffs
        # - Pair programming sessions
        # - Knowledge sharing
        # - Cross-functional work
        
        base_score = 70.0
        
        # Adjust based on impediments
        impediment_penalty = len(sprint.impediments) * 5
        
        # Adjust based on standup participation
        standup_bonus = min(len(sprint.daily_standups) * 2, 20)
        
        return max(0, min(100, base_score - impediment_penalty + standup_bonus))
    
    async def _generate_retrospective_insights(self, sprint: Sprint, feedback: Dict[str, Any]) -> List[RetrospectiveInsight]:
        """Generate AI-powered retrospective insights"""
        insights = []
        
        # Analyze velocity trends
        if self._identify_velocity_trend(self._get_historical_velocities()) == "decreasing":
            insights.append(RetrospectiveInsight(
                insight_id=f"insight_{datetime.utcnow().timestamp()}",
                category="process",
                description="Team velocity has been decreasing over the last 3 sprints",
                impact_score=75.0,
                recommended_actions=[
                    "Review story estimation practices",
                    "Identify and address technical debt",
                    "Check for team burnout indicators"
                ],
                related_patterns=["velocity_decline", "estimation_drift"],
                confidence=0.85
            ))
        
        # Analyze impediment patterns
        impediment_categories = defaultdict(int)
        for imp in self.impediments.values():
            if sprint.start_date <= imp.identified_date <= sprint.end_date:
                # Categorize impediment (simplified)
                if "technical" in imp.description.lower():
                    impediment_categories["technical"] += 1
                elif "communication" in imp.description.lower():
                    impediment_categories["communication"] += 1
                else:
                    impediment_categories["process"] += 1
        
        # Generate insights based on impediment patterns
        for category, count in impediment_categories.items():
            if count >= 3:
                insights.append(RetrospectiveInsight(
                    insight_id=f"insight_imp_{datetime.utcnow().timestamp()}",
                    category=category,
                    description=f"High frequency of {category} impediments detected ({count} occurrences)",
                    impact_score=60.0,
                    recommended_actions=self._get_impediment_recommendations(category),
                    related_patterns=[f"{category}_impediments"],
                    confidence=0.9
                ))
        
        # Analyze team feedback sentiment
        sentiment_insights = self._analyze_feedback_sentiment(feedback)
        insights.extend(sentiment_insights)
        
        return insights
    
    def _identify_improvement_actions(self, insights: List[RetrospectiveInsight], feedback: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify concrete improvement actions from insights"""
        actions = []
        
        # Convert high-impact insights to actions
        for insight in insights:
            if insight.impact_score >= 70:
                for recommendation in insight.recommended_actions[:2]:  # Top 2 recommendations
                    actions.append({
                        "action": recommendation,
                        "priority": "high" if insight.impact_score >= 80 else "medium",
                        "category": insight.category,
                        "assigned_to": "team",  # Would be more specific in real implementation
                        "due_date": (datetime.utcnow() + timedelta(days=14)).isoformat()
                    })
        
        # Add actions from direct feedback
        if "improvement_suggestions" in feedback:
            for suggestion in feedback["improvement_suggestions"]:
                actions.append({
                    "action": suggestion,
                    "priority": "medium",
                    "category": "team_suggested",
                    "assigned_to": "team",
                    "due_date": (datetime.utcnow() + timedelta(days=14)).isoformat()
                })
        
        return actions
    
    def _calculate_team_health_score(self, sprint: Sprint, feedback: Dict[str, Any]) -> float:
        """Calculate overall team health score"""
        scores = []
        
        # Sprint performance score
        performance_score = min(100, sprint.progress_percentage)
        scores.append(performance_score)
        
        # Impediment resolution score
        resolved_impediments = sum(1 for imp in self.impediments.values() 
                                 if imp.status == "resolved" and 
                                 sprint.start_date <= imp.identified_date <= sprint.end_date)
        total_impediments = sum(1 for imp in self.impediments.values() 
                              if sprint.start_date <= imp.identified_date <= sprint.end_date)
        resolution_score = (resolved_impediments / total_impediments * 100) if total_impediments > 0 else 100
        scores.append(resolution_score)
        
        # Team satisfaction from feedback
        satisfaction_score = feedback.get("team_satisfaction", 70)
        scores.append(satisfaction_score)
        
        # Collaboration score
        collaboration_score = self._calculate_collaboration_score(sprint)
        scores.append(collaboration_score)
        
        return statistics.mean(scores)
    
    async def _monitor_team_health(self):
        """Background task to monitor team health"""
        while True:
            try:
                if self.current_sprint:
                    # Calculate current team health metrics
                    health_metrics = TeamHealthMetrics(
                        velocity_trend=self._identify_velocity_trend(self._get_historical_velocities()),
                        collaboration_score=self._calculate_collaboration_score(self.current_sprint),
                        impediment_resolution_time=self._calculate_avg_impediment_resolution_time(
                            list(self.impediments.values())
                        ),
                        sprint_predictability=self._calculate_sprint_predictability(),
                        team_happiness=75.0,  # Would come from surveys/feedback
                        burnout_risk=self._calculate_burnout_risk()
                    )
                    
                    self.team_health_history.append(health_metrics)
                    
                    # Alert if health metrics are concerning
                    if health_metrics.burnout_risk > 70:
                        await self.publish_event("health_alert", {
                            "type": "burnout_risk",
                            "risk_level": health_metrics.burnout_risk,
                            "recommendations": ["Consider reducing sprint velocity", "Schedule team building activities"]
                        })
                
                await asyncio.sleep(3600)  # Check every hour
                
            except Exception as e:
                self.scrum_logger.error(f"Error in health monitoring: {e}")
                await asyncio.sleep(3600)
    
    async def _detect_impediments(self):
        """Background task to proactively detect impediments"""
        while True:
            try:
                if self.current_sprint:
                    # Check for stories stuck in progress
                    for story_id in self.current_sprint.stories:
                        if story_id in self.stories:
                            story = self.stories[story_id]
                            if story.status == StoryStatus.IN_PROGRESS:
                                # Check if stuck too long
                                if story.updated_at < datetime.utcnow() - timedelta(days=2):
                                    await self._create_impediment({
                                        "description": f"Story '{story.title}' has been in progress for >2 days",
                                        "severity": "medium",
                                        "affected_stories": [story_id],
                                        "affected_members": [story.assigned_to] if story.assigned_to else []
                                    })
                    
                    # Check for WIP limit violations
                    wip_by_member = defaultdict(int)
                    for story_id in self.current_sprint.stories:
                        if story_id in self.stories:
                            story = self.stories[story_id]
                            if story.status == StoryStatus.IN_PROGRESS and story.assigned_to:
                                wip_by_member[story.assigned_to] += 1
                    
                    for member_id, wip_count in wip_by_member.items():
                        if wip_count > self.optimization_rules["optimal_wip_limit"]:
                            await self._create_impediment({
                                "description": f"Team member {member_id} has {wip_count} stories in progress (WIP limit: {self.optimization_rules['optimal_wip_limit']})",
                                "severity": "medium",
                                "affected_members": [member_id]
                            })
                
                await asyncio.sleep(7200)  # Check every 2 hours
                
            except Exception as e:
                self.scrum_logger.error(f"Error in impediment detection: {e}")
                await asyncio.sleep(7200)
    
    def _get_historical_velocities(self, team_id: str = "default") -> List[float]:
        """Get historical velocity data"""
        velocities = []
        
        for sprint_id, sprint in self.sprints.items():
            if sprint.phase == SprintPhase.CLOSED and sprint.velocity:
                velocities.append(sprint.velocity)
        
        return velocities[-10:]  # Last 10 sprints
    
    def _calculate_velocity_forecast(self, historical_velocities: List[float], periods_ahead: int) -> Dict[str, Any]:
        """Calculate velocity forecast using weighted moving average"""
        if len(historical_velocities) < 3:
            return {"velocity": 0, "confidence_interval": [0, 0], "factors": []}
        
        # Weights for recent sprints (more recent = higher weight)
        weights = [0.5, 0.3, 0.2] if len(historical_velocities) >= 3 else [0.6, 0.4]
        recent_velocities = historical_velocities[-len(weights):]
        
        # Calculate weighted average
        weighted_sum = sum(v * w for v, w in zip(recent_velocities, weights))
        base_forecast = weighted_sum
        
        # Adjust for trend
        if len(historical_velocities) >= 3:
            trend = (historical_velocities[-1] - historical_velocities[-3]) / 2
            base_forecast += trend * periods_ahead * 0.5
        
        # Calculate confidence interval
        std_dev = statistics.stdev(historical_velocities) if len(historical_velocities) > 1 else 0
        confidence_interval = [
            max(0, base_forecast - 1.96 * std_dev),
            base_forecast + 1.96 * std_dev
        ]
        
        # Identify affecting factors
        factors = []
        if self._identify_velocity_trend(historical_velocities) == "decreasing":
            factors.append("declining_trend")
        if len(self.impediments) > 5:
            factors.append("high_impediment_count")
        
        return {
            "velocity": round(base_forecast, 1),
            "confidence_interval": [round(ci, 1) for ci in confidence_interval],
            "factors": factors
        }
    
    def _identify_velocity_trend(self, velocities: List[float]) -> str:
        """Identify velocity trend"""
        if len(velocities) < 3:
            return "stable"
        
        recent_avg = statistics.mean(velocities[-3:])
        older_avg = statistics.mean(velocities[-6:-3]) if len(velocities) >= 6 else velocities[0]
        
        if recent_avg > older_avg * 1.1:
            return "increasing"
        elif recent_avg < older_avg * 0.9:
            return "decreasing"
        else:
            return "stable"
    
    def _analyze_impediment_impact(self, impediment: Impediment) -> Dict[str, Any]:
        """Analyze the impact of an impediment"""
        impact = {
            "affected_story_points": 0,
            "affected_team_capacity": 0,
            "sprint_risk": "low",
            "escalation_needed": False
        }
        
        # Calculate affected story points
        for story_id in impediment.affected_stories:
            if story_id in self.stories:
                impact["affected_story_points"] += self.stories[story_id].story_points or 0
        
        # Calculate affected capacity
        impact["affected_team_capacity"] = len(impediment.affected_members) / len(self.team_members) * 100
        
        # Determine sprint risk
        if impediment.severity == "critical" or impact["affected_story_points"] > 20:
            impact["sprint_risk"] = "high"
            impact["escalation_needed"] = True
        elif impediment.severity == "high" or impact["affected_story_points"] > 10:
            impact["sprint_risk"] = "medium"
        
        return impact
    
    async def _generate_resolution_strategies(self, impediment: Impediment) -> List[Dict[str, str]]:
        """Generate strategies to resolve impediment"""
        strategies = []
        
        # Common resolution patterns
        if "technical" in impediment.description.lower():
            strategies.extend([
                {"strategy": "Pair programming session with senior developer", "effort": "2 hours"},
                {"strategy": "Technical spike to investigate solution", "effort": "4 hours"},
                {"strategy": "Consult with architect for design guidance", "effort": "1 hour"}
            ])
        
        if "blocked" in impediment.description.lower() and "waiting" in impediment.description.lower():
            strategies.extend([
                {"strategy": "Escalate to dependent team", "effort": "30 minutes"},
                {"strategy": "Find alternative approach to unblock", "effort": "2 hours"},
                {"strategy": "Re-prioritize to work on non-blocked items", "effort": "15 minutes"}
            ])
        
        if "communication" in impediment.description.lower():
            strategies.extend([
                {"strategy": "Schedule clarification meeting", "effort": "1 hour"},
                {"strategy": "Create communication protocol", "effort": "2 hours"},
                {"strategy": "Establish daily sync for affected parties", "effort": "15 minutes/day"}
            ])
        
        # Generic strategies
        strategies.extend([
            {"strategy": "Facilitate focused problem-solving session", "effort": "1 hour"},
            {"strategy": "Bring to team for collaborative solution", "effort": "30 minutes"}
        ])
        
        return strategies[:3]  # Return top 3 strategies
    
    async def _escalate_impediment(self, impediment: Impediment):
        """Escalate high-severity impediment"""
        escalation_message = {
            "impediment_id": impediment.impediment_id,
            "severity": impediment.severity,
            "description": impediment.description,
            "impact": self._analyze_impediment_impact(impediment),
            "escalation_time": datetime.utcnow().isoformat()
        }
        
        # In real implementation, this would notify stakeholders
        await self.publish_event("impediment_escalated", escalation_message)
        
        self.scrum_logger.warning(f"Escalated {impediment.severity} impediment: {impediment.description}")
    
    def _get_impediment_recommendations(self, category: str) -> List[str]:
        """Get recommendations for specific impediment category"""
        recommendations = {
            "technical": [
                "Schedule technical debt reduction sprint",
                "Implement pair programming for complex tasks",
                "Create technical documentation",
                "Establish code review standards"
            ],
            "communication": [
                "Implement daily standup best practices",
                "Create team communication charter",
                "Use collaboration tools more effectively",
                "Schedule regular stakeholder updates"
            ],
            "process": [
                "Review and optimize team processes",
                "Clarify roles and responsibilities",
                "Implement process automation",
                "Create process documentation"
            ]
        }
        
        return recommendations.get(category, ["Conduct root cause analysis", "Implement continuous improvement"])
    
    def _analyze_feedback_sentiment(self, feedback: Dict[str, Any]) -> List[RetrospectiveInsight]:
        """Analyze sentiment from team feedback"""
        insights = []
        
        # Simplified sentiment analysis
        positive_keywords = ["good", "great", "excellent", "happy", "satisfied", "improved"]
        negative_keywords = ["bad", "poor", "frustrated", "difficult", "problem", "issue"]
        
        positive_count = 0
        negative_count = 0
        
        for member_feedback in feedback.get("member_feedback", {}).values():
            text = member_feedback.get("comments", "").lower()
            positive_count += sum(1 for keyword in positive_keywords if keyword in text)
            negative_count += sum(1 for keyword in negative_keywords if keyword in text)
        
        sentiment_ratio = positive_count / (positive_count + negative_count) if (positive_count + negative_count) > 0 else 0.5
        
        if sentiment_ratio < 0.3:
            insights.append(RetrospectiveInsight(
                insight_id=f"insight_sentiment_{datetime.utcnow().timestamp()}",
                category="team",
                description="Team sentiment is predominantly negative",
                impact_score=80.0,
                recommended_actions=[
                    "Schedule team morale discussion",
                    "Identify and address key pain points",
                    "Consider team building activities"
                ],
                related_patterns=["low_morale", "team_dissatisfaction"],
                confidence=0.75
            ))
        
        return insights
    
    def _calculate_sprint_predictability(self) -> float:
        """Calculate how predictable sprint outcomes are"""
        if len(self.sprints) < 3:
            return 50.0  # Not enough data
        
        # Look at commitment accuracy over last sprints
        accuracies = []
        for sprint in list(self.sprints.values())[-5:]:
            if sprint.phase == SprintPhase.CLOSED and sprint.committed_points > 0:
                accuracy = abs(sprint.completed_points - sprint.committed_points) / sprint.committed_points
                accuracies.append(1 - accuracy)  # Convert to score where 1 is perfect
        
        if not accuracies:
            return 50.0
        
        return statistics.mean(accuracies) * 100
    
    def _calculate_burnout_risk(self) -> float:
        """Calculate team burnout risk"""
        risk_score = 0.0
        
        # Factor 1: Velocity trend
        if self._identify_velocity_trend(self._get_historical_velocities()) == "decreasing":
            risk_score += 20
        
        # Factor 2: Overtime/capacity
        for member in self.team_members.values():
            if member.current_sprint_availability < 0.8:  # Working at >120% capacity
                risk_score += 10
        
        # Factor 3: Impediment frequency
        recent_impediments = sum(1 for imp in self.impediments.values() 
                               if imp.identified_date > datetime.utcnow() - timedelta(days=14))
        if recent_impediments > 10:
            risk_score += 20
        
        # Factor 4: Sprint extensions or failures
        failed_sprints = sum(1 for sprint in self.sprints.values() 
                           if sprint.phase == SprintPhase.CLOSED and 
                           sprint.completed_points < sprint.committed_points * 0.7)
        risk_score += failed_sprints * 10
        
        return min(100, risk_score)
    
    async def _collaborate_with_po(self, message: Dict[str, Any]) -> AgentResult:
        """Handle collaboration with Product Owner"""
        message_type = message.get("type")
        
        if message_type == "backlog_refinement":
            # Provide velocity data for planning
            return AgentResult(
                success=True,
                data={
                    "average_velocity": statistics.mean(self._get_historical_velocities()) if self._get_historical_velocities() else 0,
                    "velocity_trend": self._identify_velocity_trend(self._get_historical_velocities()),
                    "team_capacity": self.get_team_capacity(),
                    "recommended_sprint_size": self._calculate_recommended_velocity(self.current_sprint) if self.current_sprint else 0
                },
                confidence=0.9,
                processing_time=0.0
            )
        
        elif message_type == "priority_clarification":
            # Provide team feedback on priorities
            return AgentResult(
                success=True,
                data={
                    "team_feedback": "Acknowledged priority clarification",
                    "technical_constraints": self._identify_technical_constraints(),
                    "dependency_warnings": self._identify_dependency_warnings()
                },
                confidence=0.85,
                processing_time=0.0
            )
        
        return AgentResult(
            success=True,
            data={"response": "Message received from Product Owner"},
            confidence=1.0,
            processing_time=0.0
        )
    
    async def _collaborate_with_dev(self, message: Dict[str, Any]) -> AgentResult:
        """Handle collaboration with Development Team member"""
        message_type = message.get("type")
        
        if message_type == "impediment_report":
            # Handle impediment from dev team
            return await self._handle_impediment(message.get("impediment_data", {}))
        
        elif message_type == "capacity_update":
            # Update team member capacity
            member_id = message.get("member_id")
            if member_id in self.team_members:
                self.team_members[member_id].current_sprint_availability = message.get("availability", 1.0)
                return AgentResult(
                    success=True,
                    data={"message": "Capacity updated"},
                    confidence=1.0,
                    processing_time=0.0
                )
        
        return AgentResult(
            success=True,
            data={"response": "Message received from Development Team"},
            confidence=1.0,
            processing_time=0.0
        )
    
    def _identify_technical_constraints(self) -> List[str]:
        """Identify current technical constraints"""
        constraints = []
        
        # Check for technical impediments
        tech_impediments = [imp for imp in self.impediments.values() 
                          if "technical" in imp.description.lower() and imp.status == "open"]
        
        for imp in tech_impediments[:3]:  # Top 3
            constraints.append(f"Technical constraint: {imp.description}")
        
        # Check for technical debt indicators
        if self._identify_velocity_trend(self._get_historical_velocities()) == "decreasing":
            constraints.append("Decreasing velocity may indicate technical debt accumulation")
        
        return constraints
    
    def _identify_dependency_warnings(self) -> List[str]:
        """Identify dependency warnings for planning"""
        warnings = []
        
        # Check for stories with many dependencies
        for story in self.stories.values():
            if len(story.dependencies) > 2:
                warnings.append(f"Story '{story.title}' has {len(story.dependencies)} dependencies")
        
        # Check for circular dependencies (simplified)
        # In real implementation, this would use graph algorithms
        
        return warnings[:5]  # Top 5 warnings