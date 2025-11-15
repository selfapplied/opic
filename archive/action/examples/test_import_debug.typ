#import "typst_templates.typ": *

= Debug Import

Inline function works:
#let inline-test(content) = block(fill: blue.lighten(90%), inset: 8pt)[#content]
#inline-test("Inline works")

Imported function shows literal code:
#margin-explain("This shows literal code")
