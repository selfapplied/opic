#import "../systems/typst_templates.typ": *

#set page(margin: 2cm)

= Test Document

Testing margin note:
#margin-explain("This is a test note")

Testing code block:
#ops-code[
  voice test / {input -> output}
]

Testing equation:
#fee-equation()

Testing seal:
#seal-certificate("test123", "realm", "ca")

