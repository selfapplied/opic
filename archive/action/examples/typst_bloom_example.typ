#import "typst_templates.typ": *

#set page(margin: (x: 2.5cm, y: 2cm))
#set text(size: 11pt)

= Radiant Bloom Visualization

The radiant bloom system generates radial petal diagrams from field traces, visualizing coherence patterns related to the Riemann Hypothesis.

== Bloom Diagram

#bloom-diagram("bloom_test.svg", width: 80%, caption: "Radiant bloom: field traces as radial petals")

#margin-explain("Each petal represents a field trace. Angle = position, radius = entropy, color = file/author.")

== Field Equations

#zeta-equation()

#margin-tip("The bloom visualization connects field dynamics to zeta function structure through coherence patterns.")
