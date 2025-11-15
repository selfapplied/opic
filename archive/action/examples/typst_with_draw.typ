#import "typst_templates.typ": *

#set page(margin: (x: 2.5cm, y: 2cm))
#set text(size: 11pt)

= Opic Draw System Integration

Opic's draw system generates 2D visualizations that can be embedded in Typst documents.

== Canvas Visualization

#draw-diagram("draw_test_simple.svg", width: 80%, caption: "Example canvas from draw system")

== Field Equations with Diagrams

#fee-equation()

#margin-tip("Diagrams can illustrate field dynamics visually.")

== Conclusion

The draw system enables rich 2D visualizations alongside mathematical equations and code.
