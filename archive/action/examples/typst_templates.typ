// Typst template functions for opic documents
// Include this in your Typst documents: #include "typst_templates.typ"

// ============================================================================
// OPS SYNTAX COLORING
// ============================================================================

#let ops-code(body) = {
  block(
    fill: rgb("F9FAFB"),
    stroke: 1pt + rgb("E5E7EB"),
    radius: 4pt,
    inset: 12pt,
    width: 100%,
    text(size: 9pt, fill: rgb("1F2937"))[
      #body
    ]
  )
}

#let highlight-ops(code) = {
  // OPS syntax highlighting - simplified version using regex replacement
  code
}

// ============================================================================
// MARGIN NOTES / EXPLAIN MARGINS
// ============================================================================

#let margin-explain(content) = {
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

#let margin-warning(content) = {
  block(
    fill: rgb("FEF3C7"),
    stroke: 1pt + rgb("F59E0B"),
    radius: 4pt,
    inset: 8pt,
    width: 100%,
    text(size: 8pt, fill: rgb("92400E"))[
      *Warning:* #content
    ]
  )
}

#let margin-tip(content) = {
  block(
    fill: rgb("D1FAE5"),
    stroke: 1pt + rgb("10B981"),
    radius: 4pt,
    inset: 8pt,
    width: 100%,
    text(size: 8pt, fill: rgb("065F46"))[
      *Tip:* #content
    ]
  )
}

// ============================================================================
// CRYPTOGRAPHIC SEALS
// ============================================================================

#let cryptographic-seal(signature, realm, ca, style: "certificate") = {
  [
    #align(center)[
      #block(
        fill: rgb("F9FAFB"),
        stroke: 2pt + rgb("6366F1"),
        radius: 8pt,
        inset: 16pt,
        width: 60%,
        [
        #if style == "certificate" [
          #text(size: 10pt, fill: rgb("4F46E5"), weight: "bold")[CERTIFICATE]
          #v(8pt)
        ] else if style == "witness" [
          #text(size: 10pt, fill: rgb("7C3AED"), weight: "bold")[WITNESS]
          #v(8pt)
        ] else [
          #text(size: 10pt, fill: rgb("059669"), weight: "bold")[SIGNED]
          #v(8pt)
        ]
        
        #text(size: 9pt, fill: rgb("374151"))[
          Realm: *#realm*
          #v(4pt)
          CA: *#ca*
          #v(8pt)
          Signature: #text(size: 7pt)[#signature]
        ]
      ]
    )
    ]
  ]
}

#let seal-certificate(signature, realm, ca) = {
  cryptographic-seal(signature, realm, ca, style: "certificate")
}

#let seal-witness(signature, realm, ca) = {
  cryptographic-seal(signature, realm, ca, style: "witness")
}

#let seal-signed(signature, realm, ca) = {
  cryptographic-seal(signature, realm, ca, style: "signed")
}

// ============================================================================
// BEAUTIFUL FIELD EQUATIONS
// ============================================================================

// Debug mode detection from environment
#let is-debug-mode = sys.inputs.at("DEBUG", default: none) != none

// Debug helper for layout diagnosis
#let debug-frame(content, debug: auto) = {
  let debug-enabled = if debug == auto { is-debug-mode } else { debug }
  if debug-enabled {
    block(
      stroke: 0.5pt + rgb("F59E0B"),
      inset: 4pt,
      radius: 3pt,
      fill: rgb("FEF3C7"),
      [#content]
    )
  } else {
    content
  }
}

// Bloom icon for use next to equations (small decorative flower)
// Different types generate different bloom patterns
#let bloom-icon(size: 24pt, type: "default") = {
  let svg-path = if type == "wave" {
    "images/bloom_wave.svg"
  } else if type == "energy" {
    "images/bloom_energy.svg"
  } else if type == "coherence" {
    "images/bloom_coherence.svg"
  } else if type == "zeta" {
    "images/bloom_zeta.svg"
  } else if type == "flux" {
    "images/bloom_flux.svg"
  } else if type == "xi" {
    "images/bloom_xi.svg"
  } else {
    "images/bloom_icon.svg"
  }
  image(svg-path, height: size, fit: "contain")
}

