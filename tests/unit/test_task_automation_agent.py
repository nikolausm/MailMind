"""
Unit tests for TaskAutomationAgent
"""

import pytest
from datetime import datetime
from unittest.mock import AsyncMock, patch

from src.ai.agents.task_automation_agent import (
    TaskAutomationAgent, Rule, RuleType, ActionType, Condition, RuleExecution
)
from src.ai.agents.base_agent import AgentTask, AgentResult


class TestTaskAutomationAgent:
    """Test cases for TaskAutomationAgent"""
    
    @pytest.fixture
    def agent(self):
        """Create task automation agent"""
        return TaskAutomationAgent()
    
    @pytest.fixture
    def sample_email(self):
        """Sample email data for testing"""
        return {
            "id": "email_123",
            "subject": "Important meeting tomorrow",
            "sender_email": "boss@company.com",
            "recipient_email": "user@company.com",
            "content": "Please prepare the quarterly report for our meeting tomorrow.",
            "attachments": 1,
            "sender_reputation": 0.9,
            "received_at": "2024-01-15T10:30:00Z"
        }
    
    def test_agent_initialization(self, agent):
        """Test agent initialization with default rules"""
        assert agent.agent_name == "task_automation"
        assert len(agent.rules) > 0
        assert "spam_filter" in agent.rules
        assert "vip_priority" in agent.rules
        assert "invoice_processing" in agent.rules
        assert len(agent.execution_history) == 0
    
    def test_supported_task_types(self, agent):
        """Test supported task types"""
        supported_types = agent.get_supported_task_types()
        
        expected_types = [
            "apply_rules",
            "create_rule",
            "update_rule",
            "delete_rule",
            "get_rules",
            "extract_action_items"
        ]
        
        for task_type in expected_types:
            assert task_type in supported_types
    
    @pytest.mark.asyncio
    async def test_apply_rules_success(self, agent, sample_email):
        """Test successful rule application"""
        task = AgentTask(
            task_id="apply_rules_test",
            task_type="apply_rules",
            payload={"email_data": sample_email}
        )
        
        result = await agent.execute_task(task)
        
        assert result.success is True
        assert "rules_processed" in result.data
        assert "rules_matched" in result.data
        assert "actions_executed" in result.data
        assert result.data["email_id"] == "email_123"
    
    @pytest.mark.asyncio
    async def test_vip_rule_matching(self, agent, sample_email):
        """Test VIP rule matching"""
        # Email from VIP sender should match VIP rule
        task = AgentTask(
            task_id="vip_test",
            task_type="apply_rules",
            payload={"email_data": sample_email}
        )
        
        result = await agent.execute_task(task)
        
        # Check if VIP rule was matched
        vip_execution = None
        for execution in result.data["executions"]:
            if execution["rule_id"] == "vip_priority":
                vip_execution = execution
                break
        
        assert vip_execution is not None
        assert vip_execution["matched"] is True
        assert "set_priority" in vip_execution["actions"]
    
    @pytest.mark.asyncio
    async def test_spam_filter_rule(self, agent):
        """Test spam filter rule"""
        spam_email = {
            "id": "spam_email",
            "subject": "URGENT! You are a winner! Click here now!",
            "sender_email": "spam@suspicious.com",
            "sender_reputation": 0.1,
            "content": "Congratulations! You have won $1,000,000!"
        }
        
        task = AgentTask(
            task_id="spam_test",
            task_type="apply_rules",
            payload={"email_data": spam_email}
        )
        
        result = await agent.execute_task(task)
        
        # Check if spam rule was matched
        spam_execution = None
        for execution in result.data["executions"]:
            if execution["rule_id"] == "spam_filter":
                spam_execution = execution
                break
        
        assert spam_execution is not None
        assert spam_execution["matched"] is True
        assert "add_tag" in spam_execution["actions"]
    
    @pytest.mark.asyncio
    async def test_create_rule(self, agent):
        """Test creating a new rule"""
        rule_data = {
            "rule_id": "test_rule",
            "name": "Test Rule",
            "description": "A test rule",
            "rule_type": "filter",
            "conditions": [
                {
                    "field": "subject",
                    "condition": "contains",
                    "value": "test",
                    "case_sensitive": False
                }
            ],
            "actions": [
                {
                    "type": "add_tag",
                    "value": "test_tag"
                }
            ],
            "priority": 5,
            "enabled": True
        }
        
        task = AgentTask(
            task_id="create_rule_test",
            task_type="create_rule",
            payload={"rule_data": rule_data}
        )
        
        result = await agent.execute_task(task)
        
        assert result.success is True
        assert result.data["rule_id"] == "test_rule"
        assert "test_rule" in agent.rules
        
        # Verify rule properties
        created_rule = agent.rules["test_rule"]
        assert created_rule.name == "Test Rule"
        assert created_rule.rule_type == RuleType.FILTER
        assert created_rule.enabled is True
    
    @pytest.mark.asyncio
    async def test_update_rule(self, agent):
        """Test updating an existing rule"""
        # First create a rule
        agent.rules["update_test"] = Rule(
            rule_id="update_test",
            name="Original Name",
            description="Original description",
            rule_type=RuleType.FILTER,
            conditions=[],
            actions=[],
            enabled=True
        )
        
        # Update the rule
        task = AgentTask(
            task_id="update_rule_test",
            task_type="update_rule",
            payload={
                "rule_id": "update_test",
                "updates": {
                    "name": "Updated Name",
                    "enabled": False
                }
            }
        )
        
        result = await agent.execute_task(task)
        
        assert result.success is True
        
        # Verify updates
        updated_rule = agent.rules["update_test"]
        assert updated_rule.name == "Updated Name"
        assert updated_rule.enabled is False
        assert updated_rule.description == "Original description"  # Unchanged
    
    @pytest.mark.asyncio
    async def test_delete_rule(self, agent):
        """Test deleting a rule"""
        # Add a rule to delete
        agent.rules["delete_test"] = Rule(
            rule_id="delete_test",
            name="To Delete",
            description="",
            rule_type=RuleType.FILTER,
            conditions=[],
            actions=[]
        )
        
        task = AgentTask(
            task_id="delete_rule_test",
            task_type="delete_rule",
            payload={"rule_id": "delete_test"}
        )
        
        result = await agent.execute_task(task)
        
        assert result.success is True
        assert "delete_test" not in agent.rules
    
    @pytest.mark.asyncio
    async def test_get_rules(self, agent):
        """Test getting rules"""
        task = AgentTask(
            task_id="get_rules_test",
            task_type="get_rules",
            payload={}
        )
        
        result = await agent.execute_task(task)
        
        assert result.success is True
        assert "rules" in result.data
        assert len(result.data["rules"]) > 0
        
        # Check that default rules are present
        assert "spam_filter" in result.data["rules"]
        assert "vip_priority" in result.data["rules"]
    
    @pytest.mark.asyncio
    async def test_extract_action_items(self, agent):
        """Test extracting action items from email content"""
        email_content = """
        Hi team,
        
        Please review the attached document by Friday.
        We need to finalize the budget by next week.
        
        Action items:
        - Complete the quarterly review
        - Schedule a meeting with the client
        
        Deadline: Submit all reports by December 15th.
        
        Thanks!
        """
        
        task = AgentTask(
            task_id="extract_actions_test",
            task_type="extract_action_items",
            payload={"email_content": email_content}
        )
        
        result = await agent.execute_task(task)
        
        assert result.success is True
        assert "action_items" in result.data
        assert result.data["count"] > 0
        
        # Check that some action items were found
        action_items = result.data["action_items"]
        assert len(action_items) > 0
        
        # Look for specific patterns
        action_texts = [item["text"] for item in action_items]
        assert any("review" in text.lower() for text in action_texts)
    
    def test_condition_handlers(self, agent):
        """Test individual condition handlers"""
        # Test contains condition
        assert agent._condition_contains("Hello World", "hello", {"case_sensitive": False}) is True
        assert agent._condition_contains("Hello World", "hello", {"case_sensitive": True}) is False
        assert agent._condition_contains("Hello World", "xyz", {"case_sensitive": False}) is False
        
        # Test equals condition
        assert agent._condition_equals("test", "test", {"case_sensitive": True}) is True
        assert agent._condition_equals("Test", "test", {"case_sensitive": False}) is True
        assert agent._condition_equals("Test", "test", {"case_sensitive": True}) is False
        
        # Test regex match
        assert agent._condition_regex_match("test123", r"\d+", {}) is True
        assert agent._condition_regex_match("testABC", r"\d+", {}) is False
        
        # Test numeric conditions
        assert agent._condition_greater_than(10, 5, {}) is True
        assert agent._condition_greater_than(3, 5, {}) is False
        assert agent._condition_less_than(3, 5, {}) is True
        assert agent._condition_less_than(10, 5, {}) is False
        
        # Test list conditions
        assert agent._condition_in_list("apple", ["apple", "banana"], {}) is True
        assert agent._condition_in_list("orange", ["apple", "banana"], {}) is False
        assert agent._condition_not_in_list("orange", ["apple", "banana"], {}) is True
    
    @pytest.mark.asyncio
    async def test_field_value_extraction(self, agent):
        """Test extracting field values from nested data"""
        test_data = {
            "sender": {
                "email": "test@example.com",
                "name": "Test User"
            },
            "subject": "Test Subject",
            "metadata": {
                "priority": "high",
                "tags": ["important", "urgent"]
            }
        }
        
        # Test simple field
        assert agent._get_field_value(test_data, "subject") == "Test Subject"
        
        # Test nested field
        assert agent._get_field_value(test_data, "sender.email") == "test@example.com"
        assert agent._get_field_value(test_data, "sender.name") == "Test User"
        
        # Test non-existent field
        assert agent._get_field_value(test_data, "nonexistent") is None
        assert agent._get_field_value(test_data, "sender.nonexistent") is None
    
    @pytest.mark.asyncio
    async def test_rule_execution_metrics(self, agent, sample_email):
        """Test that rule execution metrics are recorded"""
        initial_count = len(agent.execution_history)
        
        task = AgentTask(
            task_id="metrics_test",
            task_type="apply_rules",
            payload={"email_data": sample_email}
        )
        
        result = await agent.execute_task(task)
        
        # Check that execution history was recorded
        assert len(agent.execution_history) > initial_count
        
        # Check that rule execution counts were updated
        vip_rule = agent.rules["vip_priority"]
        if any(ex.rule_id == "vip_priority" and ex.matched for ex in agent.execution_history):
            assert vip_rule.execution_count > 0
            assert vip_rule.last_executed is not None
    
    @pytest.mark.asyncio
    async def test_invalid_task_type(self, agent):
        """Test handling of invalid task types"""
        task = AgentTask(
            task_id="invalid_test",
            task_type="invalid_task_type",
            payload={}
        )
        
        result = await agent.execute_task(task)
        
        assert result.success is False
        assert "Unknown task type" in result.error_message
    
    @pytest.mark.asyncio
    async def test_empty_email_data(self, agent):
        """Test handling of empty email data"""
        task = AgentTask(
            task_id="empty_test",
            task_type="apply_rules",
            payload={}
        )
        
        result = await agent.execute_task(task)
        
        assert result.success is False
        assert "No email data provided" in result.error_message


if __name__ == "__main__":
    pytest.main([__file__])