#import "typst_templates.typ": *

= Test

#let test-func(content) = {
  block(fill: rgb("EFF6FF"), stroke: 1pt + rgb("3B82F6"), inset: 8pt)[
    #content
  ]
}

#test-func("This should work")

#margin-explain("This should also work")
