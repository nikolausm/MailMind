"""
Notification Agent
Handles real-time user notifications and alerts for email events
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import asyncio
import json

from .base_agent import BaseAgent, AgentTask, AgentResult, TaskPriority

class NotificationType(Enum):
    EMAIL_RECEIVED = "email_received"
    HIGH_PRIORITY = "high_priority"
    VIP_SENDER = "vip_sender"
    DEADLINE_REMINDER = "deadline_reminder"
    WORKFLOW_COMPLETE = "workflow_complete"
    RULE_TRIGGERED = "rule_triggered"
    SPAM_DETECTED = "spam_detected"
    SYSTEM_ALERT = "system_alert"
    CUSTOM = "custom"

class NotificationChannel(Enum):
    DESKTOP = "desktop"
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"
    SLACK = "slack"
    TEAMS = "teams"
    WEBHOOK = "webhook"
    IN_APP = "in_app"

class NotificationPriority(Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"

@dataclass
class NotificationRule:
    """Rule for when to send notifications"""
    rule_id: str
    name: str
    notification_type: NotificationType
    conditions: Dict[str, Any]
    channels: List[NotificationChannel]
    priority: NotificationPriority
    enabled: bool = True
    quiet_hours: Optional[Dict[str, str]] = None  # {"start": "22:00", "end": "08:00"}
    rate_limit: Optional[Dict[str, Any]] = None  # {"max_per_hour": 10}
    created_at: datetime = field(default_factory=datetime.utcnow)

@dataclass
class Notification:
    """Individual notification"""
    notification_id: str
    notification_type: NotificationType
    title: str
    message: str
    priority: NotificationPriority
    channels: List[NotificationChannel]
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    scheduled_at: Optional[datetime] = None
    sent_at: Optional[datetime] = None
    delivered_channels: List[NotificationChannel] = field(default_factory=list)
    failed_channels: List[NotificationChannel] = field(default_factory=list)
    user_id: Optional[str] = None

class NotificationAgent(BaseAgent):
    """
    Handles real-time notifications and user alerts
    
    Features:
    - Multi-channel notifications (desktop, email, SMS, push, etc.)
    - Intelligent notification rules and filtering
    - Rate limiting and quiet hours
    - Notification prioritization and grouping
    - Delivery status tracking
    - Integration with Blazor SignalR for real-time updates
    - Customizable notification templates
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__("notification_agent", config)
        self.notification_rules: Dict[str, NotificationRule] = {}
        self.pending_notifications: List[Notification] = []
        self.sent_notifications: List[Notification] = []
        self.channel_handlers = self._initialize_channel_handlers()
        self.rate_limiters: Dict[str, Dict[str, int]] = {}  # channel -> hour -> count
        self._initialize_default_rules()
        
        # Start background task for processing notifications
        asyncio.create_task(self._notification_processor())
    
    def _initialize_channel_handlers(self) -> Dict[NotificationChannel, callable]:
        """Initialize notification channel handlers"""
        return {
            NotificationChannel.DESKTOP: self._send_desktop_notification,
            NotificationChannel.EMAIL: self._send_email_notification,
            NotificationChannel.SMS: self._send_sms_notification,
            NotificationChannel.PUSH: self._send_push_notification,
            NotificationChannel.SLACK: self._send_slack_notification,
            NotificationChannel.TEAMS: self._send_teams_notification,
            NotificationChannel.WEBHOOK: self._send_webhook_notification,
            NotificationChannel.IN_APP: self._send_in_app_notification
        }
    
    def _initialize_default_rules(self):
        """Initialize default notification rules"""
        
        # High priority email notifications
        high_priority_rule = NotificationRule(
            rule_id="high_priority_email",
            name="High Priority Email Alert",
            notification_type=NotificationType.HIGH_PRIORITY,
            conditions={
                "priority": ["high", "urgent"],
                "sender_type": ["vip", "boss", "client"]
            },
            channels=[NotificationChannel.DESKTOP, NotificationChannel.IN_APP],
            priority=NotificationPriority.HIGH,
            rate_limit={"max_per_hour": 20}
        )
        
        # VIP sender notifications
        vip_sender_rule = NotificationRule(
            rule_id="vip_sender",
            name="VIP Sender Alert",
            notification_type=NotificationType.VIP_SENDER,
            conditions={
                "sender_vip": True
            },
            channels=[NotificationChannel.DESKTOP, NotificationChannel.PUSH],
            priority=NotificationPriority.HIGH,
            quiet_hours={"start": "22:00", "end": "08:00"},
            rate_limit={"max_per_hour": 15}
        )
        
        # Deadline reminders
        deadline_rule = NotificationRule(
            rule_id="deadline_reminder",
            name="Deadline Reminder",
            notification_type=NotificationType.DEADLINE_REMINDER,
            conditions={
                "has_deadline": True,
                "hours_until_deadline": {"less_than": 24}
            },
            channels=[NotificationChannel.DESKTOP, NotificationChannel.EMAIL],
            priority=NotificationPriority.NORMAL,
            rate_limit={"max_per_hour": 5}
        )
        
        # Workflow completion
        workflow_complete_rule = NotificationRule(
            rule_id="workflow_complete",
            name="Workflow Completion Alert",
            notification_type=NotificationType.WORKFLOW_COMPLETE,
            conditions={
                "workflow_status": "completed",
                "workflow_duration": {"greater_than": 300}  # Only for workflows > 5 min
            },
            channels=[NotificationChannel.IN_APP],
            priority=NotificationPriority.NORMAL
        )
        
        # System alerts
        system_alert_rule = NotificationRule(
            rule_id="system_alert",
            name="System Alert",
            notification_type=NotificationType.SYSTEM_ALERT,
            conditions={
                "alert_level": ["warning", "error", "critical"]
            },
            channels=[NotificationChannel.DESKTOP, NotificationChannel.EMAIL, NotificationChannel.SLACK],
            priority=NotificationPriority.URGENT
        )
        
        self.notification_rules = {
            rule.rule_id: rule for rule in [
                high_priority_rule, vip_sender_rule, deadline_rule, 
                workflow_complete_rule, system_alert_rule
            ]
        }
    
    async def process_task(self, task: AgentTask) -> AgentResult:
        """Process notification tasks"""
        try:
            if task.task_type == "send_notification":
                return await self._send_notification(task.payload)
            elif task.task_type == "create_notification_rule":
                return await self._create_notification_rule(task.payload)
            elif task.task_type == "update_notification_rule":
                return await self._update_notification_rule(task.payload)
            elif task.task_type == "check_notification_rules":
                return await self._check_notification_rules(task.payload)
            elif task.task_type == "get_notification_status":
                return await self._get_notification_status(task.payload)
            elif task.task_type == "schedule_notification":
                return await self._schedule_notification(task.payload)
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
            "send_notification",
            "create_notification_rule",
            "update_notification_rule",
            "check_notification_rules",
            "get_notification_status",
            "schedule_notification"
        ]
    
    async def _send_notification(self, payload: Dict[str, Any]) -> AgentResult:
        """Send a notification immediately"""
        try:
            notification = self._create_notification_from_payload(payload)
            
            # Add to processing queue
            self.pending_notifications.append(notification)
            
            return AgentResult(
                success=True,
                data={
                    "notification_id": notification.notification_id,
                    "message": "Notification queued for sending"
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
    
    def _create_notification_from_payload(self, payload: Dict[str, Any]) -> Notification:
        """Create notification object from payload"""
        return Notification(
            notification_id=payload.get("notification_id", f"notif_{datetime.utcnow().timestamp()}"),
            notification_type=NotificationType(payload.get("type", NotificationType.CUSTOM.value)),
            title=payload["title"],
            message=payload["message"],
            priority=NotificationPriority(payload.get("priority", NotificationPriority.NORMAL.value)),
            channels=[NotificationChannel(ch) for ch in payload.get("channels", ["in_app"])],
            metadata=payload.get("metadata", {}),
            user_id=payload.get("user_id"),
            scheduled_at=payload.get("scheduled_at")
        )
    
    async def _check_notification_rules(self, payload: Dict[str, Any]) -> AgentResult:
        """Check if event triggers any notification rules"""
        event_data = payload.get("event_data", {})
        triggered_rules = []
        
        for rule in self.notification_rules.values():
            if not rule.enabled:
                continue
                
            if self._evaluate_rule_conditions(rule, event_data):
                # Check rate limits
                if self._check_rate_limit(rule):
                    # Check quiet hours
                    if not self._is_quiet_hours(rule):
                        triggered_rules.append(rule)
                        
                        # Create and queue notification
                        notification = self._create_notification_from_rule(rule, event_data)
                        self.pending_notifications.append(notification)
        
        return AgentResult(
            success=True,
            data={
                "triggered_rules": len(triggered_rules),
                "rule_ids": [rule.rule_id for rule in triggered_rules],
                "notifications_queued": len(triggered_rules)
            },
            confidence=1.0,
            processing_time=0.0
        )
    
    def _evaluate_rule_conditions(self, rule: NotificationRule, event_data: Dict[str, Any]) -> bool:
        """Evaluate if rule conditions are met"""
        for condition_key, condition_value in rule.conditions.items():
            event_value = event_data.get(condition_key)
            
            if isinstance(condition_value, list):
                if event_value not in condition_value:
                    return False
            elif isinstance(condition_value, dict):
                # Handle complex conditions like {"greater_than": 100}
                if "greater_than" in condition_value:
                    if not (event_value and float(event_value) > condition_value["greater_than"]):
                        return False
                elif "less_than" in condition_value:
                    if not (event_value and float(event_value) < condition_value["less_than"]):
                        return False
                elif "equals" in condition_value:
                    if event_value != condition_value["equals"]:
                        return False
            else:
                if event_value != condition_value:
                    return False
        
        return True
    
    def _check_rate_limit(self, rule: NotificationRule) -> bool:
        """Check if notification is within rate limits"""
        if not rule.rate_limit:
            return True
        
        max_per_hour = rule.rate_limit.get("max_per_hour")
        if not max_per_hour:
            return True
        
        current_hour = datetime.utcnow().strftime("%Y-%m-%d-%H")
        
        if rule.rule_id not in self.rate_limiters:
            self.rate_limiters[rule.rule_id] = {}
        
        current_count = self.rate_limiters[rule.rule_id].get(current_hour, 0)
        
        if current_count >= max_per_hour:
            return False
        
        # Increment counter
        self.rate_limiters[rule.rule_id][current_hour] = current_count + 1
        
        # Clean up old entries
        self._cleanup_rate_limiters()
        
        return True
    
    def _cleanup_rate_limiters(self):
        """Clean up old rate limiter entries"""
        current_hour = datetime.utcnow().strftime("%Y-%m-%d-%H")
        
        for rule_id in self.rate_limiters:
            hours_to_remove = []
            for hour in self.rate_limiters[rule_id]:
                if hour < current_hour:
                    hours_to_remove.append(hour)
            
            for hour in hours_to_remove:
                del self.rate_limiters[rule_id][hour]
    
    def _is_quiet_hours(self, rule: NotificationRule) -> bool:
        """Check if current time is within quiet hours"""
        if not rule.quiet_hours:
            return False
        
        current_time = datetime.utcnow().time()
        start_time = datetime.strptime(rule.quiet_hours["start"], "%H:%M").time()
        end_time = datetime.strptime(rule.quiet_hours["end"], "%H:%M").time()
        
        if start_time <= end_time:
            # Same day quiet hours
            return start_time <= current_time <= end_time
        else:
            # Overnight quiet hours
            return current_time >= start_time or current_time <= end_time
    
    def _create_notification_from_rule(self, rule: NotificationRule, event_data: Dict[str, Any]) -> Notification:
        """Create notification from rule and event data"""
        # Generate notification content based on type
        title, message = self._generate_notification_content(rule.notification_type, event_data)
        
        return Notification(
            notification_id=f"rule_{rule.rule_id}_{datetime.utcnow().timestamp()}",
            notification_type=rule.notification_type,
            title=title,
            message=message,
            priority=rule.priority,
            channels=rule.channels,
            metadata={
                "rule_id": rule.rule_id,
                "event_data": event_data
            },
            user_id=event_data.get("user_id")
        )
    
    def _generate_notification_content(self, notification_type: NotificationType, event_data: Dict[str, Any]) -> tuple:
        """Generate notification title and message based on type"""
        templates = {
            NotificationType.EMAIL_RECEIVED: {
                "title": "New Email",
                "message": "You have received a new email from {sender}"
            },
            NotificationType.HIGH_PRIORITY: {
                "title": "High Priority Email",
                "message": "High priority email from {sender}: {subject}"
            },
            NotificationType.VIP_SENDER: {
                "title": "VIP Email",
                "message": "Email from VIP contact {sender}"
            },
            NotificationType.DEADLINE_REMINDER: {
                "title": "Deadline Reminder",
                "message": "Deadline approaching: {deadline_description}"
            },
            NotificationType.WORKFLOW_COMPLETE: {
                "title": "Workflow Complete",
                "message": "Workflow '{workflow_name}' has completed successfully"
            },
            NotificationType.RULE_TRIGGERED: {
                "title": "Rule Triggered",
                "message": "Automation rule '{rule_name}' was triggered"
            },
            NotificationType.SPAM_DETECTED: {
                "title": "Spam Detected",
                "message": "Spam email detected and moved to spam folder"
            },
            NotificationType.SYSTEM_ALERT: {
                "title": "System Alert",
                "message": "System alert: {alert_message}"
            }
        }
        
        template = templates.get(notification_type, {
            "title": "Notification",
            "message": "You have a new notification"
        })
        
        # Format with event data
        try:
            title = template["title"].format(**event_data)
            message = template["message"].format(**event_data)
        except KeyError:
            # Use defaults if formatting fails
            title = template["title"]
            message = template["message"]
        
        return title, message
    
    async def _notification_processor(self):
        """Background task to process pending notifications"""
        while True:
            try:
                if self.pending_notifications:
                    # Process notifications in priority order
                    self.pending_notifications.sort(key=lambda n: self._get_priority_weight(n.priority), reverse=True)
                    
                    # Process batch of notifications
                    batch_size = min(10, len(self.pending_notifications))
                    batch = self.pending_notifications[:batch_size]
                    self.pending_notifications = self.pending_notifications[batch_size:]
                    
                    # Send notifications in parallel
                    tasks = [self._deliver_notification(notification) for notification in batch]
                    await asyncio.gather(*tasks, return_exceptions=True)
                
                # Wait before next batch
                await asyncio.sleep(1)
                
            except Exception as e:
                self.logger.error(f"Error in notification processor: {e}")
                await asyncio.sleep(5)  # Wait longer on error
    
    def _get_priority_weight(self, priority: NotificationPriority) -> int:
        """Get numeric weight for priority sorting"""
        weights = {
            NotificationPriority.LOW: 1,
            NotificationPriority.NORMAL: 2,
            NotificationPriority.HIGH: 3,
            NotificationPriority.URGENT: 4
        }
        return weights.get(priority, 2)
    
    async def _deliver_notification(self, notification: Notification):
        """Deliver notification through all specified channels"""
        for channel in notification.channels:
            try:
                handler = self.channel_handlers.get(channel)
                if handler:
                    await handler(notification)
                    notification.delivered_channels.append(channel)
                else:
                    self.logger.warning(f"No handler for channel: {channel}")
                    notification.failed_channels.append(channel)
                    
            except Exception as e:
                self.logger.error(f"Failed to send notification via {channel}: {e}")
                notification.failed_channels.append(channel)
        
        notification.sent_at = datetime.utcnow()
        self.sent_notifications.append(notification)
        
        # Keep only recent notifications in memory
        if len(self.sent_notifications) > 1000:
            self.sent_notifications = self.sent_notifications[-500:]
    
    # Channel handlers
    async def _send_desktop_notification(self, notification: Notification):
        """Send desktop notification"""
        self.logger.info(f"Desktop notification: {notification.title} - {notification.message}")
        # Implementation would use desktop notification API
    
    async def _send_email_notification(self, notification: Notification):
        """Send email notification"""
        self.logger.info(f"Email notification to {notification.user_id}: {notification.title}")
        # Implementation would use email service
    
    async def _send_sms_notification(self, notification: Notification):
        """Send SMS notification"""
        self.logger.info(f"SMS notification: {notification.message}")
        # Implementation would use SMS service (Twilio, etc.)
    
    async def _send_push_notification(self, notification: Notification):
        """Send push notification"""
        self.logger.info(f"Push notification: {notification.title}")
        # Implementation would use push notification service
    
    async def _send_slack_notification(self, notification: Notification):
        """Send Slack notification"""
        self.logger.info(f"Slack notification: {notification.message}")
        # Implementation would use Slack API
    
    async def _send_teams_notification(self, notification: Notification):
        """Send Microsoft Teams notification"""
        self.logger.info(f"Teams notification: {notification.message}")
        # Implementation would use Teams API
    
    async def _send_webhook_notification(self, notification: Notification):
        """Send webhook notification"""
        webhook_url = notification.metadata.get("webhook_url")
        if webhook_url:
            self.logger.info(f"Webhook notification to {webhook_url}")
            # Implementation would send HTTP POST to webhook
    
    async def _send_in_app_notification(self, notification: Notification):
        """Send in-app notification via SignalR"""
        self.logger.info(f"In-app notification: {notification.title}")
        # Implementation would use SignalR to send real-time notification to Blazor frontend
        
        # Example SignalR integration
        signalr_data = {
            "type": "notification",
            "notification": {
                "id": notification.notification_id,
                "title": notification.title,
                "message": notification.message,
                "priority": notification.priority.value,
                "timestamp": notification.created_at.isoformat(),
                "metadata": notification.metadata
            }
        }
        
        # This would be sent via SignalR hub to connected Blazor clients
        self.logger.info(f"SignalR data: {json.dumps(signalr_data)}")
    
    async def _create_notification_rule(self, payload: Dict[str, Any]) -> AgentResult:
        """Create a new notification rule"""
        try:
            rule_data = payload.get("rule_data", {})
            
            rule = NotificationRule(
                rule_id=rule_data.get("rule_id", f"rule_{len(self.notification_rules) + 1}"),
                name=rule_data["name"],
                notification_type=NotificationType(rule_data["notification_type"]),
                conditions=rule_data.get("conditions", {}),
                channels=[NotificationChannel(ch) for ch in rule_data.get("channels", ["in_app"])],
                priority=NotificationPriority(rule_data.get("priority", "normal")),
                enabled=rule_data.get("enabled", True),
                quiet_hours=rule_data.get("quiet_hours"),
                rate_limit=rule_data.get("rate_limit")
            )
            
            self.notification_rules[rule.rule_id] = rule
            
            return AgentResult(
                success=True,
                data={"rule_id": rule.rule_id, "message": "Notification rule created"},
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
    
    async def _update_notification_rule(self, payload: Dict[str, Any]) -> AgentResult:
        """Update an existing notification rule"""
        rule_id = payload.get("rule_id")
        updates = payload.get("updates", {})
        
        if rule_id not in self.notification_rules:
            return AgentResult(
                success=False,
                data={},
                confidence=0.0,
                processing_time=0.0,
                error_message=f"Rule {rule_id} not found"
            )
        
        rule = self.notification_rules[rule_id]
        
        # Apply updates
        for key, value in updates.items():
            if hasattr(rule, key):
                if key == "channels":
                    setattr(rule, key, [NotificationChannel(ch) for ch in value])
                elif key == "notification_type":
                    setattr(rule, key, NotificationType(value))
                elif key == "priority":
                    setattr(rule, key, NotificationPriority(value))
                else:
                    setattr(rule, key, value)
        
        return AgentResult(
            success=True,
            data={"rule_id": rule_id, "message": "Rule updated successfully"},
            confidence=1.0,
            processing_time=0.0
        )
    
    async def _get_notification_status(self, payload: Dict[str, Any]) -> AgentResult:
        """Get notification status and statistics"""
        notification_id = payload.get("notification_id")
        
        if notification_id:
            # Get specific notification status
            notification = next(
                (n for n in self.sent_notifications if n.notification_id == notification_id),
                None
            )
            
            if notification:
                return AgentResult(
                    success=True,
                    data={
                        "notification": {
                            "id": notification.notification_id,
                            "title": notification.title,
                            "status": "sent" if notification.sent_at else "pending",
                            "delivered_channels": [ch.value for ch in notification.delivered_channels],
                            "failed_channels": [ch.value for ch in notification.failed_channels],
                            "sent_at": notification.sent_at.isoformat() if notification.sent_at else None
                        }
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
                    error_message=f"Notification {notification_id} not found"
                )
        else:
            # Get general statistics
            return AgentResult(
                success=True,
                data={
                    "statistics": {
                        "total_sent": len(self.sent_notifications),
                        "pending": len(self.pending_notifications),
                        "active_rules": len([r for r in self.notification_rules.values() if r.enabled]),
                        "total_rules": len(self.notification_rules)
                    }
                },
                confidence=1.0,
                processing_time=0.0
            )
    
    async def _schedule_notification(self, payload: Dict[str, Any]) -> AgentResult:
        """Schedule a notification for future delivery"""
        try:
            notification = self._create_notification_from_payload(payload)
            scheduled_time = payload.get("scheduled_at")
            
            if scheduled_time:
                if isinstance(scheduled_time, str):
                    notification.scheduled_at = datetime.fromisoformat(scheduled_time)
                else:
                    notification.scheduled_at = scheduled_time
            else:
                # Default to 1 minute from now
                notification.scheduled_at = datetime.utcnow() + timedelta(minutes=1)
            
            # Add to pending notifications (processor will handle scheduling)
            self.pending_notifications.append(notification)
            
            return AgentResult(
                success=True,
                data={
                    "notification_id": notification.notification_id,
                    "scheduled_at": notification.scheduled_at.isoformat(),
                    "message": "Notification scheduled"
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