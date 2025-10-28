"""
Integration tests for AgentOrchestrator
"""

import pytest
import asyncio
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

from src.ai.orchestrator import AgentOrchestrator
from src.ai.agents.base_agent import BaseAgent, AgentResult


class MockLLMClient:
    """Mock LLM client for testing"""
    
    async def generate(self, prompt, **kwargs):
        return "Mock LLM response"


class MockEmailClassifier(BaseAgent):
    """Mock email classifier for testing"""
    
    def __init__(self, config=None):
        super().__init__("email_classifier", config)
    
    async def process_task(self, task):
        return AgentResult(
            success=True,
            data={
                "category": "work",
                "priority": "high",
                "sentiment": "neutral",
                "confidence": 0.85
            },
            confidence=0.85,
            processing_time=0.2
        )
    
    def get_supported_task_types(self):
        return ["classify_email", "analyze_reply_context"]


class MockSearchAgent(BaseAgent):
    """Mock search agent for testing"""
    
    def __init__(self, config=None):
        super().__init__("search_agent", config)
    
    async def process_task(self, task):
        return AgentResult(
            success=True,
            data={
                "embedding": [0.1, 0.2, 0.3],
                "similar_emails": [],
                "indexed": True
            },
            confidence=0.9,
            processing_time=0.15
        )
    
    def get_supported_task_types(self):
        return ["generate_embedding", "find_similar_emails", "get_thread_emails"]


class MockTaggingAgent(BaseAgent):
    """Mock tagging agent for testing"""
    
    def __init__(self, config=None):
        super().__init__("tagging_agent", config)
    
    async def process_task(self, task):
        return AgentResult(
            success=True,
            data={
                "tags": ["work", "meeting", "important"],
                "tag_confidence": {"work": 0.9, "meeting": 0.8, "important": 0.7}
            },
            confidence=0.8,
            processing_time=0.1
        )
    
    def get_supported_task_types(self):
        return ["generate_tags"]


