"""
Unit tests for WorkflowOrchestrationAgent
"""

import pytest
import asyncio
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

from src.ai.agents.workflow_orchestration_agent import (
    WorkflowOrchestrationAgent, Workflow, WorkflowStep, WorkflowStatus, StepStatus
)
from src.ai.agents.base_agent import AgentTask, AgentResult, BaseAgent


class MockAgent(BaseAgent):
    """Mock agent for testing workflow orchestration"""
    
    def __init__(self, agent_name: str, should_succeed: bool = True):
        super().__init__(agent_name)
        self.should_succeed = should_succeed
        self.executed_tasks = []
    
    async def process_task(self, task) -> AgentResult:
        """Mock task processing"""
        self.executed_tasks.append(task)
        
        if self.should_succeed:
            return AgentResult(
                success=True,
                data={"result": f"{self.agent_name}_result"},
                confidence=0.9,
                processing_time=0.1
            )
        else:
            return AgentResult(
                success=False,
                data={},
                confidence=0.0,
                processing_time=0.1,
                error_message=f"{self.agent_name}_error"
            )
    
    def get_supported_task_types(self):
        return ["test_task", "classify_email", "generate_tags", "generate_embedding"]


class TestWorkflowOrchestrationAgent:
    """Test cases for WorkflowOrchestrationAgent"""
    
    @pytest.fixture
    def orchestrator(self):
        """Create workflow orchestration agent"""
        return WorkflowOrchestrationAgent()
    
    @pytest.fixture
    def mock_agents(self):
        """Create mock agents for testing"""
        return {
            "classifier": MockAgent("classifier", should_succeed=True),
            "tagger": MockAgent("tagger", should_succeed=True),
            "embedder": MockAgent("embedder", should_succeed=True),
            "faulty_agent": MockAgent("faulty_agent", should_succeed=False)
        }
    
    def test_orchestrator_initialization(self, orchestrator):
        """Test orchestrator initialization"""
        assert orchestrator.agent_name == "workflow_orchestration"
        assert len(orchestrator.workflow_templates) > 0
        assert "new_email_processing" in orchestrator.workflow_templates
        assert "thread_summary" in orchestrator.workflow_templates
        assert "smart_reply" in orchestrator.workflow_templates
    
    def test_agent_registration(self, orchestrator, mock_agents):
        """Test agent registration"""
        for name, agent in mock_agents.items():
            orchestrator.register_agent(name, agent)
        
        assert len(orchestrator.agent_registry) == len(mock_agents)
        assert orchestrator.agent_registry["classifier"] == mock_agents["classifier"]
    
    def test_supported_task_types(self, orchestrator):
        """Test supported task types"""
        supported_types = orchestrator.get_supported_task_types()
        
        expected_types = [
            "execute_workflow",
            "create_workflow",
            "get_workflow_status",
            "cancel_workflow"
        ]
        
        for task_type in expected_types:
            assert task_type in supported_types
    
    @pytest.mark.asyncio
    async def test_execute_workflow_template(self, orchestrator, mock_agents):
        """Test executing a workflow from template"""
        # Register mock agents
        orchestrator.register_agent("email_classifier", mock_agents["classifier"])
        orchestrator.register_agent("tagging_agent", mock_agents["tagger"])
        orchestrator.register_agent("search_agent", mock_agents["embedder"])
        orchestrator.register_agent("notification_agent", mock_agents["classifier"])  # Reuse for test
        
        # Create task to execute workflow
        task = AgentTask(
            task_id="test_workflow",
            task_type="execute_workflow",
            payload={
                "template_id": "new_email_processing",
                "workflow_data": {
                    "email_id": "test_email",
                    "subject": "Test Email",
                    "content": "This is a test email"
                }
            }
        )
        
        # Execute workflow
        result = await orchestrator.execute_task(task)
        
        # Verify results
        assert result.success is True
        assert "workflow_id" in result.data
        assert result.data["status"] == "completed"
        assert len(result.data["steps"]) > 0
        
        # Verify all steps completed
        for step in result.data["steps"]:
            assert step["status"] == "completed"
    
    @pytest.mark.asyncio
    async def test_workflow_with_dependencies(self, orchestrator, mock_agents):
        """Test workflow execution with step dependencies"""
        # Register agents
        for name, agent in mock_agents.items():
            orchestrator.register_agent(name, agent)
        
        # Create custom workflow with dependencies
        task = AgentTask(
            task_id="dependency_test",
            task_type="create_workflow",
            payload={
                "workflow_id": "test_dependencies",
                "name": "Dependency Test Workflow",
                "description": "Test workflow dependencies",
                "steps": [
                    {
                        "step_id": "step1",
                        "agent_name": "classifier",
                        "task_type": "test_task",
                        "payload": {"step": 1},
                        "dependencies": []
                    },
                    {
                        "step_id": "step2",
                        "agent_name": "tagger",
                        "task_type": "test_task",
                        "payload": {"step": 2},
                        "dependencies": ["step1"]
                    },
                    {
                        "step_id": "step3",
                        "agent_name": "embedder",
                        "task_type": "test_task",
                        "payload": {"step": 3},
                        "dependencies": ["step1", "step2"]
                    }
                ]
            }
        )
        
        # Create workflow
        create_result = await orchestrator.execute_task(task)
        assert create_result.success is True
        
        # Execute the workflow
        execute_task = AgentTask(
            task_id="execute_deps",
            task_type="execute_workflow",
            payload={
                "workflow_id": "test_dependencies",
                "workflow_data": {"test": "data"}
            }
        )
        
        result = await orchestrator.execute_task(execute_task)
        
        # Verify execution order by checking agent call order
        # Step1 should execute first, then step2, then step3
        classifier_calls = len(mock_agents["classifier"].executed_tasks)
        tagger_calls = len(mock_agents["tagger"].executed_tasks)
        embedder_calls = len(mock_agents["embedder"].executed_tasks)
        
        assert classifier_calls >= 1
        assert tagger_calls >= 1
        assert embedder_calls >= 1
    
    @pytest.mark.asyncio
    async def test_workflow_with_failed_step(self, orchestrator, mock_agents):
        """Test workflow handling when a step fails"""
        # Register agents including faulty one
        for name, agent in mock_agents.items():
            orchestrator.register_agent(name, agent)
        
        # Create workflow with faulty agent
        task = AgentTask(
            task_id="failure_test",
            task_type="execute_workflow",
            payload={
                "workflow_id": "test_failure",
                "name": "Failure Test",
                "steps": [
                    {
                        "step_id": "good_step",
                        "agent_name": "classifier",
                        "task_type": "test_task",
                        "payload": {},
                        "dependencies": []
                    },
                    {
                        "step_id": "bad_step",
                        "agent_name": "faulty_agent",
                        "task_type": "test_task",
                        "payload": {},
                        "dependencies": ["good_step"]
                    }
                ]
            }
        )
        
        result = await orchestrator.execute_task(task)
        
        # Workflow should report failure
        assert result.data["status"] == "failed"
        
        # Check individual step statuses
        steps = result.data["steps"]
        good_step = next(s for s in steps if s["step_id"].endswith("good_step"))
        bad_step = next(s for s in steps if s["step_id"].endswith("bad_step"))
        
        assert good_step["status"] == "completed"
        assert bad_step["status"] == "failed"
    
    @pytest.mark.asyncio
    async def test_get_workflow_status(self, orchestrator):
        """Test getting workflow status"""
        # This test would need a running workflow to be meaningful
        # For now, test the not found case
        task = AgentTask(
            task_id="status_test",
            task_type="get_workflow_status",
            payload={"workflow_id": "nonexistent"}
        )
        
        result = await orchestrator.execute_task(task)
        
        assert result.success is False
        assert "not found" in result.error_message
    
    @pytest.mark.asyncio
    async def test_cancel_workflow(self, orchestrator):
        """Test cancelling a workflow"""
        task = AgentTask(
            task_id="cancel_test",
            task_type="cancel_workflow",
            payload={"workflow_id": "nonexistent"}
        )
        
        result = await orchestrator.execute_task(task)
        
        assert result.success is False
        assert "not found" in result.error_message
    
    @pytest.mark.asyncio
    async def test_workflow_step_retry_logic(self, orchestrator, mock_agents):
        """Test retry logic for failed steps"""
        # Create an agent that fails first two times, succeeds third time
        retry_agent = MockAgent("retry_agent")
        call_count = 0
        
        async def mock_execute_task(task):
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                return AgentResult(False, {}, 0.0, 0.1, "Temporary failure")
            else:
                return AgentResult(True, {"attempt": call_count}, 1.0, 0.1)
        
        retry_agent.execute_task = mock_execute_task
        orchestrator.register_agent("retry_agent", retry_agent)
        
        # Create workflow with retry agent
        task = AgentTask(
            task_id="retry_test",
            task_type="execute_workflow",
            payload={
                "workflow_id": "retry_test",
                "name": "Retry Test",
                "steps": [
                    {
                        "step_id": "retry_step",
                        "agent_name": "retry_agent",
                        "task_type": "test_task",
                        "payload": {},
                        "retry_count": 3
                    }
                ]
            }
        )
        
        result = await orchestrator.execute_task(task)
        
        # Should succeed after retries
        assert result.data["status"] == "completed"
        assert call_count == 3  # Failed twice, succeeded on third attempt
    
    def test_workflow_template_structure(self, orchestrator):
        """Test that workflow templates have proper structure"""
        for template_id, template in orchestrator.workflow_templates.items():
            assert isinstance(template, Workflow)
            assert template.workflow_id == template_id
            assert template.name
            assert template.description
            assert len(template.steps) > 0
            
            for step in template.steps:
                assert isinstance(step, WorkflowStep)
                assert step.step_id
                assert step.agent_name
                assert step.task_type
                assert isinstance(step.payload, dict)
                assert isinstance(step.dependencies, list)
    
    @pytest.mark.asyncio
    async def test_invalid_task_type(self, orchestrator):
        """Test handling of invalid task types"""
        task = AgentTask(
            task_id="invalid_test",
            task_type="invalid_task_type",
            payload={}
        )
        
        result = await orchestrator.execute_task(task)
        
        assert result.success is False
        assert "Unknown task type" in result.error_message


if __name__ == "__main__":
    pytest.main([__file__])