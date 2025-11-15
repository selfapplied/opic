#let margin-explain-fixed(content) = {
  block(
    fill: rgb("EFF6FF"),
    stroke: 1pt + rgb("3B82F6"),
    radius: 4pt,
    inset: 8pt,
    width: 100%,
    text(size: 8pt, fill: rgb("1E40AF"))[
      *Note:* #content
    ]
  )
}

= Fixed Test

#margin-explain-fixed("This should work without nested text()")