#let field-equation(eq, vars: none, explanation: none, icon: true, icon-type: "default") = {
  debug-frame(
    block(
      fill: rgb("FAFBFC"),
      stroke: 1pt + rgb("E5E7EB"),
      radius: 6pt,
      inset: 16pt,
      width: 90%,
      [
        #if explanation != none [
          #text(size: 9pt, fill: rgb("6B7280"), style: "italic")[#explanation]
          #v(8pt)
        ]
        
        #grid(
          columns: (auto, 1fr),
          column-gutter: 6pt,
          [
            #if icon [
              #align(top)[#bloom-icon(size: 18pt, type: icon-type)]
            ]
            #block(
              fill: white,
              stroke: 0.5pt + rgb("D1D5DB"),
              radius: 4pt,
              inset: 12pt,
              eq
            )
          ]
        )
        
        #if vars != none [
          #v(8pt)
          #text(size: 8pt, fill: rgb("6B7280"))[
            Where: #vars
          ]
        ]
      ]
    )
  )
}

#let fee-equation(icon-type: "coherence", debug: auto) = {
  field-equation(
    $f(Delta t, Delta Phi, "proof_of_care") = sum_(i) w_i * (t_i + Phi_i + v_i)$,
    vars: "tau = (t, Phi, v)",
    explanation: "Field Equation Exchange: Learning Energy Units computed from time, coherence, and validation",
    icon-type: icon-type
  )
}

#let coherence-equation(icon-type: "coherence", debug: auto) = {
  field-equation(
    $(d Phi)/(d t) = "div" J + S$,
    vars: "Phi = field state, J = current, S = source",
    explanation: "Field coherence evolution: rate of change equals divergence of current plus sources",
    icon-type: icon-type
  )
}

#let zeta-equation(icon-type: "zeta", debug: auto) = {
  field-equation(
    $zeta(s) = chi(s) * zeta(1 - s)$,
    vars: "s = 1/2 + i*t",
    explanation: "Riemann zeta functional equation: symmetry across the critical line",
    icon-type: icon-type
  )
}

// ============================================================================
// DRAW SYSTEM / 2D VISUALIZATION
// ============================================================================

#let draw-diagram(svg-path, width: 100%, caption: none) = {
  block(
    fill: rgb("FAFBFC"),
    stroke: 1pt + rgb("E5E7EB"),
    radius: 6pt,
    inset: 12pt,
    width: width,
    [
      #align(center)[
        #image(svg-path, width: width)
      ]
      
      #if caption != none [
        #v(8pt)
        #text(size: 8pt, fill: rgb("6B7280"), style: "italic")[
          #align(center)[#caption]
        ]
      ]
    ]
  )
}

// Helper functions for draw system integration
// Use #draw-diagram() directly with SVG file paths
// Or use typst.draw_svg primitive from Opic to generate SVG from draw definitions

// ============================================================================
// RADIANT BLOOM / RADIAL PETAL VISUALIZATION
// ============================================================================

#let bloom-diagram(svg-path, width: 100%, caption: none) = {
  block(
    fill: rgb("FAFBFC"),
    stroke: 1pt + rgb("E5E7EB"),
    radius: 6pt,
    inset: 12pt,
    width: width,
    [
      #align(center)[
        #image(svg-path, width: width)
      ]
      
      #if caption != none [
        #v(8pt)
        #text(size: 8pt, fill: rgb("6B7280"), style: "italic")[
          #align(center)[#caption]
        ]
      ]
    ]
  )
}

// Radiant bloom visualization for Riemann Hypothesis field traces
// Each petal/ray represents a field trace with:
// - Angle (θ) = position in sequence
// - Radius (r) = entropy (phi_entropy)
// - Color = file/author (hue)
// - Opacity = boundary_score

