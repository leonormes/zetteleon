#!/usr/bin/env python3
"""
ProdOS Natural Language Parser

Parses natural language input and maps to structured ProdOS commands.
Core functionality for the ProdOS natural language interface.
"""

import re
import json
from typing import Dict, List, Optional, Tuple, NamedTuple
from dataclasses import dataclass
from enum import Enum


class CommandType(Enum):
    DAILY_PLAN = "daily_plan"
    WHAT_NEXT = "what_next"
    CAPTURE = "capture"
    URGENT_TASKS = "urgent_tasks"
    SYNC_STATUS = "sync_status"
    CURRENT_PROJECTS = "current_projects"
    LOW_ENERGY_TASKS = "low_energy_tasks"
    TODAY_PROGRESS = "today_progress"
    HELP = "help"
    UNKNOWN = "unknown"


@dataclass
class CommandResult:
    """Structured result of natural language parsing"""
    command_type: CommandType
    confidence: float
    parameters: Dict[str, str]
    raw_input: str
    suggestions: List[str] = None
    
    def is_confident(self, threshold: float = 0.7) -> bool:
        """Check if confidence meets threshold for execution"""
        return self.confidence >= threshold


class NaturalLanguageParser:
    """
    Parses natural language input and maps to ProdOS commands.
    
    Uses regex patterns with confidence scoring to handle variations
    in user input while providing fallbacks for unclear commands.
    """
    
    def __init__(self):
        self.patterns = self._initialize_patterns()
        self.command_suggestions = {
            CommandType.DAILY_PLAN: ["daily", "morning plan", "start day", "daily planning"],
            CommandType.WHAT_NEXT: ["next", "what next", "what's next", "next task"],
            CommandType.CAPTURE: ["capture", "add task", "quick add", "note"],
            CommandType.URGENT_TASKS: ["urgent", "high priority", "important", "critical"],
            CommandType.SYNC_STATUS: ["status", "sync", "health", "check systems"],
            CommandType.CURRENT_PROJECTS: ["projects", "active projects", "current work"],
            CommandType.LOW_ENERGY_TASKS: ["lowkey", "low energy", "easy tasks", "light work"],
            CommandType.TODAY_PROGRESS: ["progress", "completed", "done today", "accomplishments"]
        }
    
    def _initialize_patterns(self) -> Dict[CommandType, List[Tuple[str, float]]]:
        """Initialize regex patterns with base confidence scores"""
        return {
            CommandType.DAILY_PLAN: [
                (r'^\s*daily\s*plan\s*$', 1.0),
                (r'^\s*daily\s*$', 0.95),
                (r'^\s*(morning|start)?\s*(plan|planning)\s*$', 0.85),
                (r'^\s*start\s*(the\s*)?day\s*$', 0.80),
                (r'.*daily.*plan.*', 0.75),
                (r'.*d[a-z]*l[a-z]*y.*plan.*', 0.70),  # Fuzzy match for typos like "daliy"
            ],
            
            CommandType.WHAT_NEXT: [
                (r'^\s*what\'?s\s*next\s*\??\s*$', 1.0),
                (r'^\s*next\s*$', 0.95),
                (r'^\s*what\s*next\s*$', 0.95),
                (r'^\s*(next|what)\s*(task|item)\s*$', 0.90),
                (r'.*what.*next.*', 0.75),
                (r'.*w[a-z]*t[a-z]*s.*next.*', 0.70),  # Fuzzy match for typos like "whats"
            ],
            
            CommandType.CAPTURE: [
                (r'^\s*capture\s+(.+)', 0.95),  # Capture with content
                (r'^\s*add\s+(task|item)?\s*(.+)', 0.90),
                (r'^\s*(quick\s*)?(add|note)\s+(.+)', 0.85),
                (r'^\s*capture\s*$', 0.80),  # Capture without content
                (r'.*capture.*', 0.70),
            ],
            
            CommandType.URGENT_TASKS: [
                (r'^\s*urgent\s*(tasks?)?\s*$', 0.95),
                (r'^\s*(high\s*)?priority\s*(tasks?)?\s*$', 0.90),
                (r'^\s*(important|critical)\s*(tasks?)?\s*$', 0.85),
                (r'.*urgent.*', 0.75),
            ],
            
            CommandType.SYNC_STATUS: [
                (r'^\s*(sync\s*)?status\s*$', 0.95),
                (r'^\s*sync\s*$', 0.90),
                (r'^\s*health\s*(check)?\s*$', 0.85),
                (r'^\s*check\s*systems?\s*$', 0.80),
                (r'.*status.*', 0.70),
            ],
            
            CommandType.CURRENT_PROJECTS: [
                (r'^\s*(current\s*)?projects\s*$', 0.95),
                (r'^\s*active\s*projects\s*$', 0.90),
                (r'^\s*current\s*work\s*$', 0.85),
                (r'^\s*projects\s*list\s*$', 0.80),
                (r'.*projects.*', 0.70),
            ],
            
            CommandType.LOW_ENERGY_TASKS: [
                (r'^\s*low\s*key\s*(tasks?)?\s*$', 0.95),
                (r'^\s*low\s*energy\s*(tasks?)?\s*$', 0.95),
                (r'^\s*easy\s*(tasks?)?\s*$', 0.85),
                (r'^\s*light\s*work\s*$', 0.80),
                (r'.*low.*energy.*', 0.75),
            ],
            
            CommandType.TODAY_PROGRESS: [
                (r'^\s*progress\s*$', 0.95),
                (r'^\s*(today\'?s\s*)?progress\s*$', 0.90),
                (r'^\s*(completed|done)\s*(today)?\s*$', 0.85),
                (r'^\s*accomplishments\s*$', 0.80),
                (r'.*progress.*', 0.70),
            ],
            
            CommandType.HELP: [
                (r'^\s*help\s*$', 0.95),
                (r'^\s*\?\s*$', 0.90),
                (r'^\s*(help\s+)?commands?\s*$', 0.85),
                (r'^\s*what\s*can\s*you\s*do\s*$', 0.80),
            ],
        }
    
    def parse(self, user_input: str) -> CommandResult:
        """
        Parse natural language input and return structured command result.
        
        Args:
            user_input: Raw user input string
            
        Returns:
            CommandResult with command type, confidence, and parameters
        """
        if not user_input or not user_input.strip():
            return CommandResult(
                command_type=CommandType.UNKNOWN,
                confidence=0.0,
                parameters={},
                raw_input=user_input,
                suggestions=["Try: daily, next, capture, urgent, or status"]
            )
        
        normalized_input = self._normalize_input(user_input)
        best_match = None
        best_confidence = 0.0
        extracted_params = {}
        
        # Try matching against all patterns
        for command_type, patterns in self.patterns.items():
            for pattern, base_confidence in patterns:
                match = re.search(pattern, normalized_input, re.IGNORECASE)
                if match:
                    confidence = self._calculate_confidence(
                        base_confidence, normalized_input, pattern, match
                    )
                    
                    if confidence > best_confidence:
                        best_confidence = confidence
                        best_match = command_type
                        extracted_params = self._extract_parameters(
                            command_type, match, user_input  # Use original input for parameters
                        )
        
        if best_match:
            return CommandResult(
                command_type=best_match,
                confidence=best_confidence,
                parameters=extracted_params,
                raw_input=user_input,
                suggestions=None  # No suggestions needed for recognized commands
            )
        else:
            # No match found - provide suggestions
            suggestions = self._generate_suggestions(normalized_input)
            return CommandResult(
                command_type=CommandType.UNKNOWN,
                confidence=0.0,
                parameters={},
                raw_input=user_input,
                suggestions=suggestions
            )
    
    def _normalize_input(self, user_input: str) -> str:
        """Normalize user input for better pattern matching"""
        # Strip whitespace but preserve case for parameter extraction
        normalized = user_input.strip()
        
        # Handle common contractions and abbreviations (case-insensitive)
        replacements = {
            "what's": "what is",
            "What's": "What is",
            "can't": "cannot",
            "won't": "will not",
            "n't": " not",
            "pls": "please",
            "plz": "please",
        }
        
        for old, new in replacements.items():
            normalized = normalized.replace(old, new)
        
        # Remove extra whitespace
        normalized = re.sub(r'\s+', ' ', normalized)
        
        return normalized
    
    def _calculate_confidence(
        self, 
        base_confidence: float, 
        input_text: str, 
        pattern: str, 
        match: re.Match
    ) -> float:
        """Calculate confidence score with adjustments for match quality"""
        confidence = base_confidence
        
        # Exact match bonus
        if match.group(0).strip().lower() == input_text.strip().lower():
            confidence += 0.05
        
        # Length penalty for very long inputs (likely more complex)
        if len(input_text) > 50:
            confidence -= 0.1
        
        # Bonus for capturing parameters successfully
        if match.groups():
            confidence += 0.02
        
        # Ensure confidence stays within bounds
        return min(max(confidence, 0.0), 1.0)
    
    def _extract_parameters(
        self, 
        command_type: CommandType, 
        match: re.Match, 
        input_text: str
    ) -> Dict[str, str]:
        """Extract parameters from matched text"""
        params = {}
        
        if command_type == CommandType.CAPTURE:
            # Extract capture content from groups
            groups = [g for g in match.groups() if g is not None]
            if groups:
                # Take the last non-None group as the content
                content = groups[-1].strip()
                if content:
                    params['content'] = content
            
            # If no content in groups, try to extract from full input
            if 'content' not in params:
                # Look for content after common capture words
                capture_match = re.search(
                    r'(?:capture|add|note)\s+(.+)', 
                    input_text, 
                    re.IGNORECASE
                )
                if capture_match:
                    params['content'] = capture_match.group(1).strip()
        
        # Future: Add parameter extraction for other command types
        # e.g., project filters, energy levels, date ranges
        
        return params
    
    def _generate_suggestions(self, input_text: str) -> List[str]:
        """Generate helpful suggestions for unrecognized input"""
        suggestions = []
        
        # Check for partial matches or typos
        input_words = set(input_text.split())
        
        for command_type, suggestion_list in self.command_suggestions.items():
            for suggestion in suggestion_list:
                suggestion_words = set(suggestion.split())
                # If there's word overlap, suggest this command
                if input_words & suggestion_words:
                    suggestions.append(f"{suggestion} - {self._get_command_description(command_type)}")
                    break  # Only add one suggestion per command type
        
        # If no partial matches, provide general suggestions
        if not suggestions:
            suggestions = [
                "daily - Start your morning planning",
                "next - Get your next recommended task", 
                "capture <message> - Quick task/idea capture",
                "urgent - Show high-priority items",
                "status - Check system sync status"
            ]
        
        return suggestions[:5]  # Limit to 5 suggestions
    
    def _get_command_description(self, command_type: CommandType) -> str:
        """Get user-friendly description for command type"""
        descriptions = {
            CommandType.DAILY_PLAN: "Start your morning planning",
            CommandType.WHAT_NEXT: "Get your next recommended task",
            CommandType.CAPTURE: "Quick task/idea capture",
            CommandType.URGENT_TASKS: "Show high-priority items",
            CommandType.SYNC_STATUS: "Check system sync status",
            CommandType.CURRENT_PROJECTS: "Show all active projects",
            CommandType.LOW_ENERGY_TASKS: "Show low-energy tasks",
            CommandType.TODAY_PROGRESS: "See today's accomplishments",
            CommandType.HELP: "Show available commands"
        }
        return descriptions.get(command_type, "Execute command")


def main():
    """CLI interface for testing the parser"""
    parser = NaturalLanguageParser()
    
    print("ProdOS Natural Language Parser Test")
    print("Type 'quit' to exit\n")
    
    while True:
        try:
            user_input = input(">>> ").strip()
            if user_input.lower() == 'quit':
                break
                
            result = parser.parse(user_input)
            
            print(f"Command: {result.command_type.value}")
            print(f"Confidence: {result.confidence:.2f}")
            print(f"Parameters: {result.parameters}")
            
            if result.suggestions:
                print(f"Suggestions: {result.suggestions}")
                
            if result.is_confident():
                print("✅ Ready for execution")
            else:
                print("❓ Low confidence - need clarification")
                
            print("-" * 50)
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()