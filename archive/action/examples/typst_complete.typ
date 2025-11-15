#import "typst_templates.typ": *

#set page(margin: (x: 2.5cm, y: 2cm))
#set text(size: 11pt)

= Opic Language Documentation

#v(0.5cm)

Opic is a self-hosting language for distributed computation with cryptographic trust.

== Features

- *Self-hosting*: Opic defines itself in `.ops` files
- *Cryptographic trust*: Each voice is signed with a certificate
- *Field equations*: Programs evolve under field dynamics
- *Compositional*: Voices compose naturally into chains

#margin-explain("Voices are opic's fundamental unit of computation. They transform inputs to outputs.")

== OPS Syntax Example

Here's a simple opic voice with syntax highlighting:

#ops-code[
  voice greet / {name -> "Hello " + name -> greeting}
  voice main / {greet "world" -> greet}
]

This demonstrates opic's compositional elegance: voices transform inputs to outputs, and compose naturally.

== Field Equations

Opic's architecture expresses field dynamics through mathematical equations:

#fee-equation()

#margin-tip("The field equation computes Learning Energy Units from time, coherence, and validation.")

The coherence equation describes how fields evolve:

#coherence-equation()

== Cryptographic Seals

Each opic voice can be cryptographically signed:

#seal-certificate("sha256:abc123def456...", "opic_realm", "opic_ca")

#seal-witness("sha256:witness789...", "opic_realm", "opic_ca")

#margin-warning("Always verify signatures before executing voices from untrusted sources.")

== Architecture

Opic's architecture naturally expresses the duality at the heart of analytic number theory:

- *Left Flank — Category (Discrete)*: voices compose into a spectrum of prime morphisms
- *Right Flank — Field (Continuous)*: coherence evolves under field equations  
- *Bridge — Certificate Operator*: a unitary transformation equating the two halves

#margin-explain("This duality mirrors the Riemann zeta function's functional equation.")

The zeta equation demonstrates this symmetry:

#zeta-equation()

== Conclusion

Opic combines mathematical elegance with practical cryptographic trust, enabling distributed computation with built-in verification.

#v(1cm)

#align(center)[
  #seal-signed("sha256:final...", "opic_realm", "opic_ca")
]

