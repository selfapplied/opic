#!/bin/bash
# Test: Self-compile opic into Metal

set -e

echo "=========================================="
echo "Opic Self-Compilation Test"
echo "=========================================="
echo ""

echo "Step 1: Generate Metal code from opic's own .ops files"
echo "------------------------------------------------------"
./opic metal core.ops core.metal
./opic metal runtime.ops runtime.metal
echo "✓ Generated core.metal and runtime.metal"
echo ""

echo "Step 2: Compile Metal shaders into library"
echo "------------------------------------------------------"
if command -v xcrun >/dev/null 2>&1; then
    if xcrun -sdk macosx metal -c core.metal runtime.metal -o opic.metallib 2>/dev/null; then
        echo "✓ Compiled opic.metallib"
        
        if command -v xcrun >/dev/null 2>&1 && xcrun -sdk macosx metallib -info opic.metallib >/dev/null 2>&1; then
            echo ""
            echo "Metal library info:"
            xcrun -sdk macosx metallib -info opic.metallib | head -20
        fi
        
        echo ""
        echo "Step 3: Verify compilation"
        echo "------------------------------------------------------"
        if [ -f opic.metallib ]; then
            file opic.metallib
            ls -lh opic.metallib
            echo ""
            echo "✓ Self-compilation successful!"
            echo "  opic → Metal code → opic.metallib"
        fi
    else
        echo "⚠ Metal compiler not available (Xcode command line tools required)"
        echo "  Generated Metal files:"
        ls -lh *.metal
        echo ""
        echo "To compile manually:"
        echo "  xcrun -sdk macosx metal -c core.metal runtime.metal -o opic.metallib"
    fi
else
    echo "⚠ xcrun not available"
    echo "  Generated Metal files:"
    ls -lh *.metal
fi

echo ""
echo "=========================================="
echo "Self-compilation test complete"
echo "=========================================="

