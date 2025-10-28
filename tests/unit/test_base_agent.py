"""
Unit tests for BaseAgent class
"""

import pytest
import asyncio
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

from src.ai.agents.base_agent import (
    BaseAgent, AgentTask, AgentResult, AgentStatus, TaskPriority
)


class TestableAgent(BaseAgent):
    """Test implementation of BaseAgent"""
    
    def __init__(self, agent_name: str = "test_agent", config: dict = None):
        super().__init__(agent_name, config)
        self.process_task_mock = AsyncMock()
    
    async def process_task(self, task: AgentTask) -> AgentResult:
        """Mock implementation for testing"""
        return await self.process_task_mock(task)
    
    def get_supported_task_types(self) -> list:
        return ["test_task", "mock_task", "error_task"]


class TestBaseAgent:
    """Test cases for BaseAgent"""
    
    @pytest.fixture
    def agent(self):
        """Create a test agent instance"""
        return TestableAgent()
    
    @pytest.fixture
    def sample_task(self):
        """Create a sample task for testing"""
        return AgentTask(
            task_id="test_task_1",
            task_type="test_task",
            payload={"test": "data"},
            priority=TaskPriority.NORMAL
        )
    
    def test_agent_initialization(self):
        """Test agent initialization"""
        agent = TestableAgent("test_agent", {"key": "value"})
        
        assert agent.agent_name == "test_agent"
        assert agent.config == {"key": "value"}
        assert agent.status == AgentStatus.IDLE
        assert agent.metrics["tasks_processed"] == 0
        assert agent.metrics["tasks_failed"] == 0
    
    def test_agent_health_status(self, agent):
        """Test health status reporting"""
        health = agent.get_health_status()
        
        assert health["agent_name"] == "test_agent"
        assert health["status"] == AgentStatus.IDLE.value
        assert health["supported_tasks"] == ["test_task", "mock_task", "error_task"]
        assert "metrics" in health
        assert "config" in health
    
    @pytest.mark.asyncio
    async def test_successful_task_execution(self, agent, sample_task):
        """Test successful task execution"""
        # Setup mock to return successful result
        expected_result = AgentResult(
            success=True,
            data={"result": "success"},
            confidence=0.9,
            processing_time=0.1
        )
        agent.process_task_mock.return_value = expected_result
        
        # Execute task
        result = await agent.execute_task(sample_task)
        
        # Verify results
        assert result.success is True
        assert result.data == {"result": "success"}
        assert result.confidence == 0.9
        assert result.processing_time > 0
        assert agent.metrics["tasks_processed"] == 1
        assert agent.metrics["tasks_failed"] == 0
        assert agent.status == AgentStatus.IDLE
    
    @pytest.mark.asyncio
    async def test_failed_task_execution(self, agent, sample_task):
        """Test failed task execution"""
        # Setup mock to raise exception
        agent.process_task_mock.side_effect = Exception("Test error")
        
        # Execute task
        result = await agent.execute_task(sample_task)
        
        # Verify results
        assert result.success is False
        assert "Test error" in result.error_message
        assert agent.metrics["tasks_processed"] == 0
        assert agent.metrics["tasks_failed"] == 1
        assert agent.status == AgentStatus.ERROR
    
    @pytest.mark.asyncio
    async def test_task_timeout(self, agent):
        """Test task timeout handling"""
        # Create task with short timeout
        task = AgentTask(
            task_id="timeout_task",
            task_type="test_task",
            payload={},
            timeout=1  # 1 second timeout
        )
        
        # Setup mock to simulate long-running task
        async def slow_task(task):
            await asyncio.sleep(2)  # Takes longer than timeout
            return AgentResult(True, {}, 1.0, 2.0)
        
        agent.process_task_mock.side_effect = slow_task
        
        # Execute task
        result = await agent.execute_task(task)
        
        # Verify timeout handling
        assert result.success is False
        assert "timed out" in result.error_message
        assert agent.metrics["tasks_failed"] == 1
        assert agent.status == AgentStatus.ERROR
    
    @pytest.mark.asyncio
    async def test_unsupported_task_type(self, agent):
        """Test handling of unsupported task types"""
        task = AgentTask(
            task_id="unsupported_task",
            task_type="unsupported_type",
            payload={}
        )
        
        # Execute task
        result = await agent.execute_task(task)
        
        # Verify error handling
        assert result.success is False
        assert "Unsupported task type" in result.error_message
        assert agent.metrics["tasks_failed"] == 1
    
    @pytest.mark.asyncio
    async def test_metrics_calculation(self, agent):
        """Test metrics calculation and averaging"""
        # Execute multiple successful tasks
        for i in range(3):
            task = AgentTask(f"task_{i}", "test_task", {})
            agent.process_task_mock.return_value = AgentResult(
                True, {}, 1.0, 0.1 * (i + 1)  # Different processing times
            )
            await agent.execute_task(task)
        
        # Verify metrics
        assert agent.metrics["tasks_processed"] == 3
        assert agent.metrics["tasks_failed"] == 0
        assert agent.metrics["average_processing_time"] > 0
        assert agent.metrics["last_activity"] is not None
    
    def test_config_update(self, agent):
        """Test configuration updates"""
        new_config = {"new_key": "new_value", "existing": "updated"}
        agent.update_config(new_config)
        
        assert agent.config["new_key"] == "new_value"
        assert agent.config["existing"] == "updated"
    
    @pytest.mark.asyncio
    async def test_graceful_shutdown(self, agent):
        """Test graceful shutdown"""
        # Start with processing status
        agent.status = AgentStatus.PROCESSING
        
        # Start shutdown in background
        shutdown_task = asyncio.create_task(agent.shutdown())
        
        # Wait a bit then set to idle
        await asyncio.sleep(0.1)
        agent.status = AgentStatus.IDLE
        
        # Wait for shutdown to complete
        await shutdown_task
        
        assert agent.status == AgentStatus.MAINTENANCE


