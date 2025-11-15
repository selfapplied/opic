#let margin-explain-direct(content) = {
  block(
    fill: rgb("EFF6FF"),
    stroke: 1pt + rgb("3B82F6"),
    radius: 4pt,
    inset: 8pt,
    width: 100%,
    [
      text(size: 8pt, fill: rgb("1E40AF"))[
        #text(weight: "bold")[Note:] #content
      ]
    ]
  )
}

= Direct Copy Test

#margin-explain-direct("This should work")
