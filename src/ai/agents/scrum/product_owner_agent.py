"""
Product Owner Agent
Requirements Engineering and Prioritization for Scrum teams
"""

from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import asyncio
import re
from collections import defaultdict

from .base_scrum_agent import (
    BaseScrumAgent, UserStory, StoryStatus, StoryPriority, Sprint
)
from ..base_agent import AgentTask, AgentResult


class RequirementType(Enum):
    FUNCTIONAL = "functional"
    NON_FUNCTIONAL = "non_functional"
    BUSINESS = "business"
    TECHNICAL = "technical"
    REGULATORY = "regulatory"


class BusinessValue(Enum):
    VERY_HIGH = 5
    HIGH = 4
    MEDIUM = 3
    LOW = 2
    VERY_LOW = 1


@dataclass
class Requirement:
    """Represents a business requirement"""
    requirement_id: str
    title: str
    description: str
    type: RequirementType
    source: str  # stakeholder, market analysis, regulation, etc.
    business_value: BusinessValue
    created_at: datetime = field(default_factory=datetime.utcnow)
    validated: bool = False
    stories_generated: List[str] = field(default_factory=list)
    
    
@dataclass
class Stakeholder:
    """Represents a project stakeholder"""
    stakeholder_id: str
    name: str
    role: str
    email: str
    influence_level: str  # high, medium, low
    interest_areas: List[str]
    communication_preferences: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MarketInsight:
    """Market analysis insight"""
    insight_id: str
    category: str  # competitor, trend, opportunity, threat
    description: str
    impact: str  # high, medium, low
    confidence: float
    source: str
    identified_date: datetime = field(default_factory=datetime.utcnow)
    related_features: List[str] = field(default_factory=list)


@dataclass
class FeatureROI:
    """ROI calculation for a feature"""
    feature_id: str
    development_cost: float  # story points or hours
    expected_revenue: float
    cost_savings: float
    time_to_market: int  # days
    confidence_level: float
    assumptions: List[str]
    risks: List[str]
    
    @property
    def roi_percentage(self) -> float:
        """Calculate ROI percentage"""
        total_benefit = self.expected_revenue + self.cost_savings
        if self.development_cost == 0:
            return 0.0
        return ((total_benefit - self.development_cost) / self.development_cost) * 100


