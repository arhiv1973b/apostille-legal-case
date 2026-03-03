import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tri_instance_ai_coordinator import (
    Task,
    TaskResult,
    AIInstance,
    InstanceStatus,
    TriInstanceAICoordinator,
)


class TestTask:
    def test_task_creation(self):
        task = Task(
            id="test_1",
            description="Test task",
            priority=5
        )
        assert task.id == "test_1"
        assert task.description == "Test task"
        assert task.priority == 5
        assert task.retries == 0
        assert task.max_retries == 3
        assert task.created_at is not None

    def test_task_default_values(self):
        task = Task(id="test_2", description="Test", priority=1)
        assert task.environment is None
        assert task.created_at is not None


class TestTaskResult:
    def test_task_result_creation(self):
        result = TaskResult(
            task_id="task_1",
            success=True,
            result="Completed",
            execution_time=1.5,
            environment="windows"
        )
        assert result.task_id == "task_1"
        assert result.success is True
        assert result.result == "Completed"
        assert result.error is None
        assert result.execution_time == 1.5

    def test_task_result_failure(self):
        result = TaskResult(
            task_id="task_2",
            success=False,
            error="Timeout error"
        )
        assert result.success is False
        assert result.error == "Timeout error"
        assert result.result is None


class TestAIInstance:
    def test_instance_creation(self):
        instance = AIInstance("windows", 0)
        assert instance.environment == "windows"
        assert instance.instance_id == 0
        assert instance.status == InstanceStatus.ACTIVE
        assert instance.processed_tasks == 0
        assert instance.failed_tasks == 0
        assert instance.temperature == 0.5
        assert instance.clarity == 0.8

    def test_instance_execute_task(self):
        instance = AIInstance("windows", 0)
        task = Task(id="test_task", description="Test", priority=1)
        
        instance.temperature = 0.5
        instance.clarity = 0.8
        
        result = instance.execute_task(task)
        
        assert result.task_id == "test_task"
        assert result.environment == "windows"
        assert isinstance(result.execution_time, float)

    def test_instance_status(self):
        instance = AIInstance("wsl", 1)
        assert instance.status == InstanceStatus.ACTIVE
        
        instance.status = InstanceStatus.TUNNELING
        assert instance.status == InstanceStatus.TUNNELING


class TestTriInstanceAICoordinator:
    def test_coordinator_creation(self):
        coordinator = TriInstanceAICoordinator()
        
        assert len(coordinator.instances) == 3
        assert coordinator.instances[0].environment == "windows"
        assert coordinator.instances[1].environment == "wsl"
        assert coordinator.instances[2].environment == "git"
        assert coordinator.running is False

    def test_add_task(self):
        coordinator = TriInstanceAICoordinator()
        
        task_id = coordinator.add_task("Test task", priority=3)
        
        assert task_id is not None
        assert task_id.startswith("task_")

    def test_coordinator_environments(self):
        coordinator = TriInstanceAICoordinator()
        
        envs = [inst.environment for inst in coordinator.instances]
        assert "windows" in envs
        assert "wsl" in envs
        assert "git" in envs
