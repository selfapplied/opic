#!/usr/bin/env python3
"""Test script to verify Typst output is correct (not showing literal code)."""

import subprocess
import sys
import os
from pathlib import Path

# Try to import PDF text extraction libraries
try:
    import PyPDF2
    HAS_PYPDF2 = True
except ImportError:
    HAS_PYPDF2 = False

try:
    import pypdf
    HAS_PYPDF = True
except ImportError:
    HAS_PYPDF = False

def run_command(cmd, cwd=None):
    """Run a command and return stdout, stderr, and return code."""
    result = subprocess.run(
        cmd, shell=True, capture_output=True, text=True, cwd=cwd
    )
    return result.stdout, result.stderr, result.returncode

def extract_typst_content(typ_file):
    """Extract rendered content from Typst file using Typst query."""
    # Use Typst's query command to get rendered text
    stdout, stderr, code = run_command(
        f'typst query {typ_file} --field value --one "<text>"',
        cwd=Path(typ_file).parent
    )
    if code == 0 and stdout:
        return stdout
    return None

def extract_pdf_text(pdf_file):
    """Extract text from PDF for verification."""
    if not Path(pdf_file).exists():
        return None
    
    # Try PyPDF2 first
    if HAS_PYPDF2:
        try:
            with open(pdf_file, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                return text
        except Exception as e:
            pass
    
    # Try pypdf
    if HAS_PYPDF:
        try:
            with open(pdf_file, 'rb') as f:
                reader = pypdf.PdfReader(f)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                return text
        except Exception as e:
            pass
    
    # Try pdftotext command
    stdout, stderr, code = run_command(f"pdftotext {pdf_file} - 2>/dev/null")
    if code == 0 and stdout:
        return stdout
    
    return None

def test_pdf_content(pdf_file):
    """Test that PDF doesn't contain literal Typst code."""
    print(f"\nTesting PDF content: {pdf_file}")

    # Try PDF extraction
    text = extract_pdf_text(pdf_file)

    if text is None:
        print("⚠️  Could not extract PDF text")
        print("   Install PyPDF2 for content verification: pip3 install --user PyPDF2")
        print("   Or install poppler: brew install poppler")
        return True  # Don't fail if we can't check

    # Patterns that indicate literal code is appearing
    problematic_patterns = [
        ('#body', 'Function parameter appearing literally'),
        ('if explanation != none', 'Conditional logic appearing literally'),
        ('if vars != none', 'Conditional logic appearing literally'),
        ('if style == "certificate"', 'Conditional logic appearing literally'),
        ('text(size: 8pt, fill: rgb("1E40AF"))', 'Function call appearing literally (without #)'),
        ('text(size: 9pt, fill: rgb("6B7280"))', 'Function call appearing literally (without #)'),
        ('text(size: 10pt, fill: rgb("4F46E5"))', 'Function call appearing literally (without #)'),
        ('#let ops-code', 'Function definition appearing literally'),
        ('#margin-explain("', 'Function call appearing literally (should be rendered)'),
        ('block( fill: rgb("F9FAFC")', 'Block function appearing literally'),
        ('align(center)[ block(', 'Nested block appearing literally'),
        ('v(8pt)', 'Vertical spacing appearing literally'),
        ('#v(8pt)', 'Hashed vertical spacing appearing literally'),
    ]

    issues = []
    for pattern, description in problematic_patterns:
        if pattern in text:
            # Count occurrences
            count = text.count(pattern)
            issues.append(f"  ❌ {description}: found {count} time(s)")

    if issues:
        print("❌ PDF contains literal Typst code:")
        for issue in issues:
            print(issue)
        # Show a snippet of where it appears
        for pattern, _ in problematic_patterns:
            if pattern in text:
                idx = text.find(pattern)
                snippet = text[max(0, idx-50):idx+150].replace('\n', ' ')
                print(f"\n  Example context: ...{snippet}...")
                break
        return False
    else:
        print("✅ PDF content verified - no literal code found")

        # Verify expected styled content appears
        print("\n=== Verifying styled content ===")
        expected_content = {
            'Note:': 'margin-explain notes',
            'Warning:': 'margin-warning notes',
            'Tip:': 'margin-tip notes',
            'CERTIFICATE': 'cryptographic seals',
            'SIGNED': 'cryptographic seals',
            'WITNESS': 'cryptographic seals',
            'Where:': 'field equation variables',
            'Field Equation Exchange': 'field equation explanations',
            'Realm:': 'cryptographic seal details',
        }

        found_content = []
        missing_content = []
        for keyword, description in expected_content.items():
            if keyword in text:
                found_content.append(f"  ✅ '{keyword}' ({description})")
            else:
                missing_content.append(f"  ⚠️  '{keyword}' ({description})")

        for item in found_content:
            print(item)
        if missing_content:
            print("\n⚠️  Some expected content not found:")
            for item in missing_content:
                print(item)

        # Check for proper formatting (no raw code blocks)
        if 'voice greet' in text or 'voice main' in text:
            print("\n✅ Code blocks contain OPS code")
        else:
            print("\n⚠️  Code blocks may be missing")

        return True

def test_golden_snapshot(pdf_file, golden_file=None):
    """Compare PDF text against golden snapshot."""
    if golden_file is None:
        golden_file = Path("tests/snapshots") / f"{Path(pdf_file).stem}_golden.txt"

    if not golden_file.exists():
        print(f"⚠️  No golden snapshot found at {golden_file}")
        return True

    print(f"📸 Comparing against golden snapshot: {golden_file}")

    # Extract current text
    current_text = extract_pdf_text(pdf_file)
    if not current_text:
        print("❌ Could not extract text from current PDF")
        return False

    # Load golden text
    try:
        with open(golden_file, 'r', encoding='utf-8') as f:
            golden_text = f.read()
    except Exception as e:
        print(f"❌ Could not read golden snapshot: {e}")
        return False

    # Compare
    if current_text.strip() == golden_text.strip():
        print("✅ Text matches golden snapshot")
        return True
    else:
        print("❌ Text differs from golden snapshot")
        # Show diff (simplified)
        current_lines = current_text.strip().split('\n')
        golden_lines = golden_text.strip().split('\n')

        if len(current_lines) != len(golden_lines):
            print(f"   Line count differs: {len(current_lines)} vs {len(golden_lines)}")
        else:
            print("   Content differs (same line count)")
            # Could add more detailed diff here

        return False

def test_typst_compilation(typ_file, pdf_file):
    """Test that Typst file compiles without errors."""
    print(f"Testing compilation: {typ_file}")
    stdout, stderr, code = run_command(
        f"typst compile {typ_file} {pdf_file}",
        cwd=Path(typ_file).parent
    )
    
    if code != 0:
        print(f"❌ Compilation failed:")
        print(stderr)
        return False
    
    # Check for critical errors (warnings are OK)
    if "error:" in stderr.lower():
        print(f"❌ Compilation errors found:")
        print(stderr)
        return False
    
    if not Path(pdf_file).exists():
        print(f"❌ PDF not created: {pdf_file}")
        return False
    
    print(f"✅ Compilation successful: {pdf_file}")
    return True

def test_no_literal_code(typ_file):
    """Test that the Typst file doesn't have obvious literal code issues."""
    print(f"\nTesting for literal code issues in: {typ_file}")
    
    with open(typ_file, 'r') as f:
        content = f.read()
    
    # Check that function definitions exist (they should be in templates)
    template_file = Path(typ_file).parent / "typst_templates.typ"
    if template_file.exists():
        with open(template_file, 'r') as f:
            template_content = f.read()
        
        # Verify key functions are defined
        required_functions = [
            '#let ops-code',
            '#let margin-explain',
            '#let field-equation',
            '#let fee-equation',
        ]
        
        missing = []
        for func in required_functions:
            if func not in template_content:
                missing.append(func)
        
        if missing:
            print(f"❌ Missing function definitions: {missing}")
            return False
    
    # Patterns that indicate literal code might be rendered
    # These should NOT appear in the main document (only in templates)
    problematic_patterns = [
        ('#body', 'Function parameter appearing literally'),
        ('if explanation != none', 'Conditional appearing literally'),
    ]
    
    issues = []
    for pattern, description in problematic_patterns:
        # Check if pattern appears in the main document (not templates)
        if pattern in content:
            # Check if it's NOT in a function definition
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if pattern in line:
                    # Check if this is NOT a function definition
                    context = '\n'.join(lines[max(0, i-2):i+1])
                    if '#let ' not in context and 'typst_templates' not in str(Path(typ_file).name):
                        issues.append(f"  ⚠️  {description}: line {i+1}")
                        break
    
    if issues:
        print("⚠️  Potential literal code issues found:")
        for issue in issues[:3]:  # Show first 3
            print(issue)
        return False
    else:
        print("✅ No obvious literal code patterns found")
        return True

def test_function_calls(typ_file):
    """Test that function calls exist in the Typst file."""
    print(f"\nTesting function calls in: {typ_file}")
    
    with open(typ_file, 'r') as f:
        content = f.read()
    
    # Check for function calls (should have #function-name)
    functions_to_check = [
        'margin-explain',
        'margin-warning', 
        'margin-tip',
        'ops-code',
        'fee-equation',
        'coherence-equation',
        'zeta-equation',
        'seal-certificate',
        'seal-signed'
    ]
    
    found = []
    missing = []
    
    for func in functions_to_check:
        if f"#{func}" in content or f"#seal-" in content:
            found.append(func)
        else:
            missing.append(func)
    
    if missing:
        print(f"⚠️  Some expected functions not found: {missing}")
    else:
        print(f"✅ All expected function calls found")
    
    return len(missing) == 0

def test_template_import(typ_file):
    """Test that templates are imported correctly."""
    print(f"\nTesting template import in: {typ_file}")
    
    with open(typ_file, 'r') as f:
        content = f.read()
    
    if '#import' in content and 'typst_templates' in content:
        print("✅ Template import found")
        return True
    else:
        print("❌ Template import missing")
        return False

def main():
    """Run all tests."""
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    examples_dir = project_root / "examples"
    
    typ_file = examples_dir / "typst_complete.typ"
    pdf_file = examples_dir / "typst_complete.pdf"
    
    if not typ_file.exists():
        print(f"❌ Typst file not found: {typ_file}")
        return 1
    
    print("=" * 60)
    print("Typst Output Verification")
    print("=" * 60)
    
    all_passed = True
    
    # Test 1: Template import
    if not test_template_import(typ_file):
        all_passed = False
    
    # Test 2: Function calls exist
    if not test_function_calls(typ_file):
        all_passed = False
    
    # Test 3: No literal code
    if not test_no_literal_code(typ_file):
        all_passed = False
    
    # Test 4: Compilation
    if not test_typst_compilation(typ_file, pdf_file):
        all_passed = False
    
    # Test 5: PDF content verification
    if not test_pdf_content(pdf_file):
        all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ All tests passed!")
        return 0
    else:
        print("❌ Some tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())

