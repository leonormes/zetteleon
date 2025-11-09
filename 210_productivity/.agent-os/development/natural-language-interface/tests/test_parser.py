#!/usr/bin/env python3
"""
Unit tests for ProdOS Natural Language Parser

Tests pattern recognition, confidence scoring, parameter extraction,
and error handling for the natural language interface.
"""

import unittest
import sys
import os
from typing import List

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from parser import NaturalLanguageParser, CommandType, CommandResult


class TestNaturalLanguageParser(unittest.TestCase):
    """Test cases for natural language parser functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.parser = NaturalLanguageParser()
    
    def test_daily_plan_recognition(self):
        """Test recognition of daily plan commands"""
        test_cases = [
            ("daily plan", CommandType.DAILY_PLAN, 0.95),
            ("daily", CommandType.DAILY_PLAN, 0.90),
            ("morning plan", CommandType.DAILY_PLAN, 0.85),
            ("start day", CommandType.DAILY_PLAN, 0.80),
            ("Daily Plan", CommandType.DAILY_PLAN, 0.95),  # Case insensitive
            ("  daily plan  ", CommandType.DAILY_PLAN, 0.95),  # Whitespace handling
        ]
        
        for input_text, expected_command, min_confidence in test_cases:
            with self.subTest(input_text=input_text):
                result = self.parser.parse(input_text)
                self.assertEqual(result.command_type, expected_command)
                self.assertGreaterEqual(result.confidence, min_confidence - 0.1)
                self.assertTrue(result.is_confident())
    
    def test_what_next_recognition(self):
        """Test recognition of what's next commands"""
        test_cases = [
            ("what's next?", CommandType.WHAT_NEXT, 0.98),
            ("next", CommandType.WHAT_NEXT, 0.95),
            ("what next", CommandType.WHAT_NEXT, 0.95),
            ("next task", CommandType.WHAT_NEXT, 0.85),
            ("whats next", CommandType.WHAT_NEXT, 0.85),  # Typo handling
        ]
        
        for input_text, expected_command, min_confidence in test_cases:
            with self.subTest(input_text=input_text):
                result = self.parser.parse(input_text)
                self.assertEqual(result.command_type, expected_command)
                self.assertGreaterEqual(result.confidence, min_confidence - 0.1)
    
    def test_capture_with_content(self):
        """Test capture commands with content extraction"""
        test_cases = [
            ("capture meeting notes", "meeting notes"),
            ("capture FFAPP-4565 API testing", "FFAPP-4565 API testing"),
            ("add task review documentation", "review documentation"),
            ("quick add finish report", "finish report"),
            ("note call John about project", "call John about project"),
        ]
        
        for input_text, expected_content in test_cases:
            with self.subTest(input_text=input_text):
                result = self.parser.parse(input_text)
                self.assertEqual(result.command_type, CommandType.CAPTURE)
                self.assertTrue(result.is_confident())
                self.assertIn('content', result.parameters)
                self.assertEqual(result.parameters['content'], expected_content)
    
    def test_capture_without_content(self):
        """Test capture command without content"""
        result = self.parser.parse("capture")
        self.assertEqual(result.command_type, CommandType.CAPTURE)
        self.assertTrue(result.is_confident())
        # Should not have content parameter or it should be empty
        if 'content' in result.parameters:
            self.assertEqual(result.parameters['content'], '')
    
    def test_urgent_tasks_recognition(self):
        """Test recognition of urgent task commands"""
        test_cases = [
            ("urgent", CommandType.URGENT_TASKS, 0.95),
            ("urgent tasks", CommandType.URGENT_TASKS, 0.95),
            ("priority", CommandType.URGENT_TASKS, 0.90),
            ("high priority", CommandType.URGENT_TASKS, 0.90),
            ("important", CommandType.URGENT_TASKS, 0.85),
            ("critical tasks", CommandType.URGENT_TASKS, 0.85),
        ]
        
        for input_text, expected_command, min_confidence in test_cases:
            with self.subTest(input_text=input_text):
                result = self.parser.parse(input_text)
                self.assertEqual(result.command_type, expected_command)
                self.assertGreaterEqual(result.confidence, min_confidence - 0.1)
    
    def test_sync_status_recognition(self):
        """Test recognition of sync status commands"""
        test_cases = [
            ("status", CommandType.SYNC_STATUS, 0.95),
            ("sync status", CommandType.SYNC_STATUS, 0.95),
            ("sync", CommandType.SYNC_STATUS, 0.90),
            ("health check", CommandType.SYNC_STATUS, 0.85),
            ("check systems", CommandType.SYNC_STATUS, 0.80),
        ]
        
        for input_text, expected_command, min_confidence in test_cases:
            with self.subTest(input_text=input_text):
                result = self.parser.parse(input_text)
                self.assertEqual(result.command_type, expected_command)
                self.assertGreaterEqual(result.confidence, min_confidence - 0.1)
    
    def test_all_command_types(self):
        """Test that all major command types are recognized"""
        test_cases = [
            ("daily plan", CommandType.DAILY_PLAN),
            ("what's next", CommandType.WHAT_NEXT),
            ("capture test", CommandType.CAPTURE),
            ("urgent", CommandType.URGENT_TASKS),
            ("status", CommandType.SYNC_STATUS),
            ("projects", CommandType.CURRENT_PROJECTS),
            ("low energy", CommandType.LOW_ENERGY_TASKS),
            ("progress", CommandType.TODAY_PROGRESS),
            ("help", CommandType.HELP),
        ]
        
        for input_text, expected_command in test_cases:
            with self.subTest(input_text=input_text):
                result = self.parser.parse(input_text)
                self.assertEqual(result.command_type, expected_command)
                self.assertTrue(result.is_confident())
    
    def test_confidence_scoring(self):
        """Test confidence scoring accuracy"""
        # High confidence cases
        high_confidence_cases = [
            "daily plan",
            "what's next?",
            "capture meeting notes",
            "urgent tasks",
            "sync status"
        ]
        
        for input_text in high_confidence_cases:
            with self.subTest(input_text=input_text):
                result = self.parser.parse(input_text)
                self.assertGreater(result.confidence, 0.8)
                self.assertTrue(result.is_confident())
        
        # Lower confidence cases (but still valid)
        medium_confidence_cases = [
            "some daily plan stuff",
            "what about next task",
            "urgent something"
        ]
        
        for input_text in medium_confidence_cases:
            with self.subTest(input_text=input_text):
                result = self.parser.parse(input_text)
                if result.command_type != CommandType.UNKNOWN:
                    self.assertLess(result.confidence, 0.9)
    
    def test_unrecognized_input(self):
        """Test handling of unrecognized input"""
        unrecognized_inputs = [
            "xyz123",
            "random gibberish",
            "completely unrelated text",
            "",
            "   "
        ]
        
        for input_text in unrecognized_inputs:
            with self.subTest(input_text=input_text):
                result = self.parser.parse(input_text)
                self.assertEqual(result.command_type, CommandType.UNKNOWN)
                self.assertEqual(result.confidence, 0.0)
                self.assertFalse(result.is_confident())
                self.assertIsNotNone(result.suggestions)
                self.assertGreater(len(result.suggestions), 0)
    
    def test_typo_handling(self):
        """Test handling of common typos and variations"""
        typo_cases = [
            ("daliy plan", CommandType.DAILY_PLAN),  # Should still match with lower confidence
            ("whats next", CommandType.WHAT_NEXT),
            ("urgnt", None),  # Too different, should not match
        ]
        
        for input_text, expected_command in typo_cases:
            with self.subTest(input_text=input_text):
                result = self.parser.parse(input_text)
                if expected_command:
                    self.assertEqual(result.command_type, expected_command)
                else:
                    self.assertEqual(result.command_type, CommandType.UNKNOWN)
    
    def test_whitespace_normalization(self):
        """Test proper handling of whitespace"""
        test_cases = [
            "  daily plan  ",
            "\\tdaily\\tplan\\t",
            "daily  plan",  # Multiple spaces
            "daily\\nplan"   # Newline
        ]
        
        for input_text in test_cases:
            with self.subTest(input_text=input_text):
                result = self.parser.parse(input_text)
                self.assertEqual(result.command_type, CommandType.DAILY_PLAN)
                self.assertTrue(result.is_confident())
    
    def test_case_insensitivity(self):
        """Test case insensitive parsing"""
        test_cases = [
            "DAILY PLAN",
            "Daily Plan", 
            "daily PLAN",
            "DaIlY pLaN"
        ]
        
        for input_text in test_cases:
            with self.subTest(input_text=input_text):
                result = self.parser.parse(input_text)
                self.assertEqual(result.command_type, CommandType.DAILY_PLAN)
                self.assertTrue(result.is_confident())
    
    def test_parameter_extraction_edge_cases(self):
        """Test edge cases in parameter extraction"""
        test_cases = [
            ("capture", {}),  # No content
            ("capture ", {}),  # Just space after capture
            ("capture @urgent fix bug", {"content": "@urgent fix bug"}),  # Special characters
            ("capture 'quoted content'", {"content": "'quoted content'"}),  # Quoted content
            ("add task with, commas and; semicolons", {"content": "with, commas and; semicolons"}),
        ]
        
        for input_text, expected_params in test_cases:
            with self.subTest(input_text=input_text):
                result = self.parser.parse(input_text)
                self.assertEqual(result.command_type, CommandType.CAPTURE)
                
                if expected_params:
                    self.assertEqual(result.parameters, expected_params)
                else:
                    # Should either have no content key or empty content
                    if 'content' in result.parameters:
                        self.assertEqual(result.parameters['content'], '')
    
    def test_suggestion_generation(self):
        """Test suggestion generation for unrecognized input"""
        test_cases = [
            ("daily", []),  # Should be recognized, no suggestions needed
            ("plan", ["daily"]),  # Should suggest daily plan
            ("task", ["next", "capture"]),  # Should suggest task-related commands
            ("xyz123", ["daily", "next", "capture", "urgent", "status"]),  # Generic suggestions
        ]
        
        for input_text, expected_suggestion_keywords in test_cases:
            with self.subTest(input_text=input_text):
                result = self.parser.parse(input_text)
                
                if expected_suggestion_keywords:
                    self.assertIsNotNone(result.suggestions)
                    # Check that at least one suggestion contains expected keywords
                    suggestion_text = " ".join(result.suggestions).lower()
                    for keyword in expected_suggestion_keywords:
                        self.assertIn(keyword, suggestion_text)
    
    def test_confidence_threshold(self):
        """Test confidence threshold functionality"""
        # Test different thresholds
        result = self.parser.parse("daily plan")
        
        self.assertTrue(result.is_confident(0.5))  # Should pass low threshold
        self.assertTrue(result.is_confident(0.7))  # Should pass default threshold
        self.assertTrue(result.is_confident(0.9))  # Should pass high threshold
        self.assertFalse(result.is_confident(0.99))  # Should fail very high threshold
    
    def test_performance(self):
        """Test parser performance with various inputs"""
        import time
        
        test_inputs = [
            "daily plan",
            "what's next?",
            "capture meeting notes with lots of content here",
            "urgent",
            "status",
            "unrecognized input that should fail",
            "projects",
            "low energy tasks",
            "progress"
        ]
        
        start_time = time.time()
        
        for input_text in test_inputs:
            result = self.parser.parse(input_text)
            # Should complete quickly
            self.assertIsNotNone(result)
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Should process all inputs in under 1 second
        self.assertLess(total_time, 1.0)
        
        # Average time per parse should be reasonable
        avg_time = total_time / len(test_inputs)
        self.assertLess(avg_time, 0.1)  # Less than 100ms per parse


