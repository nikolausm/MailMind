"""
Task Automation Agent
Handles rule-based email processing and automation tasks
"""

from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
import re
import json
import asyncio

from .base_agent import BaseAgent, AgentTask, AgentResult, TaskPriority

class RuleType(Enum):
    FILTER = "filter"
    CLASSIFICATION = "classification"
    ACTION = "action"
    CONDITIONAL = "conditional"

class ActionType(Enum):
    MOVE_TO_FOLDER = "move_to_folder"
    ADD_TAG = "add_tag"
    REMOVE_TAG = "remove_tag"
    SET_PRIORITY = "set_priority"
    MARK_READ = "mark_read"
    MARK_UNREAD = "mark_unread"
    FORWARD = "forward"
    AUTO_REPLY = "auto_reply"
    DELETE = "delete"
    ARCHIVE = "archive"
    CREATE_REMINDER = "create_reminder"
    EXTRACT_DATA = "extract_data"
    TRIGGER_WORKFLOW = "trigger_workflow"

class Condition(Enum):
    CONTAINS = "contains"
    EQUALS = "equals"
    STARTS_WITH = "starts_with"
    ENDS_WITH = "ends_with"
    REGEX_MATCH = "regex_match"
    GREATER_THAN = "greater_than"
    LESS_THAN = "less_than"
    IN_LIST = "in_list"
    NOT_IN_LIST = "not_in_list"

@dataclass
class Rule:
    """Email processing rule definition"""
    rule_id: str
    name: str
    description: str
    rule_type: RuleType
    conditions: List[Dict[str, Any]]
    actions: List[Dict[str, Any]]
    priority: int = 5
    enabled: bool = True
    created_at: datetime = None
    updated_at: datetime = None
    execution_count: int = 0
    last_executed: Optional[datetime] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.updated_at is None:
            self.updated_at = datetime.utcnow()

@dataclass
class RuleExecution:
    """Result of rule execution"""
    rule_id: str
    email_id: str
    matched: bool
    actions_executed: List[str]
    execution_time: float
    error_message: Optional[str] = None
    executed_at: datetime = None

    def __post_init__(self):
        if self.executed_at is None:
            self.executed_at = datetime.utcnow()

