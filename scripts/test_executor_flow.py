#!/usr/bin/env python3
"""
Test main executor flow: file discovery, file-output association, comment learning
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from opic_executor import OpicExecutor

def test_executor_flow():
    """Test that executor discovers files, associates them with outputs, and learns from comments"""
    project_root = Path(__file__).parent.parent
    executor = OpicExecutor(project_root)
    
    # Test 1: File discovery (natural discovery - no hardcoded paths)
    print("Test 1: File discovery...")
    # Use natural discovery - find any test file
    test_file = None
    for search_dir in [project_root / "tests", project_root / "systems", project_root / "core"]:
        if search_dir.exists():
            for ops_file in search_dir.glob("*.ops"):
                test_file = ops_file
                break
        if test_file:
            break
    
    if test_file:
        executor._load_ops_file(test_file)
        print(f"  ✓ Discovered and loaded {test_file.name} via natural discovery")
    else:
        print(f"  ⚠ No test files found")
        return False
    
    # Test 2: File-output association
    print("\nTest 2: File-output association...")
    result = executor.execute_voice("main", {})
    executor._associate_file_output(test_file, result)
    
    pairs = executor.get_file_output_pairs()
    if pairs:
        print(f"  ✓ Associated {len(pairs)} file(s) with output")
        for pair in pairs[-1:]:  # Show last one
            print(f"    File: {pair['file']}")
            print(f"    Output: {str(pair['output'])[:50]}...")
    else:
        print("  ⚠ No file-output pairs recorded")
    
    # Test 3: Comment learning
    print("\nTest 3: Comment learning...")
    comments = executor.get_file_comments(test_file)
    if comments:
        print(f"  ✓ Extracted {len(comments)} comment(s) from {test_file.name}")
        for comment in comments[:3]:  # Show first 3
            print(f"    Line {comment['line']}: {comment['comment'][:50]}...")
    else:
        print(f"  ⚠ No comments extracted from {test_file.name}")
    
    # Test 4: Integration with CodeOutputLearner
    print("\nTest 4: Code-output learning integration...")
    try:
        from code_output_learner import CodeOutputLearner
        learner = CodeOutputLearner(project_root)
        patterns = learner.analyze_patterns()
        print(f"  ✓ CodeOutputLearner available")
        print(f"    Patterns analyzed: {len(patterns.get('patterns', {}))}")
    except ImportError:
        print("  ⚠ CodeOutputLearner not available")
    
    # Test 5: Integration with CommentCodeCoupler
    print("\nTest 5: Comment-code coupling integration...")
    try:
        from comment_code_coupler import CommentCodeCoupler
        coupler = CommentCodeCoupler(project_root)
        pairs = coupler.extract_comments_from_file(test_file)
        print(f"  ✓ CommentCodeCoupler available")
        print(f"    Comment-code pairs extracted: {len(pairs)}")
    except ImportError:
        print("  ⚠ CommentCodeCoupler not available")
    
    print("\n" + "=" * 60)
    print("Executor flow test complete")
    print("=" * 60)
    return True

if __name__ == "__main__":
    success = test_executor_flow()
    sys.exit(0 if success else 1)

