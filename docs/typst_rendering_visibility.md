# Typst Rendering Visibility

opic now has built-in visibility into how Typst documents are rendered. This allows opic to verify its own output without manual inspection.

## Primitives

### `typst.inspect_pdf`
Extract text content from a rendered PDF.

```ops
voice check.rendering / {pdf_path -> typst.inspect_pdf -> extracted_text}
```

### `typst.verify`
Verify PDF rendering - checks for literal code and expected content.

```ops
voice verify.output / {pdf_path -> typst.verify -> verification_report}
```

## Usage

### Basic Verification

```ops
include systems/typst.ops
include systems/typst_inspection.ops

voice render.and.verify / {
  typst_document + output_path 
  -> typst.render 
  -> typst.verify 
  -> verification_report
}
```

### Extract Rendered Content

```ops
voice inspect.pdf / {
  "examples/output.pdf"
  -> typst.inspect
  -> rendered_text
}
```

## What Gets Checked

The verification system checks for:

**Problems (literal code appearing):**
- Function parameters (`#body`)
- Conditional logic (`if explanation != none`)
- Function calls (`text(size:`, `block( fill:`)
- Vertical spacing (`v(8pt)`)

**Expected Content:**
- Margin notes (`Note:`, `Warning:`, `Tip:`)
- Cryptographic seals (`CERTIFICATE`, `SIGNED`)
- Equation variables (`Where:`)

## Example

See `examples/typst_self_verify.ops` for a complete example of opic verifying its own Typst rendering.

