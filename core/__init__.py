"""
Agentcore Memory Demo - Core Module
"""

from .memory_manager import MemoryManager
from .knight_persona import KNIGHT_PERSONA, get_system_prompt, get_initial_greeting
from .agent import KnightAgent

__all__ = [
    'MemoryManager',
    'KnightAgent',
    'KNIGHT_PERSONA',
    'get_system_prompt',
    'get_initial_greeting'
]
