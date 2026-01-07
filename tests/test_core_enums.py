"""
Tests for core enumerations.
"""

import pytest

from acp_simulation.core.enums import ActionType, NodeState


class TestNodeState:
    """Test NodeState enumeration."""

    def test_node_state_values(self):
        """Test that NodeState has correct values."""
        assert NodeState.CLEAN.value == 0
        assert NodeState.COMPROMISED.value == 1
        assert NodeState.HONEYPOT.value == 2
        assert NodeState.PATCHED.value == 3
        assert NodeState.ISOLATED.value == 4

    def test_node_state_members(self):
        """Test that all expected NodeState members exist."""
        members = list(NodeState)
        assert len(members) == 5
        assert NodeState.CLEAN in members
        assert NodeState.COMPROMISED in members
        assert NodeState.HONEYPOT in members
        assert NodeState.PATCHED in members
        assert NodeState.ISOLATED in members

    def test_node_state_comparison(self):
        """Test NodeState comparison operations."""
        assert NodeState.CLEAN != NodeState.COMPROMISED
        assert NodeState.CLEAN == NodeState.CLEAN

    def test_node_state_iteration(self):
        """Test iterating over NodeState members."""
        states = [state for state in NodeState]
        assert len(states) == 5
        assert all(isinstance(state, NodeState) for state in states)


class TestActionType:
    """Test ActionType enumeration."""

    def test_action_type_values(self):
        """Test that ActionType has correct values."""
        # Attacker actions
        assert ActionType.SCAN.value == 0
        assert ActionType.EXPLOIT.value == 1
        assert ActionType.PROPAGATE.value == 2

        # Defender actions
        assert ActionType.MONITOR.value == 3
        assert ActionType.PATCH.value == 4
        assert ActionType.ISOLATE.value == 5
        assert ActionType.DEPLOY_HONEYPOT.value == 6
        assert ActionType.ACP_DECEPTION.value == 7
        assert ActionType.RESTORE_NODE.value == 8

    def test_action_type_members(self):
        """Test that all expected ActionType members exist."""
        members = list(ActionType)
        assert len(members) == 9

        # Attacker actions
        assert ActionType.SCAN in members
        assert ActionType.EXPLOIT in members
        assert ActionType.PROPAGATE in members

        # Defender actions
        assert ActionType.MONITOR in members
        assert ActionType.PATCH in members
        assert ActionType.ISOLATE in members
        assert ActionType.DEPLOY_HONEYPOT in members
        assert ActionType.ACP_DECEPTION in members
        assert ActionType.RESTORE_NODE in members

    def test_action_type_comparison(self):
        """Test ActionType comparison operations."""
        assert ActionType.SCAN != ActionType.EXPLOIT
        assert ActionType.SCAN == ActionType.SCAN
        assert ActionType.ACP_DECEPTION != ActionType.RESTORE_NODE

    def test_action_type_names(self):
        """Test ActionType names are correct."""
        assert ActionType.SCAN.name == "SCAN"
        assert ActionType.EXPLOIT.name == "EXPLOIT"
        assert ActionType.ACP_DECEPTION.name == "ACP_DECEPTION"
        assert ActionType.RESTORE_NODE.name == "RESTORE_NODE"

    def test_action_type_iteration(self):
        """Test iterating over ActionType members."""
        actions = [action for action in ActionType]
        assert len(actions) == 9
        assert all(isinstance(action, ActionType) for action in actions)
