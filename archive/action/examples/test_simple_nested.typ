#let test-simple(content) = block(fill: blue.lighten(90%), inset: 8pt)[#content]

#let test-nested(content) = block(fill: blue.lighten(90%), inset: 8pt)[
  text(size: 8pt)[Note: #content]
]

#let test-double-nested(content) = block(fill: blue.lighten(90%), inset: 8pt)[
  [
    text(size: 8pt)[Note: #content]
  ]
]

= Test

#test-simple("Simple works")
#test-nested("Nested?")
#test-double-nested("Double nested?")