class TestOrchestratorIntegration:
    """Integration tests for the orchestrator with real agent interactions"""
    
    @pytest.fixture
    def mock_config(self):
        """Mock configuration for orchestrator"""
        return {
            "classifier": {"model": "test"},
            "search": {"vector_db": "test"},
            "tagging": {"threshold": 0.5},
            "workflow": {"max_parallel": 3},
            "automation": {"default_rules": True},
            "notification": {"channels": ["in_app"]},
            "scheduling": {"timezone": "UTC"}
        }
    
    @pytest.fixture
    def sample_email(self):
        """Sample email data for testing"""
        return {
            "id": "test_email_123",
            "subject": "Important project update",
            "sender_email": "colleague@company.com",
            "sender_name": "John Doe",
            "recipient_email": "user@company.com",
            "content": "Hi team, please review the attached document for our meeting tomorrow.",
            "attachments": 1,
            "received_at": datetime.utcnow().isoformat(),
            "user_id": "user_123"
        }
    
    @pytest.fixture
    def orchestrator_with_mocks(self, mock_config):
        """Create orchestrator with mocked agents"""
        with patch.multiple(
            'src.ai.orchestrator',
            EmailClassifierAgent=MockEmailClassifier,
            SearchAgent=MockSearchAgent,
            TaggingAgent=MockTaggingAgent,
            SummaryAgent=MagicMock,
            ResponseAgent=MagicMock,
            WorkflowOrchestrationAgent=MagicMock,
            TaskAutomationAgent=MagicMock,
            NotificationAgent=MagicMock,
            SchedulingAgent=MagicMock
        ):
            return AgentOrchestrator(mock_config)
    
    @pytest.mark.asyncio
    async def test_orchestrator_initialization(self, orchestrator_with_mocks):
        """Test that orchestrator initializes all agents correctly"""
        orchestrator = orchestrator_with_mocks
        
        # Check that all expected agents are registered
        expected_agents = [
            "email_classifier",
            "search_agent", 
            "tagging_agent",
            "summary_agent",
            "response_agent",
            "workflow_orchestration",
            "task_automation",
            "notification_agent",
            "scheduling_agent"
        ]
        
        for agent_name in expected_agents:
            assert agent_name in orchestrator.agents
            assert orchestrator.agents[agent_name] is not None
    
    @pytest.mark.asyncio
    async def test_email_processing_pipeline(self, orchestrator_with_mocks, sample_email):
        """Test complete email processing pipeline"""
        orchestrator = orchestrator_with_mocks
        
        # Mock workflow and automation agents to return success
        orchestrator.agents["workflow_orchestration"].execute_task = AsyncMock(
            return_value=AgentResult(
                success=True,
                data={
                    "workflow_id": "test_workflow",
                    "status": "completed",
                    "steps": [
                        {"step_id": "classify", "status": "completed"},
                        {"step_id": "tag", "status": "completed"},
                        {"step_id": "embed", "status": "completed"}
                    ]
                },
                confidence=1.0,
                processing_time=0.5
            )
        )
        
        orchestrator.agents["task_automation"].execute_task = AsyncMock(
            return_value=AgentResult(
                success=True,
                data={
                    "rules_processed": 3,
                    "rules_matched": 1,
                    "actions_executed": 2
                },
                confidence=1.0,
                processing_time=0.1
            )
        )
        
        orchestrator.agents["notification_agent"].execute_task = AsyncMock(
            return_value=AgentResult(
                success=True,
                data={"notifications_sent": 1},
                confidence=1.0,
                processing_time=0.05
            )
        )
        
        # Process email
        result = await orchestrator.process_email(sample_email)
        
        # Verify results
        assert result["success"] is True
        assert result["email_id"] == "test_email_123"
        assert "processing_timestamp" in result
        assert "automation" in result
        assert "workflow" in result
        
        # Verify that agents were called
        orchestrator.agents["task_automation"].execute_task.assert_called_once()
        orchestrator.agents["workflow_orchestration"].execute_task.assert_called_once()
        orchestrator.agents["notification_agent"].execute_task.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_workflow_execution(self, orchestrator_with_mocks):
        """Test workflow execution through orchestrator"""
        orchestrator = orchestrator_with_mocks
        
        # Mock workflow agent
        mock_workflow_result = {
            "success": True,
            "workflow_id": "smart_reply_test",
            "status": "completed",
            "steps": [
                {"step_id": "context_analysis", "status": "completed"},
                {"step_id": "reply_generation", "status": "completed"}
            ]
        }
        
        orchestrator.agents["workflow_orchestration"].execute_task = AsyncMock(
            return_value=AgentResult(
                success=True,
                data=mock_workflow_result,
                confidence=1.0,
                processing_time=0.3
            )
        )
        
        # Execute workflow
        result = await orchestrator.execute_workflow(
            "smart_reply", 
            {"email_id": "test_123", "context": "meeting request"}
        )
        
        # Verify results
        assert result["success"] is True
        assert result["workflow_id"] == "smart_reply_test"
        assert result["status"] == "completed"
    
    @pytest.mark.asyncio
    async def test_reminder_creation(self, orchestrator_with_mocks):
        """Test reminder creation through orchestrator"""
        orchestrator = orchestrator_with_mocks
        
        # Mock scheduling agent
        orchestrator.agents["scheduling_agent"].execute_task = AsyncMock(
            return_value=AgentResult(
                success=True,
                data={
                    "reminder_id": "reminder_123",
                    "reminder_time": "2024-01-16T10:30:00Z",
                    "message": "Reminder created"
                },
                confidence=1.0,
                processing_time=0.02
            )
        )
        
        # Create reminder
        result = await orchestrator.create_reminder(
            email_id="email_123",
            user_id="user_123", 
            reminder_time="2024-01-16T10:30:00Z",
            message="Follow up on project"
        )
        
        # Verify results
        assert result["reminder_id"] == "reminder_123"
        assert "reminder_time" in result
    
    @pytest.mark.asyncio
    async def test_notification_sending(self, orchestrator_with_mocks):
        """Test notification sending through orchestrator"""
        orchestrator = orchestrator_with_mocks
        
        # Mock notification agent
        orchestrator.agents["notification_agent"].execute_task = AsyncMock(
            return_value=AgentResult(
                success=True,
                data={
                    "notification_id": "notif_123",
                    "message": "Notification queued for sending"
                },
                confidence=1.0,
                processing_time=0.01
            )
        )
        
        # Send notification
        notification_data = {
            "title": "Test Notification",
            "message": "This is a test",
            "priority": "normal",
            "channels": ["in_app"],
            "user_id": "user_123"
        }
        
        result = await orchestrator.send_notification(notification_data)
        
        # Verify results
        assert result["notification_id"] == "notif_123"
    
    @pytest.mark.asyncio
    async def test_event_publishing_and_subscription(self, orchestrator_with_mocks):
        """Test event publishing and subscription system"""
        orchestrator = orchestrator_with_mocks
        
        # Set up event subscriber
        received_events = []
        
        async def event_handler(event_data):
            received_events.append(event_data)
        
        orchestrator.subscribe_event("test_event", event_handler)
        
        # Publish event
        test_data = {"message": "test event data"}
        await orchestrator.publish_event("test_event", test_data)
        
        # Give some time for async processing
        await asyncio.sleep(0.1)
        
        # Verify event was received
        assert len(received_events) == 1
        assert received_events[0] == test_data
    
    @pytest.mark.asyncio
    async def test_system_status_reporting(self, orchestrator_with_mocks):
        """Test system status reporting"""
        orchestrator = orchestrator_with_mocks
        
        status = orchestrator.get_system_status()
        
        assert "timestamp" in status
        assert "agents" in status
        assert "queue_size" in status
        assert "cache_size" in status
        
        # Check that all agents report status
        for agent_name in orchestrator.agents.keys():
            assert agent_name in status["agents"]
    
    @pytest.mark.asyncio
    async def test_error_handling_in_email_processing(self, orchestrator_with_mocks, sample_email):
        """Test error handling when agents fail during email processing"""
        orchestrator = orchestrator_with_mocks
        
        # Mock automation agent to fail
        orchestrator.agents["task_automation"].execute_task = AsyncMock(
            return_value=AgentResult(
                success=False,
                data={},
                confidence=0.0,
                processing_time=0.1,
                error_message="Automation failed"
            )
        )
        
        # Mock workflow agent to succeed
        orchestrator.agents["workflow_orchestration"].execute_task = AsyncMock(
            return_value=AgentResult(
                success=True,
                data={"workflow_id": "test", "status": "completed"},
                confidence=1.0,
                processing_time=0.2
            )
        )
        
        # Mock notification agent
        orchestrator.agents["notification_agent"].execute_task = AsyncMock(
            return_value=AgentResult(success=True, data={}, confidence=1.0, processing_time=0.01)
        )
        
        # Process email
        result = await orchestrator.process_email(sample_email)
        
        # Should report partial failure
        assert result["success"] is False  # Overall failed due to automation failure
        assert "error" in result["automation"]
        assert result["automation"]["error"] == "Automation failed"
        assert result["workflow"]["workflow_id"] == "test"  # Workflow succeeded
    
    @pytest.mark.asyncio
    async def test_cache_functionality(self, orchestrator_with_mocks, sample_email):
        """Test that results are cached properly"""
        orchestrator = orchestrator_with_mocks
        
        # Mock agents for successful processing
        orchestrator.agents["task_automation"].execute_task = AsyncMock(
            return_value=AgentResult(success=True, data={}, confidence=1.0, processing_time=0.1)
        )
        orchestrator.agents["workflow_orchestration"].execute_task = AsyncMock(
            return_value=AgentResult(success=True, data={"status": "completed"}, confidence=1.0, processing_time=0.2)
        )
        orchestrator.agents["notification_agent"].execute_task = AsyncMock(
            return_value=AgentResult(success=True, data={}, confidence=1.0, processing_time=0.01)
        )
        
        # Process email
        result = await orchestrator.process_email(sample_email)
        
        # Check that result is cached
        email_id = sample_email["id"]
        assert email_id in orchestrator.results_cache
        assert orchestrator.results_cache[email_id]["email_id"] == email_id
    
    @pytest.mark.asyncio
    async def test_agent_cross_communication(self):
        """Test that agents can communicate with each other through orchestrator"""
        # This test verifies that the orchestrator properly wires agents together
        # The workflow orchestration agent should be able to call other agents
        
        config = {
            "workflow": {"max_parallel": 3},
            "automation": {"default_rules": True}
        }
        
        with patch.multiple(
            'src.ai.orchestrator',
            EmailClassifierAgent=MockEmailClassifier,
            SearchAgent=MockSearchAgent,
            TaggingAgent=MockTaggingAgent,
            SummaryAgent=MagicMock,
            ResponseAgent=MagicMock
        ):
            # Create orchestrator (this will wire agents together)
            orchestrator = AgentOrchestrator(config)
            
            # Verify that workflow agent has access to other agents
            workflow_agent = orchestrator.agents["workflow_orchestration"]
            
            # The workflow agent should have registered other agents
            assert hasattr(workflow_agent, 'agent_registry')
            # Note: The actual wiring happens in the real implementation
            # This test verifies the structure is in place
    
    @pytest.mark.asyncio 
    async def test_graceful_shutdown(self, orchestrator_with_mocks):
        """Test graceful shutdown of orchestrator"""
        orchestrator = orchestrator_with_mocks
        
        # Mock agent shutdown methods
        for agent in orchestrator.agents.values():
            agent.shutdown = AsyncMock()
        
        # Shutdown orchestrator
        await orchestrator.shutdown()
        
        # Verify all agents were shut down
        for agent in orchestrator.agents.values():
            agent.shutdown.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__])