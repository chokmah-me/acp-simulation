"""
Enumerations for ACP simulation.
"""

from enum import Enum


class NodeState(Enum):
    """
    Network node states.

    Attributes
    ----------
    CLEAN : int
        Node is clean and uncompromised
    COMPROMISED : int
        Node has been compromised by attacker
    HONEYPOT : int
        Node is a honeypot (deception target)
    PATCHED : int
        Node has been patched (reduced vulnerability)
    ISOLATED : int
        Node has been isolated from network
    """

    CLEAN = 0
    COMPROMISED = 1
    HONEYPOT = 2
    PATCHED = 3
    ISOLATED = 4


class ActionType(Enum):
    """
    Available actions for both agents.

    Attributes
    ----------
    SCAN : int
        Attacker action: scan network for vulnerabilities
    EXPLOIT : int
        Attacker action: exploit known vulnerability
    PROPAGATE : int
        Attacker action: propagate to adjacent nodes
    MONITOR : int
        Defender action: passive monitoring
    PATCH : int
        Defender action: patch vulnerable node
    ISOLATE : int
        Defender action: isolate compromised node
    DEPLOY_HONEYPOT : int
        Defender action: deploy honeypot deception
    ACP_DECEPTION : int
        Defender action: deploy ACP deception
    RESTORE_NODE : int
        Defender action: restore node (expensive)
    """

    # Attacker actions
    SCAN = 0
    EXPLOIT = 1
    PROPAGATE = 2

    # Defender actions
    MONITOR = 3
    PATCH = 4
    ISOLATE = 5
    DEPLOY_HONEYPOT = 6
    ACP_DECEPTION = 7
    RESTORE_NODE = 8
