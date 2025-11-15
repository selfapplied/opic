#import "typst_templates.typ": *

= Verification Test

Test margin note:
#margin-explain("This should render as a styled note, not literal code.")

Test code block:
#ops-code[
  voice test / {input -> output}
]

Test equation:
#fee-equation()