class TestCommandResult(unittest.TestCase):
    """Test cases for CommandResult dataclass"""
    
    def test_command_result_creation(self):
        """Test CommandResult creation and attributes"""
        result = CommandResult(
            command_type=CommandType.DAILY_PLAN,
            confidence=0.95,
            parameters={"test": "value"},
            raw_input="daily plan"
        )
        
        self.assertEqual(result.command_type, CommandType.DAILY_PLAN)
        self.assertEqual(result.confidence, 0.95)
        self.assertEqual(result.parameters, {"test": "value"})
        self.assertEqual(result.raw_input, "daily plan")
        self.assertIsNone(result.suggestions)
    
    def test_is_confident_method(self):
        """Test is_confident method with various confidence levels"""
        test_cases = [
            (0.95, 0.7, True),
            (0.70, 0.7, True),
            (0.69, 0.7, False),
            (0.50, 0.5, True),
            (0.49, 0.5, False),
            (1.0, 0.9, True),
            (0.0, 0.1, False),
        ]
        
        for confidence, threshold, expected in test_cases:
            with self.subTest(confidence=confidence, threshold=threshold):
                result = CommandResult(
                    command_type=CommandType.DAILY_PLAN,
                    confidence=confidence,
                    parameters={},
                    raw_input="test"
                )
                self.assertEqual(result.is_confident(threshold), expected)


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)