class ProductOwnerAgent(BaseScrumAgent):
    """
    Product Owner Agent - Manages product backlog and requirements
    
    Responsibilities:
    - Automatic user story generation from requirements
    - Intelligent backlog prioritization
    - Stakeholder communication management
    - Market analysis and feature impact prediction
    - ROI calculation for features
    - Product vision maintenance
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__("product_owner", config)
        
        # Product Owner specific data
        self.requirements: Dict[str, Requirement] = {}
        self.stakeholders: Dict[str, Stakeholder] = {}
        self.market_insights: List[MarketInsight] = []
        self.feature_roi_calculations: Dict[str, FeatureROI] = {}
        self.product_vision: str = config.get("product_vision", "")
        self.release_plan: Dict[str, List[str]] = {}  # release_id -> story_ids
        
        # Prioritization settings
        self.prioritization_weights = {
            "business_value": 0.3,
            "roi": 0.25,
            "risk_reduction": 0.15,
            "stakeholder_demand": 0.15,
            "technical_dependency": 0.15
        }
        
        # Natural language processing patterns for story generation
        self.story_patterns = self._load_story_patterns()
        
        # Start background tasks
        asyncio.create_task(self._analyze_market_trends())
        asyncio.create_task(self._monitor_stakeholder_satisfaction())
    
    def _load_story_patterns(self) -> Dict[str, str]:
        """Load patterns for user story generation"""
        return {
            "basic": "As a {user_type}, I want to {action} so that {benefit}",
            "detailed": "As a {user_type}, I want to {action} so that {benefit}. This involves {details}",
            "technical": "As a {user_type}, I need the system to {technical_requirement} in order to {goal}",
            "compliance": "As a {compliance_role}, I require {compliance_action} to meet {regulation}"
        }
    
    async def handle_sprint_event(self, event_type: str, event_data: Dict[str, Any]) -> AgentResult:
        """Handle sprint-related events"""
        try:
            if event_type == "generate_stories":
                return await self._generate_user_stories(event_data)
            elif event_type == "prioritize_backlog":
                return await self._prioritize_backlog(event_data)
            elif event_type == "calculate_roi":
                return await self._calculate_feature_roi(event_data)
            elif event_type == "stakeholder_communication":
                return await self._manage_stakeholder_communication(event_data)
            elif event_type == "market_analysis":
                return await self._perform_market_analysis(event_data)
            elif event_type == "refine_backlog":
                return await self._refine_backlog(event_data)
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
            if agent_name == "scrum_master":
                return await self._collaborate_with_sm(message)
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
    
    async def _generate_user_stories(self, req_data: Dict[str, Any]) -> AgentResult:
        """Generate user stories from requirements using AI"""
        requirement_ids = req_data.get("requirement_ids", [])
        auto_generate_all = req_data.get("auto_generate_all", False)
        
        generated_stories = []
        
        if auto_generate_all:
            # Generate stories for all unprocessed requirements
            requirement_ids = [
                req_id for req_id, req in self.requirements.items()
                if not req.stories_generated
            ]
        
        for req_id in requirement_ids:
            if req_id not in self.requirements:
                continue
                
            requirement = self.requirements[req_id]
            
            # Analyze requirement to extract story components
            story_components = self._analyze_requirement(requirement)
            
            # Generate stories based on requirement type
            if requirement.type == RequirementType.FUNCTIONAL:
                stories = self._generate_functional_stories(requirement, story_components)
            elif requirement.type == RequirementType.NON_FUNCTIONAL:
                stories = self._generate_nonfunctional_stories(requirement, story_components)
            elif requirement.type == RequirementType.REGULATORY:
                stories = self._generate_compliance_stories(requirement, story_components)
            else:
                stories = self._generate_business_stories(requirement, story_components)
            
            # Create story objects
            for story_data in stories:
                story = self.create_story(story_data)
                generated_stories.append(story)
                requirement.stories_generated.append(story.story_id)
        
        self.scrum_logger.info(f"Generated {len(generated_stories)} user stories")
        
        return AgentResult(
            success=True,
            data={
                "generated_stories": [story.__dict__ for story in generated_stories],
                "total_generated": len(generated_stories)
            },
            confidence=0.85,
            processing_time=0.0
        )
    
    async def _prioritize_backlog(self, priority_data: Dict[str, Any]) -> AgentResult:
        """Intelligent backlog prioritization using multiple factors"""
        include_sprint = priority_data.get("include_current_sprint", False)
        max_items = priority_data.get("max_items", 50)
        
        # Get all backlog items
        backlog_items = []
        for story_id in self.product_backlog:
            if story_id not in self.stories:
                continue
                
            story = self.stories[story_id]
            
            # Skip items already in sprint unless requested
            if not include_sprint and story.sprint_id:
                continue
                
            # Calculate priority score
            priority_score = self._calculate_priority_score(story)
            
            backlog_items.append({
                "story_id": story_id,
                "story": story,
                "priority_score": priority_score,
                "factors": self._get_priority_factors(story)
            })
        
        # Sort by priority score
        backlog_items.sort(key=lambda x: x["priority_score"], reverse=True)
        
        # Update backlog order
        self.product_backlog = [item["story_id"] for item in backlog_items[:max_items]]
        
        # Generate prioritization insights
        insights = self._generate_prioritization_insights(backlog_items[:10])
        
        return AgentResult(
            success=True,
            data={
                "prioritized_backlog": [
                    {
                        "story_id": item["story_id"],
                        "title": item["story"].title,
                        "priority_score": item["priority_score"],
                        "factors": item["factors"]
                    }
                    for item in backlog_items[:max_items]
                ],
                "insights": insights,
                "total_items": len(backlog_items)
            },
            confidence=0.9,
            processing_time=0.0
        )
    
    async def _calculate_feature_roi(self, roi_data: Dict[str, Any]) -> AgentResult:
        """Calculate ROI for features"""
        feature_id = roi_data["feature_id"]
        story_ids = roi_data.get("story_ids", [])
        
        # Calculate development cost (in story points)
        development_cost = sum(
            self.stories[sid].story_points or 0
            for sid in story_ids
            if sid in self.stories
        )
        
        # Estimate benefits based on business value and market analysis
        expected_revenue = self._estimate_revenue(feature_id, roi_data)
        cost_savings = self._estimate_cost_savings(feature_id, roi_data)
        
        # Calculate time to market
        time_to_market = self._estimate_time_to_market(story_ids)
        
        # Identify assumptions and risks
        assumptions = roi_data.get("assumptions", [
            "Market conditions remain stable",
            "Development estimates are accurate",
            "User adoption meets projections"
        ])
        
        risks = self._identify_roi_risks(feature_id, story_ids)
        
        # Create ROI calculation
        roi_calc = FeatureROI(
            feature_id=feature_id,
            development_cost=development_cost,
            expected_revenue=expected_revenue,
            cost_savings=cost_savings,
            time_to_market=time_to_market,
            confidence_level=0.7,  # Would be calculated based on data quality
            assumptions=assumptions,
            risks=risks
        )
        
        self.feature_roi_calculations[feature_id] = roi_calc
        
        return AgentResult(
            success=True,
            data={
                "feature_id": feature_id,
                "roi_percentage": roi_calc.roi_percentage,
                "development_cost": development_cost,
                "expected_revenue": expected_revenue,
                "cost_savings": cost_savings,
                "time_to_market": time_to_market,
                "confidence_level": roi_calc.confidence_level,
                "recommendation": self._generate_roi_recommendation(roi_calc)
            },
            confidence=roi_calc.confidence_level,
            processing_time=0.0
        )
    
    async def _manage_stakeholder_communication(self, comm_data: Dict[str, Any]) -> AgentResult:
        """Manage stakeholder communications"""
        communication_type = comm_data.get("type", "update")
        stakeholder_ids = comm_data.get("stakeholder_ids", [])
        
        if communication_type == "status_update":
            updates = self._generate_stakeholder_updates(stakeholder_ids)
        elif communication_type == "feedback_request":
            updates = self._generate_feedback_requests(stakeholder_ids)
        elif communication_type == "decision_needed":
            updates = self._generate_decision_requests(comm_data)
        else:
            updates = []
        
        # Send communications (in real implementation, would integrate with email/messaging)
        sent_count = 0
        for update in updates:
            # Log communication
            self.scrum_logger.info(f"Stakeholder communication to {update['stakeholder_id']}: {update['subject']}")
            sent_count += 1
        
        return AgentResult(
            success=True,
            data={
                "communications_sent": sent_count,
                "updates": updates
            },
            confidence=1.0,
            processing_time=0.0
        )
    
    async def _perform_market_analysis(self, market_data: Dict[str, Any]) -> AgentResult:
        """Perform market analysis for feature decisions"""
        analysis_type = market_data.get("type", "general")
        focus_area = market_data.get("focus_area", "all")
        
        insights = []
        
        if analysis_type == "competitor":
            insights = self._analyze_competitor_features(market_data)
        elif analysis_type == "trend":
            insights = self._analyze_market_trends(market_data)
        elif analysis_type == "opportunity":
            insights = self._identify_market_opportunities(market_data)
        
        # Store insights
        for insight_data in insights:
            insight = MarketInsight(
                insight_id=f"insight_{datetime.utcnow().timestamp()}",
                category=analysis_type,
                description=insight_data["description"],
                impact=insight_data["impact"],
                confidence=insight_data["confidence"],
                source=insight_data.get("source", "market_analysis")
            )
            self.market_insights.append(insight)
        
        # Generate recommendations based on insights
        recommendations = self._generate_market_recommendations(insights)
        
        return AgentResult(
            success=True,
            data={
                "insights": [insight.__dict__ for insight in insights],
                "recommendations": recommendations,
                "impact_on_backlog": self._assess_backlog_impact(insights)
            },
            confidence=0.8,
            processing_time=0.0
        )
    
    async def _refine_backlog(self, refinement_data: Dict[str, Any]) -> AgentResult:
        """Refine product backlog items"""
        story_ids = refinement_data.get("story_ids", [])
        refinement_type = refinement_data.get("type", "full")
        
        refined_stories = []
        
        for story_id in story_ids:
            if story_id not in self.stories:
                continue
                
            story = self.stories[story_id]
            
            # Refine based on type
            if refinement_type == "full":
                # Add acceptance criteria
                if not story.acceptance_criteria:
                    story.acceptance_criteria = self._generate_acceptance_criteria(story)
                
                # Estimate if not estimated
                if not story.story_points:
                    story.story_points = self._estimate_story_points(story)
                
                # Identify dependencies
                story.dependencies = self._identify_dependencies(story)
                
            elif refinement_type == "acceptance_criteria":
                story.acceptance_criteria = self._generate_acceptance_criteria(story)
                
            elif refinement_type == "estimation":
                story.story_points = self._estimate_story_points(story)
            
            story.status = StoryStatus.READY
            refined_stories.append(story)
        
        return AgentResult(
            success=True,
            data={
                "refined_stories": [story.__dict__ for story in refined_stories],
                "total_refined": len(refined_stories)
            },
            confidence=0.85,
            processing_time=0.0
        )
    
    # Helper methods
    
    def _analyze_requirement(self, requirement: Requirement) -> Dict[str, Any]:
        """Analyze requirement to extract story components"""
        components = {
            "user_types": [],
            "actions": [],
            "benefits": [],
            "acceptance_criteria": []
        }
        
        # Extract user types using patterns
        user_patterns = [r"user", r"customer", r"admin", r"operator", r"stakeholder"]
        for pattern in user_patterns:
            if re.search(pattern, requirement.description, re.IGNORECASE):
                components["user_types"].append(pattern)
        
        # Extract actions (verbs)
        action_patterns = [r"create", r"view", r"update", r"delete", r"process", r"manage", r"configure"]
        for pattern in action_patterns:
            if re.search(pattern, requirement.description, re.IGNORECASE):
                components["actions"].append(pattern)
        
        # Extract benefits
        benefit_keywords = ["so that", "in order to", "to enable", "allowing"]
        for keyword in benefit_keywords:
            if keyword in requirement.description.lower():
                # Extract text after keyword
                parts = requirement.description.lower().split(keyword)
                if len(parts) > 1:
                    components["benefits"].append(parts[1].strip()[:100])
        
        # Generate acceptance criteria based on requirement type
        if requirement.type == RequirementType.FUNCTIONAL:
            components["acceptance_criteria"] = [
                "Feature works as specified",
                "All edge cases are handled",
                "User interface is intuitive"
            ]
        elif requirement.type == RequirementType.NON_FUNCTIONAL:
            components["acceptance_criteria"] = [
                "Performance meets specified thresholds",
                "System remains stable under load",
                "Security requirements are met"
            ]
        
        return components
    
    def _generate_functional_stories(self, requirement: Requirement, components: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate functional user stories"""
        stories = []
        
        # Generate main story
        main_story = {
            "story_id": f"story_{requirement.requirement_id}_main",
            "title": f"Implement {requirement.title}",
            "description": self._format_story(
                self.story_patterns["basic"],
                user_type=components["user_types"][0] if components["user_types"] else "user",
                action=components["actions"][0] if components["actions"] else "use feature",
                benefit=components["benefits"][0] if components["benefits"] else "achieve goal"
            ),
            "acceptance_criteria": components["acceptance_criteria"],
            "story_points": None,  # To be estimated
            "priority": self._map_business_value_to_priority(requirement.business_value),
            "tags": ["functional", requirement.source]
        }
        stories.append(main_story)
        
        # Generate sub-stories for complex requirements
        if len(components["actions"]) > 2:
            for i, action in enumerate(components["actions"][1:3]):  # Limit to 2 sub-stories
                sub_story = {
                    "story_id": f"story_{requirement.requirement_id}_sub_{i}",
                    "title": f"{action.capitalize()} functionality",
                    "description": f"Enable users to {action} as part of {requirement.title}",
                    "acceptance_criteria": [f"{action} works correctly", "Error handling is implemented"],
                    "story_points": None,
                    "priority": self._map_business_value_to_priority(requirement.business_value),
                    "tags": ["functional", "sub-story"],
                    "dependencies": [main_story["story_id"]]
                }
                stories.append(sub_story)
        
        return stories
    
    def _generate_nonfunctional_stories(self, requirement: Requirement, components: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate non-functional user stories"""
        stories = []
        
        # Map non-functional requirements to specific story types
        if "performance" in requirement.description.lower():
            story = {
                "story_id": f"story_{requirement.requirement_id}_perf",
                "title": f"Performance optimization for {requirement.title}",
                "description": self._format_story(
                    self.story_patterns["technical"],
                    user_type="system",
                    technical_requirement=f"meet performance targets: {requirement.description[:100]}",
                    goal="ensure optimal user experience"
                ),
                "acceptance_criteria": [
                    "Response time < 200ms for 95% of requests",
                    "System handles specified concurrent users",
                    "Performance tests pass"
                ],
                "story_points": None,
                "priority": StoryPriority.HIGH,
                "tags": ["non-functional", "performance"]
            }
            stories.append(story)
            
        elif "security" in requirement.description.lower():
            story = {
                "story_id": f"story_{requirement.requirement_id}_sec",
                "title": f"Security implementation for {requirement.title}",
                "description": self._format_story(
                    self.story_patterns["technical"],
                    user_type="security team",
                    technical_requirement="implement security controls",
                    goal="protect user data and system integrity"
                ),
                "acceptance_criteria": [
                    "All OWASP top 10 vulnerabilities addressed",
                    "Security scan shows no critical issues",
                    "Authentication and authorization properly implemented"
                ],
                "story_points": None,
                "priority": StoryPriority.CRITICAL,
                "tags": ["non-functional", "security"]
            }
            stories.append(story)
        
        return stories
    
    def _generate_compliance_stories(self, requirement: Requirement, components: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate compliance/regulatory stories"""
        story = {
            "story_id": f"story_{requirement.requirement_id}_compliance",
            "title": f"Compliance: {requirement.title}",
            "description": self._format_story(
                self.story_patterns["compliance"],
                compliance_role="compliance officer",
                compliance_action=requirement.description[:100],
                regulation=requirement.source
            ),
            "acceptance_criteria": [
                "All regulatory requirements are met",
                "Compliance documentation is complete",
                "Audit trail is implemented",
                "Data handling follows regulations"
            ],
            "story_points": None,
            "priority": StoryPriority.CRITICAL,
            "tags": ["compliance", "regulatory", requirement.source]
        }
        
        return [story]
    
    def _generate_business_stories(self, requirement: Requirement, components: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate business-oriented stories"""
        story = {
            "story_id": f"story_{requirement.requirement_id}_business",
            "title": requirement.title,
            "description": self._format_story(
                self.story_patterns["basic"],
                user_type="business user",
                action=f"achieve {requirement.title}",
                benefit=requirement.description[:100]
            ),
            "acceptance_criteria": [
                "Business objective is met",
                "ROI targets are achievable",
                "Stakeholder approval obtained"
            ],
            "story_points": None,
            "priority": self._map_business_value_to_priority(requirement.business_value),
            "tags": ["business", requirement.source]
        }
        
        return [story]
    
    def _format_story(self, pattern: str, **kwargs) -> str:
        """Format story using pattern and parameters"""
        try:
            return pattern.format(**kwargs)
        except KeyError:
            return f"User story for: {kwargs.get('action', 'requirement')}"
    
    def _map_business_value_to_priority(self, business_value: BusinessValue) -> StoryPriority:
        """Map business value to story priority"""
        mapping = {
            BusinessValue.VERY_HIGH: StoryPriority.CRITICAL,
            BusinessValue.HIGH: StoryPriority.HIGH,
            BusinessValue.MEDIUM: StoryPriority.MEDIUM,
            BusinessValue.LOW: StoryPriority.LOW,
            BusinessValue.VERY_LOW: StoryPriority.TRIVIAL
        }
        return mapping.get(business_value, StoryPriority.MEDIUM)
    
    def _calculate_priority_score(self, story: UserStory) -> float:
        """Calculate comprehensive priority score for a story"""
        score = 0.0
        
        # Business value component
        business_value_score = (6 - story.priority.value) * 20  # 20-100 range
        score += business_value_score * self.prioritization_weights["business_value"]
        
        # ROI component
        roi_score = self._calculate_story_roi_score(story)
        score += roi_score * self.prioritization_weights["roi"]
        
        # Risk reduction component
        risk_score = self._calculate_risk_reduction_score(story)
        score += risk_score * self.prioritization_weights["risk_reduction"]
        
        # Stakeholder demand component
        stakeholder_score = self._calculate_stakeholder_demand_score(story)
        score += stakeholder_score * self.prioritization_weights["stakeholder_demand"]
        
        # Technical dependency component
        dependency_score = self._calculate_dependency_score(story)
        score += dependency_score * self.prioritization_weights["technical_dependency"]
        
        return score
    
    def _calculate_story_roi_score(self, story: UserStory) -> float:
        """Calculate ROI score for a story"""
        # Check if story is part of a feature with ROI calculation
        for feature_id, roi_calc in self.feature_roi_calculations.items():
            if story.story_id in self.get_feature_stories(feature_id):
                # Normalize ROI to 0-100 scale
                if roi_calc.roi_percentage > 200:
                    return 100
                elif roi_calc.roi_percentage < 0:
                    return 0
                else:
                    return roi_calc.roi_percentage / 2
        
        # Default score based on business value
        return (6 - story.priority.value) * 15
    
    def _calculate_risk_reduction_score(self, story: UserStory) -> float:
        """Calculate risk reduction score"""
        score = 50.0  # Base score
        
        # Security stories reduce risk
        if "security" in story.tags:
            score += 30
        
        # Compliance stories reduce risk
        if "compliance" in story.tags or "regulatory" in story.tags:
            score += 40
        
        # Bug fixes reduce risk
        if "bug" in story.tags or "fix" in story.title.lower():
            score += 20
        
        return min(100, score)
    
    def _calculate_stakeholder_demand_score(self, story: UserStory) -> float:
        """Calculate stakeholder demand score"""
        score = 40.0  # Base score
        
        # Check stakeholder interest
        high_influence_stakeholders = [
            s for s in self.stakeholders.values()
            if s.influence_level == "high"
        ]
        
        # If story relates to high-influence stakeholder interests
        for stakeholder in high_influence_stakeholders:
            for interest in stakeholder.interest_areas:
                if interest.lower() in story.title.lower() or interest.lower() in story.description.lower():
                    score += 20
                    break
        
        return min(100, score)
    
    def _calculate_dependency_score(self, story: UserStory) -> float:
        """Calculate technical dependency score"""
        # Stories with no dependencies score higher
        if not story.dependencies:
            return 80.0
        
        # Stories that unblock others score higher
        blocking_count = sum(
            1 for s in self.stories.values()
            if story.story_id in s.dependencies
        )
        
        if blocking_count > 3:
            return 100.0
        elif blocking_count > 1:
            return 90.0
        elif blocking_count == 1:
            return 70.0
        else:
            # Has dependencies but doesn't block others
            return 40.0
    
    def _get_priority_factors(self, story: UserStory) -> Dict[str, float]:
        """Get individual priority factors for a story"""
        return {
            "business_value": (6 - story.priority.value) * 20,
            "roi": self._calculate_story_roi_score(story),
            "risk_reduction": self._calculate_risk_reduction_score(story),
            "stakeholder_demand": self._calculate_stakeholder_demand_score(story),
            "technical_dependency": self._calculate_dependency_score(story)
        }
    
    def _generate_prioritization_insights(self, top_items: List[Dict[str, Any]]) -> List[str]:
        """Generate insights about prioritization"""
        insights = []
        
        # Check for common patterns in top items
        top_tags = defaultdict(int)
        for item in top_items:
            for tag in item["story"].tags:
                top_tags[tag] += 1
        
        # Generate insights based on patterns
        if top_tags.get("security", 0) >= 3:
            insights.append("Security stories are highly prioritized - consider security sprint")
        
        if top_tags.get("compliance", 0) >= 2:
            insights.append("Multiple compliance items in top priority - regulatory deadline approaching?")
        
        # Check for dependency chains
        dependency_count = sum(1 for item in top_items if item["story"].dependencies)
        if dependency_count >= 5:
            insights.append("Many dependent stories in top items - consider dependency resolution sprint")
        
        # Check ROI distribution
        high_roi_count = sum(
            1 for item in top_items
            if item["factors"]["roi"] > 70
        )
        if high_roi_count >= 4:
            insights.append("High ROI items dominating backlog - good focus on value delivery")
        
        return insights
    
    def _estimate_revenue(self, feature_id: str, roi_data: Dict[str, Any]) -> float:
        """Estimate revenue for a feature"""
        base_revenue = roi_data.get("estimated_revenue", 0)
        
        # Adjust based on market insights
        relevant_insights = [
            insight for insight in self.market_insights
            if feature_id in insight.related_features
        ]
        
        for insight in relevant_insights:
            if insight.category == "opportunity" and insight.impact == "high":
                base_revenue *= 1.3
            elif insight.category == "threat" and insight.impact == "high":
                base_revenue *= 0.7
        
        return base_revenue
    
    def _estimate_cost_savings(self, feature_id: str, roi_data: Dict[str, Any]) -> float:
        """Estimate cost savings from a feature"""
        savings = roi_data.get("estimated_savings", 0)
        
        # Add automation savings
        if "automation" in feature_id.lower():
            # Estimate hours saved * hourly rate
            hours_saved_monthly = roi_data.get("hours_saved_monthly", 20)
            hourly_rate = roi_data.get("hourly_rate", 75)
            savings += hours_saved_monthly * hourly_rate * 12  # Annual
        
        return savings
    
    def _estimate_time_to_market(self, story_ids: List[str]) -> int:
        """Estimate time to market in days"""
        total_points = sum(
            self.stories[sid].story_points or 5  # Default 5 if not estimated
            for sid in story_ids
            if sid in self.stories
        )
        
        # Assume team velocity (points per sprint)
        team_velocity = 30  # Would come from historical data
        sprint_length = 14  # days
        
        sprints_needed = (total_points / team_velocity) + 0.5  # Buffer
        
        return int(sprints_needed * sprint_length)
    
    def _identify_roi_risks(self, feature_id: str, story_ids: List[str]) -> List[str]:
        """Identify risks that could impact ROI"""
        risks = []
        
        # Technical risks
        complex_story_count = sum(
            1 for sid in story_ids
            if sid in self.stories and (self.stories[sid].story_points or 0) > 8
        )
        if complex_story_count > 2:
            risks.append("High technical complexity may impact delivery timeline")
        
        # Dependency risks
        total_dependencies = sum(
            len(self.stories[sid].dependencies)
            for sid in story_ids
            if sid in self.stories
        )
        if total_dependencies > 5:
            risks.append("Multiple dependencies could delay implementation")
        
        # Market risks
        threat_insights = [
            i for i in self.market_insights
            if i.category == "threat" and feature_id in i.related_features
        ]
        if threat_insights:
            risks.append("Market threats identified that could impact adoption")
        
        # Resource risks
        if len(story_ids) > 10:
            risks.append("Large feature scope may strain team resources")
        
        return risks
    
    def _generate_roi_recommendation(self, roi_calc: FeatureROI) -> str:
        """Generate recommendation based on ROI calculation"""
        if roi_calc.roi_percentage > 150:
            return "Strongly recommended - High ROI feature with significant value"
        elif roi_calc.roi_percentage > 75:
            return "Recommended - Good ROI with reasonable investment"
        elif roi_calc.roi_percentage > 25:
            return "Consider - Moderate ROI, evaluate against alternatives"
        elif roi_calc.roi_percentage > 0:
            return "Low priority - Minimal ROI, consider deferring"
        else:
            return "Not recommended - Negative ROI expected"
    
    def _generate_stakeholder_updates(self, stakeholder_ids: List[str]) -> List[Dict[str, Any]]:
        """Generate status updates for stakeholders"""
        updates = []
        
        # Get current sprint info
        current_sprint = self.current_sprint
        if not current_sprint:
            return updates
        
        for stakeholder_id in stakeholder_ids:
            if stakeholder_id not in self.stakeholders:
                continue
                
            stakeholder = self.stakeholders[stakeholder_id]
            
            # Customize update based on stakeholder interests
            relevant_stories = self._get_stakeholder_relevant_stories(stakeholder)
            
            update = {
                "stakeholder_id": stakeholder_id,
                "subject": f"Sprint {current_sprint.name} Progress Update",
                "content": self._format_stakeholder_update(stakeholder, current_sprint, relevant_stories),
                "priority": "normal",
                "channel": stakeholder.communication_preferences.get("channel", "email")
            }
            
            updates.append(update)
        
        return updates
    
    def _generate_feedback_requests(self, stakeholder_ids: List[str]) -> List[Dict[str, Any]]:
        """Generate feedback requests for stakeholders"""
        requests = []
        
        for stakeholder_id in stakeholder_ids:
            if stakeholder_id not in self.stakeholders:
                continue
                
            stakeholder = self.stakeholders[stakeholder_id]
            
            # Find items needing feedback
            feedback_items = self._get_items_needing_feedback(stakeholder)
            
            if feedback_items:
                request = {
                    "stakeholder_id": stakeholder_id,
                    "subject": "Your feedback needed on upcoming features",
                    "content": self._format_feedback_request(stakeholder, feedback_items),
                    "priority": "high",
                    "channel": stakeholder.communication_preferences.get("channel", "email"),
                    "response_needed_by": (datetime.utcnow() + timedelta(days=3)).isoformat()
                }
                
                requests.append(request)
        
        return requests
    
    def _generate_decision_requests(self, comm_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate decision requests for stakeholders"""
        decision_type = comm_data.get("decision_type", "prioritization")
        options = comm_data.get("options", [])
        
        requests = []
        
        # Identify decision makers
        decision_makers = [
            s for s in self.stakeholders.values()
            if s.influence_level == "high"
        ]
        
        for stakeholder in decision_makers:
            request = {
                "stakeholder_id": stakeholder.stakeholder_id,
                "subject": f"Decision needed: {decision_type}",
                "content": self._format_decision_request(stakeholder, decision_type, options),
                "priority": "urgent",
                "channel": stakeholder.communication_preferences.get("channel", "email"),
                "response_needed_by": (datetime.utcnow() + timedelta(days=2)).isoformat()
            }
            
            requests.append(request)
        
        return requests
    
    def _get_stakeholder_relevant_stories(self, stakeholder: Stakeholder) -> List[UserStory]:
        """Get stories relevant to stakeholder interests"""
        relevant_stories = []
        
        for story in self.stories.values():
            # Check if story matches stakeholder interests
            for interest in stakeholder.interest_areas:
                if (interest.lower() in story.title.lower() or 
                    interest.lower() in story.description.lower() or
                    interest.lower() in story.tags):
                    relevant_stories.append(story)
                    break
        
        return relevant_stories[:10]  # Limit to top 10
    
    def _format_stakeholder_update(self, stakeholder: Stakeholder, sprint: Sprint, relevant_stories: List[UserStory]) -> str:
        """Format stakeholder update content"""
        completed_stories = [s for s in relevant_stories if s.status == StoryStatus.DONE]
        in_progress_stories = [s for s in relevant_stories if s.status == StoryStatus.IN_PROGRESS]
        
        content = f"""
Dear {stakeholder.name},

Here's your personalized update for Sprint {sprint.name}:

Sprint Progress: {sprint.progress_percentage:.1f}% complete
Days Remaining: {(sprint.end_date - datetime.utcnow()).days}

Your Areas of Interest:
"""
        
        if completed_stories:
            content += "\nCompleted Items:\n"
            for story in completed_stories[:3]:
                content += f"- {story.title}\n"
        
        if in_progress_stories:
            content += "\nIn Progress:\n"
            for story in in_progress_stories[:3]:
                content += f"- {story.title}\n"
        
        content += "\nPlease reach out if you have any questions or concerns.\n\nBest regards,\nProduct Owner"
        
        return content
    
    def _get_items_needing_feedback(self, stakeholder: Stakeholder) -> List[UserStory]:
        """Get items that need stakeholder feedback"""
        feedback_items = []
        
        for story in self.stories.values():
            # Stories in backlog that match interests and need refinement
            if (story.status == StoryStatus.BACKLOG and
                not story.acceptance_criteria and
                any(interest.lower() in story.title.lower() for interest in stakeholder.interest_areas)):
                feedback_items.append(story)
        
        return feedback_items[:5]
    
    def _format_feedback_request(self, stakeholder: Stakeholder, items: List[UserStory]) -> str:
        """Format feedback request content"""
        content = f"""
Dear {stakeholder.name},

We're planning upcoming features and would value your input on the following items:

"""
        
        for i, story in enumerate(items, 1):
            content += f"{i}. {story.title}\n   {story.description}\n\n"
        
        content += """
Please provide feedback on:
- Are these features aligned with your needs?
- What acceptance criteria would you suggest?
- What priority would you assign to each?

Your feedback by {(datetime.utcnow() + timedelta(days=3)).strftime('%Y-%m-%d')} would be greatly appreciated.

Best regards,
Product Owner
"""
        
        return content
    
    def _format_decision_request(self, stakeholder: Stakeholder, decision_type: str, options: List[Any]) -> str:
        """Format decision request content"""
        content = f"""
Dear {stakeholder.name},

A decision is needed regarding: {decision_type}

Options to consider:
"""
        
        for i, option in enumerate(options, 1):
            content += f"\n{i}. {option.get('name', 'Option ' + str(i))}"
            if 'description' in option:
                content += f"\n   {option['description']}"
            if 'pros' in option:
                content += f"\n   Pros: {', '.join(option['pros'])}"
            if 'cons' in option:
                content += f"\n   Cons: {', '.join(option['cons'])}"
            content += "\n"
        
        content += f"""
Please provide your decision by {(datetime.utcnow() + timedelta(days=2)).strftime('%Y-%m-%d')}.

Best regards,
Product Owner
"""
        
        return content
    
    async def _analyze_market_trends(self):
        """Background task to analyze market trends"""
        while True:
            try:
                # Simulate market analysis (in real implementation, would use external data sources)
                await asyncio.sleep(86400)  # Daily analysis
                
                # Generate market insights
                trend_insights = [
                    {
                        "description": "Increased demand for AI-powered features",
                        "impact": "high",
                        "confidence": 0.8
                    },
                    {
                        "description": "Competitors launching mobile-first solutions",
                        "impact": "medium",
                        "confidence": 0.7
                    }
                ]
                
                for insight_data in trend_insights:
                    insight = MarketInsight(
                        insight_id=f"trend_{datetime.utcnow().timestamp()}",
                        category="trend",
                        description=insight_data["description"],
                        impact=insight_data["impact"],
                        confidence=insight_data["confidence"],
                        source="market_analysis"
                    )
                    self.market_insights.append(insight)
                
                # Publish market insight event
                await self.publish_event("market_insight_available", {
                    "insights": [insight.__dict__ for insight in self.market_insights[-2:]]
                })
                
            except Exception as e:
                self.scrum_logger.error(f"Error in market analysis: {e}")
                await asyncio.sleep(86400)
    
    async def _monitor_stakeholder_satisfaction(self):
        """Background task to monitor stakeholder satisfaction"""
        while True:
            try:
                await asyncio.sleep(604800)  # Weekly check
                
                # Calculate satisfaction metrics
                for stakeholder in self.stakeholders.values():
                    relevant_stories = self._get_stakeholder_relevant_stories(stakeholder)
                    
                    completed_relevant = sum(1 for s in relevant_stories if s.status == StoryStatus.DONE)
                    total_relevant = len(relevant_stories)
                    
                    if total_relevant > 0:
                        satisfaction_score = (completed_relevant / total_relevant) * 100
                        
                        if satisfaction_score < 30:
                            # Low satisfaction - needs attention
                            await self.publish_event("stakeholder_satisfaction_alert", {
                                "stakeholder_id": stakeholder.stakeholder_id,
                                "satisfaction_score": satisfaction_score,
                                "recommendation": "Schedule meeting to discuss priorities"
                            })
                
            except Exception as e:
                self.scrum_logger.error(f"Error monitoring stakeholder satisfaction: {e}")
                await asyncio.sleep(604800)
    
    def _analyze_competitor_features(self, market_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze competitor features"""
        # In real implementation, would use competitive intelligence data
        return [
            {
                "description": "Competitor X launched real-time collaboration feature",
                "impact": "high",
                "confidence": 0.9,
                "source": "competitor_analysis"
            }
        ]
    
    def _identify_market_opportunities(self, market_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify market opportunities"""
        return [
            {
                "description": "Gap in market for enterprise-grade solution",
                "impact": "high",
                "confidence": 0.75,
                "source": "market_research"
            }
        ]
    
    def _generate_market_recommendations(self, insights: List[MarketInsight]) -> List[str]:
        """Generate recommendations based on market insights"""
        recommendations = []
        
        high_impact_insights = [i for i in insights if i["impact"] == "high"]
        
        for insight in high_impact_insights:
            if "AI" in insight["description"]:
                recommendations.append("Prioritize AI-powered features in next release")
            elif "mobile" in insight["description"]:
                recommendations.append("Consider mobile-first approach for new features")
            elif "enterprise" in insight["description"]:
                recommendations.append("Focus on enterprise features for market differentiation")
        
        return recommendations
    
    def _assess_backlog_impact(self, insights: List[MarketInsight]) -> Dict[str, Any]:
        """Assess how market insights impact current backlog"""
        impact = {
            "stories_to_reprioritize": [],
            "new_stories_needed": [],
            "obsolete_stories": []
        }
        
        # Check each insight against backlog
        for insight in insights:
            if insight["impact"] == "high":
                # Find related stories
                for story in self.stories.values():
                    if any(keyword in story.title.lower() for keyword in insight["description"].lower().split()):
                        impact["stories_to_reprioritize"].append(story.story_id)
        
        return impact
    
    def _generate_acceptance_criteria(self, story: UserStory) -> List[str]:
        """Generate acceptance criteria for a story"""
        criteria = []
        
        # Basic functional criteria
        criteria.append(f"{story.title} is fully implemented")
        criteria.append("Feature works as described in all supported browsers/platforms")
        
        # Add specific criteria based on story type
        if "api" in story.title.lower():
            criteria.extend([
                "API endpoint returns correct status codes",
                "Response time is under 200ms",
                "API documentation is updated"
            ])
        elif "ui" in story.title.lower() or "interface" in story.title.lower():
            criteria.extend([
                "UI is responsive and accessible",
                "User flow is intuitive",
                "Visual design matches mockups"
            ])
        elif "security" in story.tags:
            criteria.extend([
                "Security best practices are followed",
                "No vulnerabilities in security scan",
                "Authentication/authorization properly implemented"
            ])
        
        # Always include testing criteria
        criteria.append("Unit tests written and passing")
        criteria.append("Integration tests cover main scenarios")
        
        return criteria
    
    def _estimate_story_points(self, story: UserStory) -> int:
        """Estimate story points using AI analysis"""
        # Base estimation on complexity indicators
        points = 3  # Default medium complexity
        
        # Adjust based on title and description length (rough proxy for complexity)
        if len(story.description) > 200:
            points += 2
        
        # Adjust based on acceptance criteria
        if len(story.acceptance_criteria) > 5:
            points += 2
        elif len(story.acceptance_criteria) < 3:
            points -= 1
        
        # Adjust based on dependencies
        points += len(story.dependencies)
        
        # Adjust based on tags
        if "security" in story.tags or "compliance" in story.tags:
            points += 3
        if "bug" in story.tags:
            points = max(1, points - 2)
        if "spike" in story.tags or "research" in story.tags:
            points = 3  # Spikes are typically time-boxed
        
        # Fibonacci sequence constraint
        fibonacci = [1, 2, 3, 5, 8, 13, 21]
        return min(fibonacci, key=lambda x: abs(x - points))
    
    def _identify_dependencies(self, story: UserStory) -> List[str]:
        """Identify story dependencies"""
        dependencies = []
        
        # Check for explicit dependencies in description
        dep_keywords = ["depends on", "requires", "needs", "after"]
        for keyword in dep_keywords:
            if keyword in story.description.lower():
                # Extract story references (simplified)
                # In real implementation, would use NLP
                pass
        
        # Check for technical dependencies
        if "api" in story.title.lower():
            # Check if UI stories depend on this
            for other_story in self.stories.values():
                if ("ui" in other_story.title.lower() and 
                    any(tag in story.tags for tag in other_story.tags)):
                    other_story.dependencies.append(story.story_id)
        
        # Check for logical dependencies
        if "authentication" in story.title.lower():
            # Many features depend on auth
            dependencies = []  # Auth usually has no dependencies
        elif "database" in story.title.lower() or "schema" in story.title.lower():
            # Database changes often have no dependencies but block others
            dependencies = []
        
        return dependencies
    
    def get_feature_stories(self, feature_id: str) -> List[str]:
        """Get all stories related to a feature"""
        # In real implementation, would maintain feature-story mapping
        # For now, use simple tag matching
        feature_stories = []
        
        for story_id, story in self.stories.items():
            if feature_id in story.tags or feature_id in story.title.lower():
                feature_stories.append(story_id)
        
        return feature_stories
    
    def create_requirement(self, req_data: Dict[str, Any]) -> Requirement:
        """Create a new requirement"""
        requirement = Requirement(
            requirement_id=req_data.get("requirement_id", f"req_{datetime.utcnow().timestamp()}"),
            title=req_data["title"],
            description=req_data["description"],
            type=RequirementType(req_data.get("type", RequirementType.FUNCTIONAL.value)),
            source=req_data.get("source", "stakeholder"),
            business_value=BusinessValue(req_data.get("business_value", BusinessValue.MEDIUM.value))
        )
        
        self.requirements[requirement.requirement_id] = requirement
        
        return requirement
    
    def add_stakeholder(self, stakeholder_data: Dict[str, Any]) -> Stakeholder:
        """Add a new stakeholder"""
        stakeholder = Stakeholder(
            stakeholder_id=stakeholder_data["stakeholder_id"],
            name=stakeholder_data["name"],
            role=stakeholder_data["role"],
            email=stakeholder_data["email"],
            influence_level=stakeholder_data.get("influence_level", "medium"),
            interest_areas=stakeholder_data.get("interest_areas", []),
            communication_preferences=stakeholder_data.get("communication_preferences", {})
        )
        
        self.stakeholders[stakeholder.stakeholder_id] = stakeholder
        
        return stakeholder
    
    async def _collaborate_with_sm(self, message: Dict[str, Any]) -> AgentResult:
        """Handle collaboration with Scrum Master"""
        message_type = message.get("type")
        
        if message_type == "velocity_request":
            # Provide velocity data for sprint planning
            return AgentResult(
                success=True,
                data={
                    "ready_stories": [
                        sid for sid in self.product_backlog
                        if self.stories[sid].status == StoryStatus.READY
                    ],
                    "total_ready_points": sum(
                        self.stories[sid].story_points or 0
                        for sid in self.product_backlog
                        if sid in self.stories and self.stories[sid].status == StoryStatus.READY
                    )
                },
                confidence=1.0,
                processing_time=0.0
            )
        
        elif message_type == "refinement_needed":
            # Stories need refinement
            story_ids = message.get("story_ids", [])
            return await self._refine_backlog({"story_ids": story_ids, "type": "full"})
        
        return AgentResult(
            success=True,
            data={"response": "Message received from Scrum Master"},
            confidence=1.0,
            processing_time=0.0
        )
    
    async def _collaborate_with_dev(self, message: Dict[str, Any]) -> AgentResult:
        """Handle collaboration with Development Team"""
        message_type = message.get("type")
        
        if message_type == "clarification_needed":
            # Provide clarification on stories
            story_id = message.get("story_id")
            if story_id in self.stories:
                story = self.stories[story_id]
                return AgentResult(
                    success=True,
                    data={
                        "story_id": story_id,
                        "clarification": f"Additional details for {story.title}",
                        "acceptance_criteria": story.acceptance_criteria,
                        "business_context": "This feature addresses key customer pain point"
                    },
                    confidence=1.0,
                    processing_time=0.0
                )
        
        elif message_type == "technical_feasibility":
            # Receive technical feasibility feedback
            story_id = message.get("story_id")
            feasibility = message.get("feasibility", "unknown")
            
            if story_id in self.stories and feasibility == "not_feasible":
                # Adjust story or create spike
                self.stories[story_id].tags.append("needs_spike")
                
            return AgentResult(
                success=True,
                data={"acknowledged": True},
                confidence=1.0,
                processing_time=0.0
            )
        
        return AgentResult(
            success=True,
            data={"response": "Message received from Development Team"},
            confidence=1.0,
            processing_time=0.0
        )