class TestAgentTask:
    """Test cases for AgentTask"""
    
    def test_task_creation(self):
        """Test task creation with defaults"""
        task = AgentTask(
            task_id="test_id",
            task_type="test_type",
            payload={"key": "value"}
        )
        
        assert task.task_id == "test_id"
        assert task.task_type == "test_type"
        assert task.payload == {"key": "value"}
        assert task.priority == TaskPriority.NORMAL
        assert isinstance(task.created_at, datetime)
        assert task.timeout == 300
    
    def test_task_with_custom_values(self):
        """Test task creation with custom values"""
        custom_time = datetime.utcnow()
        task = AgentTask(
            task_id="custom_id",
            task_type="custom_type",
            payload={},
            priority=TaskPriority.HIGH,
            created_at=custom_time,
            timeout=60
        )
        
        assert task.priority == TaskPriority.HIGH
        assert task.created_at == custom_time
        assert task.timeout == 60


class TestAgentResult:
    """Test cases for AgentResult"""
    
    def test_successful_result(self):
        """Test successful result creation"""
        result = AgentResult(
            success=True,
            data={"output": "value"},
            confidence=0.95,
            processing_time=1.5
        )
        
        assert result.success is True
        assert result.data == {"output": "value"}
        assert result.confidence == 0.95
        assert result.processing_time == 1.5
        assert result.error_message is None
        assert result.metadata is None
    
    def test_failed_result(self):
        """Test failed result creation"""
        result = AgentResult(
            success=False,
            data={},
            confidence=0.0,
            processing_time=0.5,
            error_message="Processing failed",
            metadata={"attempt": 1}
        )
        
        assert result.success is False
        assert result.error_message == "Processing failed"
        assert result.metadata == {"attempt": 1}


if __name__ == "__main__":
    pytest.main([__file__])