class TaskAutomationAgent(BaseAgent):
    """
    Handles rule-based email processing and automation
    
    Features:
    - Email filtering and classification rules
    - Automated actions (tagging, moving, replies)
    - Conditional processing logic
    - Pattern matching and regex support
    - Data extraction from emails
    - Integration with other agents
    - Performance monitoring and optimization
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__("task_automation", config)
        self.rules: Dict[str, Rule] = {}
        self.execution_history: List[RuleExecution] = []
        self.condition_handlers = self._initialize_condition_handlers()
        self.action_handlers = self._initialize_action_handlers()
        self._load_default_rules()
    
    def _initialize_condition_handlers(self) -> Dict[Condition, Callable]:
        """Initialize condition evaluation handlers"""
        return {
            Condition.CONTAINS: self._condition_contains,
            Condition.EQUALS: self._condition_equals,
            Condition.STARTS_WITH: self._condition_starts_with,
            Condition.ENDS_WITH: self._condition_ends_with,
            Condition.REGEX_MATCH: self._condition_regex_match,
            Condition.GREATER_THAN: self._condition_greater_than,
            Condition.LESS_THAN: self._condition_less_than,
            Condition.IN_LIST: self._condition_in_list,
            Condition.NOT_IN_LIST: self._condition_not_in_list
        }
    
    def _initialize_action_handlers(self) -> Dict[ActionType, Callable]:
        """Initialize action execution handlers"""
        return {
            ActionType.MOVE_TO_FOLDER: self._action_move_to_folder,
            ActionType.ADD_TAG: self._action_add_tag,
            ActionType.REMOVE_TAG: self._action_remove_tag,
            ActionType.SET_PRIORITY: self._action_set_priority,
            ActionType.MARK_READ: self._action_mark_read,
            ActionType.MARK_UNREAD: self._action_mark_unread,
            ActionType.FORWARD: self._action_forward,
            ActionType.AUTO_REPLY: self._action_auto_reply,
            ActionType.DELETE: self._action_delete,
            ActionType.ARCHIVE: self._action_archive,
            ActionType.CREATE_REMINDER: self._action_create_reminder,
            ActionType.EXTRACT_DATA: self._action_extract_data,
            ActionType.TRIGGER_WORKFLOW: self._action_trigger_workflow
        }
    
    def _load_default_rules(self):
        """Load default automation rules"""
        
        # Spam filtering rule
        spam_rule = Rule(
            rule_id="spam_filter",
            name="Spam Detection",
            description="Automatically detect and handle spam emails",
            rule_type=RuleType.FILTER,
            conditions=[
                {
                    "field": "subject",
                    "condition": Condition.REGEX_MATCH.value,
                    "value": r"(urgent|winner|congratulations|free|click here)",
                    "case_sensitive": False
                },
                {
                    "field": "sender_reputation",
                    "condition": Condition.LESS_THAN.value,
                    "value": 0.3
                }
            ],
            actions=[
                {
                    "type": ActionType.ADD_TAG.value,
                    "value": "spam"
                },
                {
                    "type": ActionType.MOVE_TO_FOLDER.value,
                    "value": "spam"
                }
            ],
            priority=1
        )
        
        # VIP email priority rule
        vip_rule = Rule(
            rule_id="vip_priority",
            name="VIP Email Priority",
            description="High priority for emails from VIP contacts",
            rule_type=RuleType.CLASSIFICATION,
            conditions=[
                {
                    "field": "sender_email",
                    "condition": Condition.IN_LIST.value,
                    "value": ["boss@company.com", "client@important.com"]
                }
            ],
            actions=[
                {
                    "type": ActionType.SET_PRIORITY.value,
                    "value": "high"
                },
                {
                    "type": ActionType.ADD_TAG.value,
                    "value": "vip"
                }
            ],
            priority=2
        )
        
        # Auto-reply for out of office
        ooo_rule = Rule(
            rule_id="out_of_office",
            name="Out of Office Auto-Reply",
            description="Send automatic replies when out of office",
            rule_type=RuleType.ACTION,
            conditions=[
                {
                    "field": "recipient_email",
                    "condition": Condition.EQUALS.value,
                    "value": "user@company.com"
                },
                {
                    "field": "is_out_of_office",
                    "condition": Condition.EQUALS.value,
                    "value": True
                }
            ],
            actions=[
                {
                    "type": ActionType.AUTO_REPLY.value,
                    "value": {
                        "template": "out_of_office",
                        "message": "Thank you for your email. I am currently out of office."
                    }
                }
            ],
            priority=3,
            enabled=False  # Disabled by default
        )
        
        # Invoice processing rule
        invoice_rule = Rule(
            rule_id="invoice_processing",
            name="Invoice Processing",
            description="Automatically process and categorize invoices",
            rule_type=RuleType.CONDITIONAL,
            conditions=[
                {
                    "field": "subject",
                    "condition": Condition.CONTAINS.value,
                    "value": "invoice",
                    "case_sensitive": False
                },
                {
                    "field": "attachments",
                    "condition": Condition.GREATER_THAN.value,
                    "value": 0
                }
            ],
            actions=[
                {
                    "type": ActionType.ADD_TAG.value,
                    "value": "invoice"
                },
                {
                    "type": ActionType.MOVE_TO_FOLDER.value,
                    "value": "finance/invoices"
                },
                {
                    "type": ActionType.EXTRACT_DATA.value,
                    "value": {
                        "fields": ["invoice_number", "amount", "due_date", "vendor"],
                        "save_to": "invoice_database"
                    }
                }
            ],
            priority=4
        )
        
        self.rules = {
            rule.rule_id: rule for rule in [spam_rule, vip_rule, ooo_rule, invoice_rule]
        }
    
    async def process_task(self, task: AgentTask) -> AgentResult:
        """Process automation tasks"""
        try:
            if task.task_type == "apply_rules":
                return await self._apply_rules(task.payload)
            elif task.task_type == "create_rule":
                return await self._create_rule(task.payload)
            elif task.task_type == "update_rule":
                return await self._update_rule(task.payload)
            elif task.task_type == "delete_rule":
                return await self._delete_rule(task.payload)
            elif task.task_type == "get_rules":
                return await self._get_rules(task.payload)
            elif task.task_type == "extract_action_items":
                return await self._extract_action_items(task.payload)
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
            "apply_rules",
            "create_rule",
            "update_rule", 
            "delete_rule",
            "get_rules",
            "extract_action_items"
        ]
    
    async def _apply_rules(self, payload: Dict[str, Any]) -> AgentResult:
        """Apply automation rules to an email"""
        email_data = payload.get("email_data", {})
        rule_ids = payload.get("rule_ids")  # Optional: specific rules to apply
        
        if not email_data:
            return AgentResult(
                success=False,
                data={},
                confidence=0.0,
                processing_time=0.0,
                error_message="No email data provided"
            )
        
        # Get applicable rules
        applicable_rules = []
        if rule_ids:
            applicable_rules = [self.rules[rid] for rid in rule_ids if rid in self.rules]
        else:
            applicable_rules = [rule for rule in self.rules.values() if rule.enabled]
        
        # Sort by priority
        applicable_rules.sort(key=lambda r: r.priority)
        
        executed_rules = []
        total_actions = 0
        
        for rule in applicable_rules:
            execution = await self._execute_rule(rule, email_data)
            executed_rules.append(execution)
            
            if execution.matched:
                total_actions += len(execution.actions_executed)
                rule.execution_count += 1
                rule.last_executed = datetime.utcnow()
        
        self.execution_history.extend(executed_rules)
        
        return AgentResult(
            success=True,
            data={
                "email_id": email_data.get("id", "unknown"),
                "rules_processed": len(applicable_rules),
                "rules_matched": len([ex for ex in executed_rules if ex.matched]),
                "actions_executed": total_actions,
                "executions": [
                    {
                        "rule_id": ex.rule_id,
                        "matched": ex.matched,
                        "actions": ex.actions_executed,
                        "execution_time": ex.execution_time
                    }
                    for ex in executed_rules
                ]
            },
            confidence=1.0,
            processing_time=sum(ex.execution_time for ex in executed_rules)
        )
    
    async def _execute_rule(self, rule: Rule, email_data: Dict[str, Any]) -> RuleExecution:
        """Execute a single rule against email data"""
        start_time = datetime.utcnow()
        
        try:
            # Evaluate conditions
            conditions_met = await self._evaluate_conditions(rule.conditions, email_data)
            
            actions_executed = []
            
            if conditions_met:
                # Execute actions
                for action in rule.actions:
                    try:
                        await self._execute_action(action, email_data)
                        actions_executed.append(action.get("type", "unknown"))
                    except Exception as e:
                        self.logger.error(f"Action execution failed: {e}")
                        # Continue with other actions
            
            execution_time = (datetime.utcnow() - start_time).total_seconds()
            
            return RuleExecution(
                rule_id=rule.rule_id,
                email_id=email_data.get("id", "unknown"),
                matched=conditions_met,
                actions_executed=actions_executed,
                execution_time=execution_time
            )
            
        except Exception as e:
            execution_time = (datetime.utcnow() - start_time).total_seconds()
            
            return RuleExecution(
                rule_id=rule.rule_id,
                email_id=email_data.get("id", "unknown"),
                matched=False,
                actions_executed=[],
                execution_time=execution_time,
                error_message=str(e)
            )
    
    async def _evaluate_conditions(self, conditions: List[Dict[str, Any]], email_data: Dict[str, Any]) -> bool:
        """Evaluate all conditions for a rule"""
        if not conditions:
            return True
        
        # All conditions must be met (AND logic)
        for condition in conditions:
            field = condition.get("field")
            condition_type = Condition(condition.get("condition"))
            value = condition.get("value")
            
            field_value = self._get_field_value(email_data, field)
            
            handler = self.condition_handlers.get(condition_type)
            if not handler:
                self.logger.warning(f"Unknown condition type: {condition_type}")
                continue
            
            if not handler(field_value, value, condition):
                return False
        
        return True
    
    def _get_field_value(self, email_data: Dict[str, Any], field: str) -> Any:
        """Extract field value from email data"""
        # Support nested field access (e.g., "sender.email")
        keys = field.split(".")
        value = email_data
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return None
        
        return value
    
    # Condition handlers
    def _condition_contains(self, field_value: Any, target_value: Any, condition: Dict[str, Any]) -> bool:
        """Check if field contains target value"""
        if field_value is None:
            return False
        
        field_str = str(field_value)
        target_str = str(target_value)
        
        if not condition.get("case_sensitive", True):
            field_str = field_str.lower()
            target_str = target_str.lower()
        
        return target_str in field_str
    
    def _condition_equals(self, field_value: Any, target_value: Any, condition: Dict[str, Any]) -> bool:
        """Check if field equals target value"""
        if not condition.get("case_sensitive", True) and isinstance(field_value, str):
            return str(field_value).lower() == str(target_value).lower()
        return field_value == target_value
    
    def _condition_starts_with(self, field_value: Any, target_value: Any, condition: Dict[str, Any]) -> bool:
        """Check if field starts with target value"""
        if field_value is None:
            return False
        
        field_str = str(field_value)
        target_str = str(target_value)
        
        if not condition.get("case_sensitive", True):
            field_str = field_str.lower()
            target_str = target_str.lower()
        
        return field_str.startswith(target_str)
    
    def _condition_ends_with(self, field_value: Any, target_value: Any, condition: Dict[str, Any]) -> bool:
        """Check if field ends with target value"""
        if field_value is None:
            return False
        
        field_str = str(field_value)
        target_str = str(target_value)
        
        if not condition.get("case_sensitive", True):
            field_str = field_str.lower()
            target_str = target_str.lower()
        
        return field_str.endswith(target_str)
    
    def _condition_regex_match(self, field_value: Any, pattern: str, condition: Dict[str, Any]) -> bool:
        """Check if field matches regex pattern"""
        if field_value is None:
            return False
        
        flags = 0
        if not condition.get("case_sensitive", True):
            flags |= re.IGNORECASE
        
        try:
            return bool(re.search(pattern, str(field_value), flags))
        except re.error:
            self.logger.error(f"Invalid regex pattern: {pattern}")
            return False
    
    def _condition_greater_than(self, field_value: Any, target_value: Any, condition: Dict[str, Any]) -> bool:
        """Check if field is greater than target value"""
        try:
            return float(field_value) > float(target_value)
        except (TypeError, ValueError):
            return False
    
    def _condition_less_than(self, field_value: Any, target_value: Any, condition: Dict[str, Any]) -> bool:
        """Check if field is less than target value"""
        try:
            return float(field_value) < float(target_value)
        except (TypeError, ValueError):
            return False
    
    def _condition_in_list(self, field_value: Any, target_list: List[Any], condition: Dict[str, Any]) -> bool:
        """Check if field value is in target list"""
        if not isinstance(target_list, list):
            return False
        
        if not condition.get("case_sensitive", True) and isinstance(field_value, str):
            return any(str(field_value).lower() == str(item).lower() for item in target_list)
        
        return field_value in target_list
    
    def _condition_not_in_list(self, field_value: Any, target_list: List[Any], condition: Dict[str, Any]) -> bool:
        """Check if field value is not in target list"""
        return not self._condition_in_list(field_value, target_list, condition)
    
    # Action handlers
    async def _execute_action(self, action: Dict[str, Any], email_data: Dict[str, Any]):
        """Execute a single action"""
        action_type = ActionType(action.get("type"))
        handler = self.action_handlers.get(action_type)
        
        if handler:
            await handler(action, email_data)
        else:
            self.logger.warning(f"Unknown action type: {action_type}")
    
    async def _action_move_to_folder(self, action: Dict[str, Any], email_data: Dict[str, Any]):
        """Move email to specified folder"""
        folder = action.get("value")
        self.logger.info(f"Moving email {email_data.get('id')} to folder: {folder}")
        # Implementation would integrate with email client API
    
    async def _action_add_tag(self, action: Dict[str, Any], email_data: Dict[str, Any]):
        """Add tag to email"""
        tag = action.get("value")
        self.logger.info(f"Adding tag '{tag}' to email {email_data.get('id')}")
        # Implementation would update email metadata
    
    async def _action_remove_tag(self, action: Dict[str, Any], email_data: Dict[str, Any]):
        """Remove tag from email"""
        tag = action.get("value")
        self.logger.info(f"Removing tag '{tag}' from email {email_data.get('id')}")
    
    async def _action_set_priority(self, action: Dict[str, Any], email_data: Dict[str, Any]):
        """Set email priority"""
        priority = action.get("value")
        self.logger.info(f"Setting priority '{priority}' for email {email_data.get('id')}")
    
    async def _action_mark_read(self, action: Dict[str, Any], email_data: Dict[str, Any]):
        """Mark email as read"""
        self.logger.info(f"Marking email {email_data.get('id')} as read")
    
    async def _action_mark_unread(self, action: Dict[str, Any], email_data: Dict[str, Any]):
        """Mark email as unread"""
        self.logger.info(f"Marking email {email_data.get('id')} as unread")
    
    async def _action_forward(self, action: Dict[str, Any], email_data: Dict[str, Any]):
        """Forward email to specified address"""
        to_address = action.get("value")
        self.logger.info(f"Forwarding email {email_data.get('id')} to {to_address}")
    
    async def _action_auto_reply(self, action: Dict[str, Any], email_data: Dict[str, Any]):
        """Send automatic reply"""
        reply_config = action.get("value", {})
        message = reply_config.get("message", "Thank you for your email.")
        self.logger.info(f"Sending auto-reply for email {email_data.get('id')}")
    
    async def _action_delete(self, action: Dict[str, Any], email_data: Dict[str, Any]):
        """Delete email"""
        self.logger.info(f"Deleting email {email_data.get('id')}")
    
    async def _action_archive(self, action: Dict[str, Any], email_data: Dict[str, Any]):
        """Archive email"""
        self.logger.info(f"Archiving email {email_data.get('id')}")
    
    async def _action_create_reminder(self, action: Dict[str, Any], email_data: Dict[str, Any]):
        """Create reminder for email"""
        reminder_config = action.get("value", {})
        reminder_time = reminder_config.get("time", "1 day")
        self.logger.info(f"Creating reminder for email {email_data.get('id')} in {reminder_time}")
    
    async def _action_extract_data(self, action: Dict[str, Any], email_data: Dict[str, Any]):
        """Extract structured data from email"""
        extraction_config = action.get("value", {})
        fields = extraction_config.get("fields", [])
        self.logger.info(f"Extracting data fields {fields} from email {email_data.get('id')}")
        # Implementation would use NLP/regex to extract data
    
    async def _action_trigger_workflow(self, action: Dict[str, Any], email_data: Dict[str, Any]):
        """Trigger a workflow"""
        workflow_id = action.get("value")
        self.logger.info(f"Triggering workflow '{workflow_id}' for email {email_data.get('id')}")
        # Implementation would call workflow orchestration agent
    
    async def _create_rule(self, payload: Dict[str, Any]) -> AgentResult:
        """Create a new automation rule"""
        try:
            rule_data = payload.get("rule_data", {})
            
            rule = Rule(
                rule_id=rule_data.get("rule_id", f"rule_{len(self.rules) + 1}"),
                name=rule_data["name"],
                description=rule_data.get("description", ""),
                rule_type=RuleType(rule_data["rule_type"]),
                conditions=rule_data.get("conditions", []),
                actions=rule_data.get("actions", []),
                priority=rule_data.get("priority", 5),
                enabled=rule_data.get("enabled", True)
            )
            
            self.rules[rule.rule_id] = rule
            
            return AgentResult(
                success=True,
                data={"rule_id": rule.rule_id, "message": "Rule created successfully"},
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
    
    async def _update_rule(self, payload: Dict[str, Any]) -> AgentResult:
        """Update an existing rule"""
        rule_id = payload.get("rule_id")
        updates = payload.get("updates", {})
        
        if rule_id not in self.rules:
            return AgentResult(
                success=False,
                data={},
                confidence=0.0,
                processing_time=0.0,
                error_message=f"Rule {rule_id} not found"
            )
        
        rule = self.rules[rule_id]
        
        # Apply updates
        for key, value in updates.items():
            if hasattr(rule, key):
                setattr(rule, key, value)
        
        rule.updated_at = datetime.utcnow()
        
        return AgentResult(
            success=True,
            data={"rule_id": rule_id, "message": "Rule updated successfully"},
            confidence=1.0,
            processing_time=0.0
        )
    
    async def _delete_rule(self, payload: Dict[str, Any]) -> AgentResult:
        """Delete a rule"""
        rule_id = payload.get("rule_id")
        
        if rule_id in self.rules:
            del self.rules[rule_id]
            return AgentResult(
                success=True,
                data={"rule_id": rule_id, "message": "Rule deleted successfully"},
                confidence=1.0,
                processing_time=0.0
            )
        else:
            return AgentResult(
                success=False,
                data={},
                confidence=0.0,
                processing_time=0.0,
                error_message=f"Rule {rule_id} not found"
            )
    
    async def _get_rules(self, payload: Dict[str, Any]) -> AgentResult:
        """Get all rules or specific rules"""
        rule_ids = payload.get("rule_ids")
        
        if rule_ids:
            rules_data = {
                rid: self.rules[rid].__dict__ for rid in rule_ids if rid in self.rules
            }
        else:
            rules_data = {rid: rule.__dict__ for rid, rule in self.rules.items()}
        
        return AgentResult(
            success=True,
            data={"rules": rules_data},
            confidence=1.0,
            processing_time=0.0
        )
    
    async def _extract_action_items(self, payload: Dict[str, Any]) -> AgentResult:
        """Extract action items from email content"""
        email_content = payload.get("email_content", "")
        
        if not email_content:
            return AgentResult(
                success=False,
                data={},
                confidence=0.0,
                processing_time=0.0,
                error_message="No email content provided"
            )
        
        # Simple pattern-based action item extraction
        # In production, this would use more sophisticated NLP
        action_patterns = [
            r"(?:please|can you|could you|need to|should|must)\s+([^.!?]+)",
            r"action\s+(?:item|needed):\s*([^.!?\n]+)",
            r"todo:\s*([^.!?\n]+)",
            r"deadline:\s*([^.!?\n]+)",
            r"by\s+(?:tomorrow|today|next week|friday|monday|tuesday|wednesday|thursday|saturday|sunday)\s*[,:]?\s*([^.!?\n]+)"
        ]
        
        action_items = []
        for pattern in action_patterns:
            matches = re.finditer(pattern, email_content, re.IGNORECASE)
            for match in matches:
                action_items.append({
                    "text": match.group(1).strip(),
                    "type": "action_item",
                    "confidence": 0.8,
                    "extracted_from": match.group(0)
                })
        
        # Extract dates and deadlines
        date_patterns = [
            r"(?:due|deadline|by)\s+((?:january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{1,2}(?:st|nd|rd|th)?(?:,?\s+\d{4})?)",
            r"(?:due|deadline|by)\s+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})",
            r"(?:due|deadline|by)\s+(tomorrow|today|next week|this week)"
        ]
        
        for pattern in date_patterns:
            matches = re.finditer(pattern, email_content, re.IGNORECASE)
            for match in matches:
                action_items.append({
                    "text": match.group(0),
                    "type": "deadline",
                    "date": match.group(1),
                    "confidence": 0.9
                })
        
        return AgentResult(
            success=True,
            data={
                "action_items": action_items,
                "count": len(action_items)
            },
            confidence=0.8 if action_items else 0.3,
            processing_time=0.0
        )