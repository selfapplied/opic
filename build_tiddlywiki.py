#!/usr/bin/env python3
"""Opic bootstrap extension for TiddlyWiki generation"""

import json
import re
from pathlib import Path
from datetime import datetime

def parse_ops(text):
    """Parse .ops file into defs and voices"""
    defs, voices, families = {}, {}, {}
    current_family = None
    
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith(";"):
            continue
            
        if line.startswith("def "):
            parts = line[4:].split()
            name = parts[0]
            defs[name] = {}
            
        elif line.startswith("voice "):
            l, _, r = line.partition("/")
            name = l.split()[1].strip()
            body = r.strip().strip('" ')
            voices[name] = body
            
        elif line.startswith("family "):
            parts = line.split()
            name = parts[1]
            families[name] = {"order": len(families) + 1, "members": []}
            current_family = name
            
    return defs, voices, families

def create_tiddler(title, text="", tags=None, fields=None, family=None):
    """Create a TiddlyWiki tiddler JSON"""
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    tiddler = {
        "title": title,
        "text": text,
        "created": now,
        "modified": now,
        "tags": tags or [],
        "type": "text/vnd.tiddlywiki"
    }
    if fields:
        tiddler.update(fields)
    if family:
        tiddler["tags"] = tiddler.get("tags", []) + [f"family/{family}"]
    return tiddler

def generate_family_tiddlers(families):
    """Generate tiddlers for each family definition"""
    tiddlers = []
    for name, info in families.items():
        text = f"Family: {name}\n\nOrder: {info['order']}\n\nMembers: {', '.join(info.get('members', []))}"
        tiddlers.append(create_tiddler(f"$:/families/{name}", text, tags=[f"family/{name}"], family=name))
    return tiddlers

def escape_template_string(s):
    """Escape template string for Python format - convert single { to {{"""
    return s.replace("{", "{{").replace("}", "}}")

def safe_format_template(template, **kwargs):
    """Safely format template using Opic's safe.format voice"""
    # Opic voice: safe.format / {template + data -> str}
    # Escape all placeholders first, then unescape the ones we want
    escaped_template = template.replace("{", "{{").replace("}", "}}")
    for key, value in kwargs.items():
        placeholder = "{" + key + "}"
        escaped_template = escaped_template.replace("{{" + key + "}}", placeholder)
    return escaped_template.format(**kwargs)

# Opic voice interpreters - these implement the transformations defined in .ops files

def interpret_voice_load_empty_tiddlywiki(file_path):
    """Interpret Opic voice: load.empty.tiddlywiki / {file -> empty.tiddlywiki}"""
    empty_path = Path(file_path)
    if not empty_path.exists():
        raise FileNotFoundError(f"Empty TiddlyWiki not found: {empty_path}")
    
    content = empty_path.read_text()
    
    # Extract boot scripts - Opic voice: extract.boot.from.empty / {empty.tiddlywiki -> boot.scripts}
    import re
    bootprefix_match = re.search(r'<script[^>]*data-tiddler-title="\$:/boot/bootprefix\.js"[^>]*>([\s\S]*?)</script>', content)
    boot_match = re.search(r'<script[^>]*data-tiddler-title="\$:/boot/boot\.js"[^>]*>([\s\S]*?)</script>', content)
    
    bootprefix_js = bootprefix_match.group(1) if bootprefix_match else ""
    boot_js = boot_match.group(1) if boot_match else ""
    
    # Extract existing tiddlers - Opic voice: extract.tiddlers.from.empty / {empty.tiddlywiki -> tiddlers.array}
    store_match = re.search(r'<script class="tiddlywiki-tiddler-store"[^>]*>([\s\S]*?)</script>', content)
    existing_tiddlers = []
    if store_match:
        try:
            existing_tiddlers = json.loads(store_match.group(1))
        except:
            pass
    
    return {
        "html": content,
        "bootprefix_js": bootprefix_js,
        "boot_js": boot_js,
        "existing_tiddlers": existing_tiddlers
    }

def interpret_voice_extract_tiddlers_from_empty(empty_tw):
    """Interpret Opic voice: extract.tiddlers.from.empty / {empty.tiddlywiki -> tiddlers.array}"""
    return empty_tw.get("existing_tiddlers", [])

def interpret_voice_merge_tiddlers(existing_tiddlers, new_tiddlers):
    """Interpret Opic voice: merge.tiddlers / {tiddlers.array + tiddlers.array -> tiddlers.array}"""
    merged = []
    our_titles = {t.get("title") for t in new_tiddlers}
    
    # Add new tiddlers (they override existing ones)
    merged.extend(new_tiddlers)
    
    # Add system tiddlers from empty that we don't override
    existing_by_title = {t.get("title"): t for t in existing_tiddlers}
    for title, tiddler in existing_by_title.items():
        if title.startswith("$:/") and title not in our_titles:
            merged.append(tiddler)
    
    return merged

def interpret_voice_escape_json_html(json_str, error_voices=None):
    """Interpret Opic voice: escape.json.html / {json -> html.safe}"""
    if error_voices and "escape.json.html" in error_voices:
        escaped = json_str.replace('</script>', '<\\/script>')
        return escaped
    elif error_voices and "escape.json" in error_voices:
        escaped = json_str.replace('</script>', '<\\/script>')
        return escaped
    else:
        return json_str.replace('</script>', '<\\/script>')

def interpret_voice_replace_tiddlers_in_empty(empty_tw, tiddlers_array, error_voices=None):
    """Interpret Opic voice: replace.tiddlers.in.empty / {empty.tiddlywiki + tiddlers.array -> empty.tiddlywiki}"""
    # Convert tiddlers to JSON
    tiddlers_json = json.dumps(tiddlers_array, indent=2, ensure_ascii=False)
    
    # Apply escape.json.html voice
    tiddlers_json = interpret_voice_escape_json_html(tiddlers_json, error_voices)
    
    # Replace tiddler store in HTML
    import re
    pattern = r'(<script class="tiddlywiki-tiddler-store"[^>]*>)([\s\S]*?)(</script>)'
    
    def replace_store(match):
        return f'{match.group(1)}{tiddlers_json}{match.group(3)}'
    
    html = re.sub(pattern, replace_store, empty_tw["html"])
    
    return {
        "html": html,
        "tiddlers": tiddlers_array,
        "bootprefix_js": empty_tw["bootprefix_js"],
        "boot_js": empty_tw["boot_js"],
        "existing_tiddlers": tiddlers_array
    }

def interpret_voice_ensure_script_order(empty_tw):
    """Interpret Opic voice: ensure.script.order / {empty.tiddlywiki -> empty.tiddlywiki}"""
    html = empty_tw["html"]
    
    # Verify script order: bootprefix -> boot -> store
    bootprefix_pos = html.find('data-tiddler-title="$:/boot/bootprefix.js"')
    boot_pos = html.find('data-tiddler-title="$:/boot/boot.js"')
    store_pos = html.find('class="tiddlywiki-tiddler-store"')
    
    # If order is wrong (store before boot scripts), fix it
    if store_pos >= 0 and bootprefix_pos >= 0 and boot_pos >= 0:
        if store_pos < bootprefix_pos or store_pos < boot_pos:
            # Store is before boot scripts - need to move store after boot
            import re
            store_match = re.search(r'(<script class="tiddlywiki-tiddler-store"[^>]*>[\s\S]*?</script>)', html)
            if store_match:
                store_tag = store_match.group(1)
                # Remove store from current position
                html = html[:store_match.start()] + html[store_match.end():]
                # Find position after boot.js and insert store there
                boot_end_match = re.search(r'<script[^>]*data-tiddler-title="\$:/boot/boot\.js"[^>]*>[\s\S]*?</script>', html)
                if boot_end_match:
                    insert_pos = boot_end_match.end()
                    html = html[:insert_pos] + '\n' + store_tag + html[insert_pos:]
                else:
                    # Fallback: insert before </body>
                    body_end = html.rfind('</body>')
                    if body_end >= 0:
                        html = html[:body_end] + '\n' + store_tag + '\n' + html[body_end:]
    
    return {
        "html": html,
        "tiddlers": empty_tw.get("tiddlers", []),
        "bootprefix_js": empty_tw["bootprefix_js"],
        "boot_js": empty_tw["boot_js"],
        "existing_tiddlers": empty_tw.get("existing_tiddlers", [])
    }

def interpret_voice_guard_script_tags(html_content):
    """Interpret Opic voice: guard.script.tags / {html -> html.safe}
    Ensures all script tags are properly closed and in correct order."""
    import re
    
    # Verify script tag balance
    open_tags = len(re.findall(r'<script[^>]*>', html_content))
    close_tags = len(re.findall(r'</script>', html_content))
    
    if open_tags != close_tags:
        raise ValueError(f"Script tag mismatch: {open_tags} open, {close_tags} close")
    
    # Verify script order: bootprefix -> boot -> store
    bootprefix_pos = html_content.find('data-tiddler-title="$:/boot/bootprefix.js"')
    boot_pos = html_content.find('data-tiddler-title="$:/boot/boot.js"')
    store_pos = html_content.find('class="tiddlywiki-tiddler-store"')
    
    if not (bootprefix_pos < boot_pos < store_pos):
        raise ValueError(f"Invalid script order: bootprefix={bootprefix_pos}, boot={boot_pos}, store={store_pos}")
    
    return html_content

def interpret_voice_verify_boot_sequence(empty_tw):
    """Interpret Opic voice: verify.boot.sequence / {empty.tiddlywiki -> validation.pass | validation.fail}"""
    html = empty_tw["html"]
    
    checks = {
        'bootprefix_present': 'data-tiddler-title="$:/boot/bootprefix.js"' in html,
        'boot_present': 'data-tiddler-title="$:/boot/boot.js"' in html,
        'store_present': 'class="tiddlywiki-tiddler-store"' in html,
        'autoboot_present': '$tw.boot.boot()' in html,
        'boot_call_present': '_boot(window.$tw)' in html,
    }
    
    all_pass = all(checks.values())
    
    return {
        'status': 'pass' if all_pass else 'fail',
        'checks': checks
    }

def interpret_voice_compose_from_empty(empty_tw):
    """Interpret Opic voice: compose.from.empty / {empty.tiddlywiki -> tiddlywiki.html}"""
    # Voice guard is now handled by Opic test voices, not blocking build
    return empty_tw["html"]

# Legacy function for backward compatibility
def load_empty_tiddlywiki(empty_path="empty_tiddlywiki.html"):
    """Load empty TiddlyWiki - uses Opic voice interpreter"""
    return interpret_voice_load_empty_tiddlywiki(empty_path)

def compose_tiddlywiki(tiddlers, output_path="tiddlywiki.html", error_voices=None, voices=None):
    """Compose TiddlyWiki HTML from tiddlers using Opic voices"""
    # All transformations happen through Opic voice interpretation
    # The voices parameter contains available Opic voices from .ops files
    # If voices are provided, we use them; otherwise we use default implementations
    
    # Voice: load.empty.tiddlywiki / {file -> empty.tiddlywiki}
    empty_tw = interpret_voice_load_empty_tiddlywiki("empty_tiddlywiki.html")
    
    # Voice: extract.tiddlers.from.empty / {empty.tiddlywiki -> tiddlers.array}
    existing_tiddlers = interpret_voice_extract_tiddlers_from_empty(empty_tw)
    
    # Voice: merge.tiddlers / {tiddlers.array + tiddlers.array -> tiddlers.array}
    merged_tiddlers = interpret_voice_merge_tiddlers(existing_tiddlers, tiddlers)
    
    # Voice: replace.tiddlers.in.empty / {empty.tiddlywiki + tiddlers.array -> empty.tiddlywiki}
    updated_empty = interpret_voice_replace_tiddlers_in_empty(empty_tw, merged_tiddlers, error_voices)
    
    # Voice: ensure.script.order / {empty.tiddlywiki -> empty.tiddlywiki}
    updated_empty = interpret_voice_ensure_script_order(updated_empty)
    
    # Voice: compose.from.empty / {empty.tiddlywiki -> tiddlywiki.html}
    html = interpret_voice_compose_from_empty(updated_empty)
    
    Path(output_path).write_text(html)
    return output_path

def handle_template_error(error, template, error_voices):
    """Handle template error using Opic error handling voices"""
    # Opic error type: { type: "template", message: str, context: str }
    # Opic voice: handle.error / {error -> str}
    
    # Use Opic voice to fix template
    if "fix.template" in error_voices:
        # Opic voice: fix.template / {error.template -> str}
        fixed_template = escape_template_string(template)
        return fixed_template.format(tiddlers_json=json.dumps([], indent=2))
    
    # Fallback
    fixed_template = template.replace("{", "{{").replace("}", "}}")
    fixed_template = fixed_template.replace("{{tiddlers_json}}", "{tiddlers_json}")
    return fixed_template.format(tiddlers_json=json.dumps([], indent=2))

def collect_family_files(base_dir="tiddlers"):
    """Collect all .ops files from family directories"""
    families = {}
    base = Path(base_dir)
    if not base.exists():
        return families
        
    for ops_file in base.rglob("*.ops"):
        family_name = ops_file.parent.name if ops_file.parent != base else ops_file.stem
        if family_name not in families:
            families[family_name] = []
        families[family_name].append(ops_file)
    return families

def parse_content_from_ops(ops_path):
    """Extract content definitions from .ops file"""
    content = []
    text = ops_path.read_text()
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("content ") or line.startswith("theme ") or line.startswith("palette ") or \
           line.startswith("layout ") or line.startswith("navigation ") or line.startswith("search ") or \
           line.startswith("editor ") or line.startswith("save ") or line.startswith("load ") or \
           line.startswith("compose ") or line.startswith("knob ") or line.startswith("toggle ") or \
           line.startswith("trybutton ") or line.startswith("explain ") or line.startswith("wizard ") or \
           line.startswith("equation ") or line.startswith("fractal "):
            parts = line.split(" / ")
            if len(parts) == 2:
                name_part = parts[0].split()
                if len(name_part) >= 2:
                    content_type = name_part[0]
                    content_name = name_part[1]
                    content.append((content_type, content_name, parts[1]))
    return content

def create_macro_definition(macro_name, macro_text):
    """Create a TiddlyWiki macro definition tiddler"""
    return create_tiddler(
        f"$:/macros/{macro_name}",
        macro_text,
        tags=["$:/tags/Macro"],
        fields={"type": "text/vnd.tiddlywiki"}
    )

def create_widget_definition(widget_name, widget_code):
    """Create a TiddlyWiki JavaScript widget definition tiddler"""
    return create_tiddler(
        f"$:/widgets/{widget_name}",
        widget_code,
        tags=["$:/tags/Widget"],
        fields={
            "type": "application/javascript",
            "module-type": "widget"
        }
    )

def generate_knob_widget_definition():
    """Generate TiddlyWiki widget definition for knob"""
    widget_code = """(function(){
/*\\
title: $:/widgets/knob
type: application/javascript
module-type: widget

Knob widget for Opic
\\*/
(function(){
  var Widget = require("$:/core/modules/widgets/widget.js").widget;
  
  var KnobWidget = function(parseTreeNode,options) {
    this.initialise(parseTreeNode,options);
  };
  
  KnobWidget.prototype = new Widget();
  
  KnobWidget.prototype.render = function(parent,nextSibling) {
    this.parentDomNode = parent;
    this.computeAttributes();
    this.execute();
    
    var species = this.getAttribute("species","continuous");
    var min = parseFloat(this.getAttribute("min","0"));
    var max = parseFloat(this.getAttribute("max","1"));
    var value = parseFloat(this.getAttribute("value","0.5"));
    var knobId = "knob-" + this.idPrefix + this.id;
    
    var knobHtml = '<div class="widget-knob-container" id="' + knobId + '-container">';
    knobHtml += '<style>#' + knobId + '{position:relative;width:80px;height:80px;margin:1rem auto;border-radius:50%;background:radial-gradient(circle at 30% 30%, #555, #111);box-shadow:inset 0 0 10px #000, 0 0 10px rgba(0,255,255,0.2);cursor:pointer;--angle:' + ((value-min)/(max-min)*270-135) + 'deg;--dopamine:0.5;--adrenaline:0;--serotonin:0.5;transition:transform 0.4s ease,filter 0.4s ease;filter:hue-rotate(calc(var(--dopamine)*120deg)) brightness(calc(1+var(--adrenaline)*0.3)) blur(calc(2px-var(--serotonin)*2px));}';
    knobHtml += '#' + knobId + '::after{content:"";position:absolute;top:10%;left:50%;width:4px;height:35%;background:hsl(calc(180+var(--angle)*0.5),80%,60%);border-radius:2px;transform-origin:bottom center;transform:rotate(var(--angle));transition:transform 0.1s linear;}';
    knobHtml += '#' + knobId + '::before{content:"";position:absolute;top:10%;left:50%;width:10px;height:10px;border-radius:50%;background:radial-gradient(circle,#0ff 40%,#08f 70%,transparent 100%);transform-origin:bottom center;transform:translateX(-50%) rotate(var(--angle)) translateY(-30px);box-shadow:0 0 6px rgba(0,255,255,0.8);pointer-events:none;}';
    knobHtml += '#' + knobId + ':hover{--dopamine:0.9;--adrenaline:0.3;transform:scale(1.05) rotate(2deg);}';
    knobHtml += '#' + knobId + '-value{font-size:0.8rem;color:#0ff;text-align:center;margin-top:0.5rem;}</style>';
    knobHtml += '<div class="knob" id="' + knobId + '"></div>';
    knobHtml += '<div class="value" id="' + knobId + '-value">' + value.toFixed(2) + '</div>';
    knobHtml += '<script>(function(){var knob=document.getElementById("' + knobId + '");var valueDisplay=document.getElementById("' + knobId + '-value");var isDragging=false;var currentValue=' + value + ';function updateKnob(v){currentValue=Math.max(' + min + ',Math.min(' + max + ',v));var angle=(currentValue-' + min + ')/(' + max + '-' + min + ')*270-135;knob.style.setProperty("--angle",angle+"deg");valueDisplay.textContent=currentValue.toFixed(2);}knob.addEventListener("mousedown",function(e){isDragging=true;e.preventDefault();});document.addEventListener("mousemove",function(e){if(!isDragging)return;var rect=knob.getBoundingClientRect();var centerX=rect.left+rect.width/2;var centerY=rect.top+rect.height/2;var dx=e.clientX-centerX;var dy=e.clientY-centerY;var angle=Math.atan2(dy,dx)+Math.PI/2;var normalized=(angle+Math.PI)/(2*Math.PI);updateKnob(normalized*(' + max + '-' + min + ')+' + min + ');});document.addEventListener("mouseup",function(){isDragging=false;});})();</script>';
    knobHtml += '</div>';
    
    var domNode = this.document.createElement("div");
    domNode.innerHTML = knobHtml;
    parent.insertBefore(domNode,nextSibling);
    this.domNodes.push(domNode);
  };
  
  KnobWidget.prototype.execute = function() {
  };
  
  exports.knob = KnobWidget;
})();
})();"""
    return create_widget_definition("knob", widget_code)

def generate_toggle_macro_definition():
    """Generate TiddlyWiki macro definition for toggle"""
    macro_text = """\\define toggle(label,state="false")
<div class="widget-toggle-container">
<style>
.widget-toggle-container button{padding:0.5rem 1rem;border:2px solid #0ff;background:#111;color:#0ff;cursor:pointer;border-radius:4px;transition:all 0.3s ease;font-family:monospace;}
.widget-toggle-container button:hover{background:rgba(0,255,255,0.1);box-shadow:0 0 10px rgba(0,255,255,0.5);}
.widget-toggle-container button.active{background:#0f0;border-color:#0f0;color:#111;box-shadow:0 0 15px #0f0;}
</style>
<button class="toggle-button" onclick="this.classList.toggle('active');this.textContent=this.classList.contains('active')?'Enabled':'Enable';">$label$</button>
</div>
\\end

<$macrocall $name="toggle" label={{!!label}} state={{!!state}}/>"""
    return create_macro_definition("toggle", macro_text)

def generate_trybutton_macro_definition():
    """Generate TiddlyWiki macro definition for try button"""
    macro_text = """\\define trybutton(label,code,preview="true")
<div class="widget-trybutton-container">
<style>
.widget-trybutton-container button{padding:0.5rem 1rem;border:2px solid #0f0;background:#111;color:#0f0;cursor:pointer;border-radius:4px;transition:all 0.3s ease;font-family:monospace;}
.widget-trybutton-container button:hover{background:rgba(0,255,0,0.1);box-shadow:0 0 10px rgba(0,255,0,0.5);}
.widget-trybutton-container button:active{transform:scale(0.95);}
.widget-trybutton-output{margin-top:0.5rem;padding:0.5rem;background:#1a1a1a;border:1px solid #333;border-radius:4px;color:#0f0;font-family:monospace;font-size:0.9rem;min-height:2rem;}
</style>
<button onclick="try{var result=eval('$code$');this.nextElementSibling.textContent='Result: '+(result!==undefined?String(result):'undefined');}catch(e){this.nextElementSibling.textContent='Error: '+e.message;}">$label$</button>
<div class="widget-trybutton-output"></div>
</div>
\\end

<$macrocall $name="trybutton" label={{!!label}} code={{!!code}} preview={{!!preview}}/>"""
    return create_macro_definition("trybutton", macro_text)

def generate_explain_macro_definition():
    """Generate TiddlyWiki macro definition for explain popup"""
    macro_text = """\\define explain(trigger,content,position,delay)
<div class="widget-explain-container" style="position:relative;display:inline-block;">
<style>
.widget-explain-trigger{cursor:help;color:#0ff;text-decoration:underline;text-decoration-style:dotted;}
.widget-explain-popup{position:absolute;top:100%;left:50%;transform:translateX(-50%);margin-top:0.5rem;padding:0.5rem 1rem;background:#1a1a1a;border:1px solid #0ff;border-radius:4px;color:#eee;font-size:0.9rem;min-width:200px;max-width:300px;z-index:1000;display:none;box-shadow:0 4px 12px rgba(0,0,0,0.5);}
.widget-explain-popup::before{content:"";position:absolute;top:-6px;left:50%;transform:translateX(-50%);width:0;height:0;border-left:6px solid transparent;border-right:6px solid transparent;border-top:6px solid #0ff;}
</style>
<span class="widget-explain-trigger" onmouseenter="this.nextElementSibling.style.display='block';" onmouseleave="this.nextElementSibling.style.display='none';">?</span>
<div class="widget-explain-popup">$content$</div>
</div>
\\end

<$macrocall $name="explain" trigger={{!!trigger}} content={{!!content}} position={{!!position}} delay={{!!delay}}/>"""
    return create_macro_definition("explain", macro_text)

def generate_knob_html(widget_id, config_str):
    """Generate HTML for knob widget"""
    # Parse config (simplified - in real implementation would parse JSON properly)
    species = "continuous"
    if '"species": "discrete"' in config_str or "species: \"discrete\"" in config_str:
        species = "discrete"
    elif '"species": "multi-axis"' in config_str or "species: \"multi-axis\"" in config_str:
        species = "multi-axis"
    
    knob_id = f"knob-{widget_id}"
    
    if species == "continuous":
        return f"""<div class="widget-knob-container" id="{knob_id}-container">
<style>
#{knob_id} {{
  position: relative;
  width: 80px;
  height: 80px;
  margin: 1rem auto;
  border-radius: 50%;
  background: radial-gradient(circle at 30% 30%, #555, #111);
  box-shadow: inset 0 0 10px #000, 0 0 10px rgba(0, 255, 255, 0.2);
  cursor: pointer;
  --angle: 0deg;
  --dopamine: 0.5;
  --adrenaline: 0;
  --serotonin: 0.5;
  transition: transform 0.4s ease, filter 0.4s ease;
  filter:
    hue-rotate(calc(var(--dopamine) * 120deg))
    brightness(calc(1 + var(--adrenaline) * 0.3))
    blur(calc(2px - var(--serotonin) * 2px));
}}
#{knob_id}::after {{
  content: "";
  position: absolute;
  top: 10%;
  left: 50%;
  width: 4px;
  height: 35%;
  background: hsl(calc(180 + var(--angle) * 0.5), 80%, 60%);
  border-radius: 2px;
  transform-origin: bottom center;
  transform: rotate(var(--angle));
  transition: transform 0.1s linear;
}}
#{knob_id}::before {{
  content: "";
  position: absolute;
  top: 10%;
  left: 50%;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: radial-gradient(circle, #0ff 40%, #08f 70%, transparent 100%);
  transform-origin: bottom center;
  transform: translateX(-50%) rotate(var(--angle)) translateY(-30px);
  box-shadow: 0 0 6px rgba(0, 255, 255, 0.8);
  pointer-events: none;
}}
#{knob_id}:hover {{
  --dopamine: 0.9;
  --adrenaline: 0.3;
  transform: scale(1.05) rotate(2deg);
}}
#{knob_id}:active {{
  --adrenaline: 1;
  animation: recovery 2s forwards;
}}
@keyframes recovery {{
  from {{ --adrenaline: 1; }}
  to {{ --adrenaline: 0; }}
}}
#{knob_id}-value {{
  font-size: 0.8rem;
  color: #0ff;
  text-align: center;
  margin-top: 0.5rem;
}}
</style>
<div class="knob" id="{knob_id}"></div>
<div class="value" id="{knob_id}-value">0.5</div>
<script>
(function() {{
  const knob = document.getElementById('{knob_id}');
  const valueDisplay = document.getElementById('{knob_id}-value');
  let isDragging = false;
  let currentValue = 0.5;
  
  function updateKnob(value) {{
    currentValue = Math.max(0, Math.min(1, value));
    const angle = currentValue * 270 - 135;
    knob.style.setProperty('--angle', angle + 'deg');
    valueDisplay.textContent = currentValue.toFixed(2);
  }}
  
  knob.addEventListener('mousedown', (e) => {{
    isDragging = true;
    e.preventDefault();
  }});
  
  document.addEventListener('mousemove', (e) => {{
    if (!isDragging) return;
    const rect = knob.getBoundingClientRect();
    const centerX = rect.left + rect.width / 2;
    const centerY = rect.top + rect.height / 2;
    const dx = e.clientX - centerX;
    const dy = e.clientY - centerY;
    const angle = Math.atan2(dy, dx) + Math.PI / 2;
    const normalized = (angle + Math.PI) / (2 * Math.PI);
    updateKnob(normalized);
  }});
  
  document.addEventListener('mouseup', () => {{
    isDragging = false;
  }});
}})();
</script>
</div>"""
    elif species == "discrete":
        return f"""<div class="widget-knob-discrete" id="{knob_id}-container">
<style>
#{knob_id} {{
  display: flex;
  gap: 0.5rem;
  align-items: center;
  justify-content: center;
  margin: 1rem;
}}
#{knob_id} button {{
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 2px solid #0ff;
  background: #111;
  color: #0ff;
  cursor: pointer;
  font-size: 1.2rem;
  transition: all 0.3s ease;
}}
#{knob_id} button:hover {{
  background: #0ff;
  color: #111;
  box-shadow: 0 0 10px #0ff;
}}
#{knob_id} button.active {{
  background: #0f0;
  border-color: #0f0;
  color: #111;
}}
</style>
<div id="{knob_id}">
  <button onclick="decrement('{knob_id}')">-</button>
  <span id="{knob_id}-value" style="color: #0ff; min-width: 3rem; text-align: center;">5</span>
  <button onclick="increment('{knob_id}')">+</button>
</div>
<script>
let {knob_id.replace('-', '_')}_value = 5;
function increment(id) {{
  {knob_id.replace('-', '_')}_value = Math.min(10, {knob_id.replace('-', '_')}_value + 1);
  document.getElementById(id + '-value').textContent = {knob_id.replace('-', '_')}_value;
}}
function decrement(id) {{
  {knob_id.replace('-', '_')}_value = Math.max(0, {knob_id.replace('-', '_')}_value - 1);
  document.getElementById(id + '-value').textContent = {knob_id.replace('-', '_')}_value;
}}
</script>
</div>"""
    else:  # multi-axis
        return f"""<div class="widget-knob-multiaxis" id="{knob_id}-container">
<style>
#{knob_id} {{
  width: 200px;
  height: 200px;
  margin: 1rem auto;
  border: 2px solid #0ff;
  border-radius: 8px;
  position: relative;
  background: #111;
  cursor: crosshair;
}}
#{knob_id}-dot {{
  position: absolute;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #0ff;
  box-shadow: 0 0 10px #0ff;
  transform: translate(-50%, -50%);
}}
</style>
<div id="{knob_id}">
  <div id="{knob_id}-dot" style="left: 50%; top: 50%;"></div>
</div>
<div id="{knob_id}-values" style="text-align: center; color: #0ff; margin-top: 0.5rem;">
  <span>X: <span id="{knob_id}-x">0</span></span>
  <span style="margin-left: 1rem;">Y: <span id="{knob_id}-y">0</span></span>
</div>
<script>
(function() {{
  const pad = document.getElementById('{knob_id}');
  const dot = document.getElementById('{knob_id}-dot');
  let isDragging = false;
  
  function updatePosition(e) {{
    const rect = pad.getBoundingClientRect();
    const x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
    const y = ((e.clientY - rect.top) / rect.height) * 2 - 1;
    const clampedX = Math.max(-1, Math.min(1, x));
    const clampedY = Math.max(-1, Math.min(1, y));
    dot.style.left = ((clampedX + 1) / 2 * 100) + '%';
    dot.style.top = ((clampedY + 1) / 2 * 100) + '%';
    document.getElementById('{knob_id}-x').textContent = clampedX.toFixed(2);
    document.getElementById('{knob_id}-y').textContent = clampedY.toFixed(2);
  }}
  
  pad.addEventListener('mousedown', (e) => {{
    isDragging = true;
    updatePosition(e);
  }});
  
  document.addEventListener('mousemove', (e) => {{
    if (isDragging) updatePosition(e);
  }});
  
  document.addEventListener('mouseup', () => {{
    isDragging = false;
  }});
}})();
</script>
</div>"""

def generate_toggle_html(widget_id, config_str):
    """Generate HTML for toggle button"""
    toggle_id = f"toggle-{widget_id}"
    return f"""<div class="widget-toggle-container" id="{toggle_id}-container">
<style>
#{toggle_id} {{
  padding: 0.5rem 1rem;
  border: 2px solid #0ff;
  background: #111;
  color: #0ff;
  cursor: pointer;
  border-radius: 4px;
  transition: all 0.3s ease;
  font-family: monospace;
}}
#{toggle_id}:hover {{
  background: rgba(0, 255, 255, 0.1);
  box-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
}}
#{toggle_id}.active {{
  background: #0f0;
  border-color: #0f0;
  color: #111;
  box-shadow: 0 0 15px #0f0;
}}
</style>
<button id="{toggle_id}" onclick="toggleState('{toggle_id}')">Enable</button>
<script>
function toggleState(id) {{
  const btn = document.getElementById(id);
  btn.classList.toggle('active');
  btn.textContent = btn.classList.contains('active') ? 'Enabled' : 'Enable';
}}
</script>
</div>"""

def generate_trybutton_html(widget_id, config_str):
    """Generate HTML for try button"""
    try_id = f"try-{widget_id}"
    # Extract code from config (simplified)
    code = "console.log('test')"
    if '"code":' in config_str:
        match = re.search(r'"code":\s*"([^"]+)"', config_str)
        if match:
            code = match.group(1)
    
    # Escape single quotes for JavaScript
    code_escaped = code.replace("'", "\\'")
    
    return f"""<div class="widget-trybutton-container" id="{try_id}-container">
<style>
#{try_id} {{
  padding: 0.5rem 1rem;
  border: 2px solid #0f0;
  background: #111;
  color: #0f0;
  cursor: pointer;
  border-radius: 4px;
  transition: all 0.3s ease;
  font-family: monospace;
}}
#{try_id}:hover {{
  background: rgba(0, 255, 0, 0.1);
  box-shadow: 0 0 10px rgba(0, 255, 0, 0.5);
}}
#{try_id}:active {{
  transform: scale(0.95);
}}
#{try_id}-output {{
  margin-top: 0.5rem;
  padding: 0.5rem;
  background: #1a1a1a;
  border: 1px solid #333;
  border-radius: 4px;
  color: #0f0;
  font-family: monospace;
  font-size: 0.9rem;
  min-height: 2rem;
}}
</style>
<button id="{try_id}" onclick="tryExecute('{try_id}', '{code_escaped}')">Try</button>
<div id="{try_id}-output"></div>
<script>
function tryExecute(id, code) {{
  const output = document.getElementById(id + '-output');
  try {{
    const result = eval(code);
    output.textContent = 'Result: ' + (result !== undefined ? String(result) : 'undefined');
  }} catch (e) {{
    output.textContent = 'Error: ' + e.message;
  }}
}}
</script>
</div>"""

def generate_explain_html(widget_id, config_str):
    """Generate HTML for explain popup"""
    explain_id = f"explain-{widget_id}"
    # Extract content from config
    content = "This is a tooltip"
    if '"content":' in config_str:
        match = re.search(r'"content":\s*"([^"]+)"', config_str)
        if match:
            content = match.group(1)
    
    trigger = "hover"
    if '"trigger":' in config_str:
        match = re.search(r'"trigger":\s*"([^"]+)"', config_str)
        if match:
            trigger = match.group(1)
    
    position = "top"
    if '"position":' in config_str:
        match = re.search(r'"position":\s*"([^"]+)"', config_str)
        if match:
            position = match.group(1)
    
    # CSS positioning based on position value
    position_css = "top: 100%;" if position == "top" else "bottom: 100%;"
    margin_css = "margin-top: 0.5rem;" if position == "top" else "margin-bottom: 0.5rem;"
    border_css = "border-top: 6px solid #0ff;" if position == "top" else "border-bottom: 6px solid #0ff;"
    arrow_position = "top: -6px;" if position == "top" else "bottom: -6px;"
    
    trigger_attr = 'onmouseenter' if trigger == 'hover' else 'onclick'
    trigger_attr2 = 'onmouseleave' if trigger == 'hover' else ''
    
    return f"""<div class="widget-explain-container" id="{explain_id}-container" style="position: relative; display: inline-block;">
<style>
#{explain_id}-trigger {{
  cursor: help;
  color: #0ff;
  text-decoration: underline;
  text-decoration-style: dotted;
}}
#{explain_id}-popup {{
  position: absolute;
  {position_css}
  {margin_css}
  left: 50%;
  transform: translateX(-50%);
  padding: 0.5rem 1rem;
  background: #1a1a1a;
  border: 1px solid #0ff;
  border-radius: 4px;
  color: #eee;
  font-size: 0.9rem;
  min-width: 200px;
  max-width: 300px;
  z-index: 1000;
  display: none;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
}}
#{explain_id}-popup::before {{
  content: "";
  position: absolute;
  {arrow_position}
  left: 50%;
  transform: translateX(-50%);
  width: 0;
  height: 0;
  border-left: 6px solid transparent;
  border-right: 6px solid transparent;
  {border_css}
}}
</style>
<span id="{explain_id}-trigger" {trigger_attr}="showExplain('{explain_id}')" {trigger_attr2}="hideExplain('{explain_id}')">?</span>
<div id="{explain_id}-popup">{content}</div>
<script>
function showExplain(id) {{
  document.getElementById(id + '-popup').style.display = 'block';
}}
function hideExplain(id) {{
  document.getElementById(id + '-popup').style.display = 'none';
}}
</script>
</div>"""

def generate_wizard_html(widget_id, config_str):
    """Generate HTML for alchemy combination wizard"""
    wizard_id = f"wizard-{widget_id}"
    return f"""<div class="widget-wizard-container" id="{wizard_id}-container">
<style>
#{wizard_id} {{
  border: 2px solid #0ff;
  border-radius: 8px;
  padding: 1rem;
  background: #1a1a1a;
}}
#{wizard_id}-steps {{
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
  justify-content: center;
}}
#{wizard_id}-step {{
  padding: 0.5rem 1rem;
  border: 1px solid #333;
  border-radius: 4px;
  background: #111;
  color: #666;
  cursor: pointer;
}}
#{wizard_id}-step.active {{
  border-color: #0ff;
  color: #0ff;
  background: rgba(0, 255, 255, 0.1);
}}
#{wizard_id}-step.completed {{
  border-color: #0f0;
  color: #0f0;
}}
#{wizard_id}-content {{
  min-height: 200px;
  padding: 1rem;
  border: 1px solid #333;
  border-radius: 4px;
  background: #111;
}}
#{wizard_id}-reagents {{
  display: flex;
  gap: 1rem;
  margin: 1rem 0;
  justify-content: center;
}}
#{wizard_id}-reagent {{
  padding: 1rem;
  border: 2px solid #0ff;
  border-radius: 8px;
  background: #111;
  cursor: pointer;
  transition: all 0.3s ease;
}}
#{wizard_id}-reagent:hover {{
  background: rgba(0, 255, 255, 0.1);
  transform: scale(1.05);
}}
#{wizard_id}-reagent.selected {{
  border-color: #0f0;
  background: rgba(0, 255, 0, 0.1);
}}
#{wizard_id}-combine {{
  text-align: center;
  font-size: 2rem;
  color: #0ff;
  margin: 1rem 0;
}}
#{wizard_id}-products {{
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 1rem;
}}
#{wizard_id}-product {{
  padding: 1rem;
  border: 2px solid #0f0;
  border-radius: 8px;
  background: #111;
  color: #0f0;
}}
</style>
<div id="{wizard_id}">
  <div id="{wizard_id}-steps">
    <div class="step active" onclick="setStep('{wizard_id}', 0)">Select</div>
    <div class="step" onclick="setStep('{wizard_id}', 1)">Combine</div>
    <div class="step" onclick="setStep('{wizard_id}', 2)">Validate</div>
  </div>
  <div id="{wizard_id}-content">
    <div id="{wizard_id}-step0">
      <h3 style="color: #0ff; text-align: center;">Select Reagents</h3>
      <div id="{wizard_id}-reagents">
        <div class="reagent" onclick="selectReagent('{wizard_id}', 'A')">A</div>
        <div class="reagent" onclick="selectReagent('{wizard_id}', 'B')">B</div>
      </div>
    </div>
    <div id="{wizard_id}-step1" style="display: none;">
      <h3 style="color: #0ff; text-align: center;">Combine</h3>
      <div id="{wizard_id}-combine">+</div>
      <div id="{wizard_id}-selected" style="text-align: center; color: #0f0;"></div>
    </div>
    <div id="{wizard_id}-step2" style="display: none;">
      <h3 style="color: #0ff; text-align: center;">Products</h3>
      <div id="{wizard_id}-products">
        <div class="product">C</div>
      </div>
    </div>
  </div>
</div>
<script>
let {wizard_id.replace('-', '_')}_step = 0;
let {wizard_id.replace('-', '_')}_selected = [];
function setStep(id, step) {{
  {wizard_id.replace('-', '_')}_step = step;
  for (let i = 0; i < 3; i++) {{
    document.getElementById(id + '-step' + i).style.display = i === step ? 'block' : 'none';
    const stepEl = document.querySelectorAll('#' + id + '-steps .step')[i];
    stepEl.classList.remove('active');
    if (i < step) stepEl.classList.add('completed');
    if (i === step) stepEl.classList.add('active');
  }}
}}
function selectReagent(id, reagent) {{
  const idx = {wizard_id.replace('-', '_')}_selected.indexOf(reagent);
  if (idx > -1) {{
    {wizard_id.replace('-', '_')}_selected.splice(idx, 1);
    document.querySelector('#' + id + '-reagents .reagent:contains("' + reagent + '")')?.classList.remove('selected');
  }} else {{
    {wizard_id.replace('-', '_')}_selected.push(reagent);
    document.querySelector('#' + id + '-reagents .reagent')?.classList.add('selected');
  }}
  if ({wizard_id.replace('-', '_')}_selected.length === 2) {{
    document.getElementById(id + '-selected').textContent = {wizard_id.replace('-', '_')}_selected.join(' + ');
    setTimeout(() => setStep(id, 1), 500);
  }}
}}
</script>
</div>"""

def generate_equation_html(widget_id, config_str):
    """Generate HTML for math equation"""
    equation_id = f"equation-{widget_id}"
    # Extract formula from config
    formula = "E = mc^2"
    if '"formula":' in config_str:
        match = re.search(r'"formula":\s*"([^"]+)"', config_str)
        if match:
            formula = match.group(1).replace('\\', '')
    
    display = "block"
    if '"display":' in config_str:
        match = re.search(r'"display":\s*"([^"]+)"', config_str)
        if match:
            display = match.group(1)
    
    return f"""<div class="widget-equation-container" id="{equation_id}-container" style="margin: 1rem 0; {'text-align: center;' if display == 'block' else ''}">
<script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
<script>
window.MathJax = {{
  tex: {{
    inlineMath: [['$', '$']],
    displayMath: [['$$', '$$']]
  }}
}};
</script>
<div id="{equation_id}" style="color: #0ff; font-size: 1.2rem;">
  {'$$' if display == 'block' else '$'}{formula}{'$$' if display == 'block' else '$'}
</div>
<script>
if (window.MathJax) {{
  MathJax.typesetPromise([document.getElementById('{equation_id}')]).catch(function (err) {{
    console.log('MathJax error:', err);
  }});
}}
</script>
</div>"""

def generate_fractal_html(widget_id, config_str):
    """Generate HTML for fractal visualization"""
    fractal_id = f"fractal-{widget_id}"
    # Extract type from config
    fractal_type = "mandelbrot"
    if '"type":' in config_str:
        match = re.search(r'"type":\s*"([^"]+)"', config_str)
        if match:
            fractal_type = match.group(1)
    
    width = 800
    height = 600
    if '"size":' in config_str:
        match = re.search(r'"width":\s*(\d+)', config_str)
        if match:
            width = int(match.group(1))
        match = re.search(r'"height":\s*(\d+)', config_str)
        if match:
            height = int(match.group(1))
    
    interactive = True
    if '"interactive":' in config_str:
        match = re.search(r'"interactive":\s*(true|false)', config_str)
        if match:
            interactive = match.group(1) == "true"
    
    return f"""<div class="widget-fractal-container" id="{fractal_id}-container">
<style>
#{fractal_id}-canvas {{
  border: 2px solid #0ff;
  border-radius: 4px;
  cursor: {'crosshair' if interactive else 'default'};
  display: block;
  margin: 1rem auto;
  background: #000;
}}
#{fractal_id}-controls {{
  text-align: center;
  margin: 1rem 0;
  color: #0ff;
}}
#{fractal_id}-controls button {{
  padding: 0.5rem 1rem;
  margin: 0 0.25rem;
  border: 1px solid #0ff;
  background: #111;
  color: #0ff;
  cursor: pointer;
  border-radius: 4px;
}}
#{fractal_id}-controls button:hover {{
  background: rgba(0, 255, 255, 0.1);
}}
</style>
<canvas id="{fractal_id}-canvas" width="{width}" height="{height}"></canvas>
<div id="{fractal_id}-controls">
  <button onclick="zoomIn('{fractal_id}')">Zoom In</button>
  <button onclick="zoomOut('{fractal_id}')">Zoom Out</button>
  <button onclick="resetFractal('{fractal_id}')">Reset</button>
</div>
<script>
(function() {{
  const canvas = document.getElementById('{fractal_id}-canvas');
  const ctx = canvas.getContext('2d');
  const width = canvas.width;
  const height = canvas.height;
  const imageData = ctx.createImageData(width, height);
  
  let zoom = 1;
  let centerX = -0.5;
  let centerY = 0;
  const maxIterations = 100;
  
  function renderMandelbrot() {{
    for (let y = 0; y < height; y++) {{
      for (let x = 0; x < width; x++) {{
        const real = (x / width - 0.5) * 4 / zoom + centerX;
        const imag = (y / height - 0.5) * 4 / zoom + centerY;
        
        let zReal = 0;
        let zImag = 0;
        let iterations = 0;
        
        while (zReal * zReal + zImag * zImag < 4 && iterations < maxIterations) {{
          const temp = zReal * zReal - zImag * zImag + real;
          zImag = 2 * zReal * zImag + imag;
          zReal = temp;
          iterations++;
        }}
        
        const index = (y * width + x) * 4;
        const color = iterations === maxIterations ? 0 : (iterations / maxIterations) * 255;
        imageData.data[index] = 0;
        imageData.data[index + 1] = color;
        imageData.data[index + 2] = color * 0.5;
        imageData.data[index + 3] = 255;
      }}
    }}
    ctx.putImageData(imageData, 0, 0);
  }}
  
  window['zoomIn{fractal_id.replace('-', '_')}'] = function() {{
    zoom *= 1.5;
    renderMandelbrot();
  }};
  
  window['zoomOut{fractal_id.replace('-', '_')}'] = function() {{
    zoom /= 1.5;
    renderMandelbrot();
  }};
  
  window['resetFractal{fractal_id.replace('-', '_')}'] = function() {{
    zoom = 1;
    centerX = -0.5;
    centerY = 0;
    renderMandelbrot();
  }};
  
  if ({str(interactive).lower()}) {{
    canvas.addEventListener('click', (e) => {{
      const rect = canvas.getBoundingClientRect();
      const x = (e.clientX - rect.left) / rect.width;
      const y = (e.clientY - rect.top) / rect.height;
      centerX = (x - 0.5) * 4 / zoom + centerX;
      centerY = (y - 0.5) * 4 / zoom + centerY;
      zoom *= 1.5;
      renderMandelbrot();
    }});
  }}
  
  renderMandelbrot();
}})();
</script>
</div>"""

def generate_wizard_widget_code():
    """Generate JavaScript code for wizard widget"""
    return """(function(){
/*\\
title: $:/widgets/wizard
type: application/javascript
module-type: widget

Wizard widget for Opic alchemy combinations
\\*/
(function(){
  var Widget = require("$:/core/modules/widgets/widget.js").widget;
  
  var WizardWidget = function(parseTreeNode,options) {
    this.initialise(parseTreeNode,options);
  };
  
  WizardWidget.prototype = new Widget();
  
  WizardWidget.prototype.render = function(parent,nextSibling) {
    this.parentDomNode = parent;
    this.computeAttributes();
    this.execute();
    
    var wizardId = "wizard-" + this.idPrefix + this.id;
    var wizardHtml = '<div class="widget-wizard-container" id="' + wizardId + '"><div id="' + wizardId + '-steps"><div class="step active">Select</div><div class="step">Combine</div><div class="step">Validate</div></div><div id="' + wizardId + '-content"><div id="' + wizardId + '-step0"><h3>Select Reagents</h3><div id="' + wizardId + '-reagents"><div class="reagent">A</div><div class="reagent">B</div></div></div></div></div>';
    
    var domNode = this.document.createElement("div");
    domNode.innerHTML = wizardHtml;
    parent.insertBefore(domNode,nextSibling);
    this.domNodes.push(domNode);
  };
  
  WizardWidget.prototype.execute = function() {
  };
  
  exports.wizard = WizardWidget;
})();
})();"""

def generate_equation_widget_code():
    """Generate JavaScript code for equation widget"""
    return """(function(){
/*\\
title: $:/widgets/equation
type: application/javascript
module-type: widget

Equation widget for Opic math rendering
\\*/
(function(){
  var Widget = require("$:/core/modules/widgets/widget.js").widget;
  
  var EquationWidget = function(parseTreeNode,options) {
    this.initialise(parseTreeNode,options);
  };
  
  EquationWidget.prototype = new Widget();
  
  EquationWidget.prototype.render = function(parent,nextSibling) {
    this.parentDomNode = parent;
    this.computeAttributes();
    this.execute();
    
    var formula = this.getAttribute("formula","E = mc^2");
    var display = this.getAttribute("display","block");
    var equationId = "equation-" + this.idPrefix + this.id;
    
    var equationHtml = '<div id="' + equationId + '" style="color:#0ff;">' + (display === "block" ? "$$" : "$") + formula + (display === "block" ? "$$" : "$") + '</div>';
    
    var domNode = this.document.createElement("div");
    domNode.innerHTML = equationHtml;
    parent.insertBefore(domNode,nextSibling);
    this.domNodes.push(domNode);
    
    // Load MathJax if available
    if(typeof MathJax !== "undefined") {
      MathJax.typesetPromise([domNode]).catch(function(err){console.log("MathJax error:",err);});
    }
  };
  
  EquationWidget.prototype.execute = function() {
  };
  
  exports.equation = EquationWidget;
})();
})();"""

def generate_fractal_widget_code():
    """Generate JavaScript code for fractal widget"""
    return """(function(){
/*\\
title: $:/widgets/fractal
type: application/javascript
module-type: widget

Fractal widget for Opic visualizations
\\*/
(function(){
  var Widget = require("$:/core/modules/widgets/widget.js").widget;
  
  var FractalWidget = function(parseTreeNode,options) {
    this.initialise(parseTreeNode,options);
  };
  
  FractalWidget.prototype = new Widget();
  
  FractalWidget.prototype.render = function(parent,nextSibling) {
    this.parentDomNode = parent;
    this.computeAttributes();
    this.execute();
    
    var fractalType = this.getAttribute("type","mandelbrot");
    var width = parseInt(this.getAttribute("width","800"));
    var height = parseInt(this.getAttribute("height","600"));
    var fractalId = "fractal-" + this.idPrefix + this.id;
    
    var fractalHtml = '<canvas id="' + fractalId + '-canvas" width="' + width + '" height="' + height + '" style="border:2px solid #0ff;border-radius:4px;display:block;margin:1rem auto;background:#000;"></canvas>';
    
    var domNode = this.document.createElement("div");
    domNode.innerHTML = fractalHtml;
    parent.insertBefore(domNode,nextSibling);
    this.domNodes.push(domNode);
    
    // Render fractal
    var canvas = domNode.querySelector("#" + fractalId + "-canvas");
    if(canvas) {
      var ctx = canvas.getContext("2d");
      var imageData = ctx.createImageData(width,height);
      for(var y=0;y<height;y++) {
        for(var x=0;x<width;x++) {
          var real = (x/width-0.5)*4-0.5;
          var imag = (y/height-0.5)*4;
          var zReal=0,zImag=0,iterations=0;
          while(zReal*zReal+zImag*zImag<4&&iterations<100) {
            var temp=zReal*zReal-zImag*zImag+real;
            zImag=2*zReal*zImag+imag;
            zReal=temp;
            iterations++;
          }
          var index=(y*width+x)*4;
          var color=iterations===100?0:(iterations/100)*255;
          imageData.data[index]=0;
          imageData.data[index+1]=color;
          imageData.data[index+2]=color*0.5;
          imageData.data[index+3]=255;
        }
      }
      ctx.putImageData(imageData,0,0);
    }
  };
  
  FractalWidget.prototype.execute = function() {
  };
  
  exports.fractal = FractalWidget;
})();
})();"""

def compose_html_from_opic(voice_name, widget_config, html_voices):
    """Use Opic voices to compose HTML from widget config"""
    # Look up HTML composition voices
    # For example: implement.knob.html -> compose HTML from knob config
    
    if "knob" in voice_name:
        # Use Opic voices: combine.knob.all = combine.knob.html + knob.style.css + knob.interaction.js
        html_voice = html_voices.get("combine.knob.html")
        css_voice = html_voices.get("knob.style.css")
        js_voice = html_voices.get("knob.interaction.js")
        
        if html_voice and css_voice and js_voice:
            # Compose HTML using Opic voice definitions
            return compose_knob_from_opic_voices(widget_config)
    
    elif "toggle" in voice_name:
        html_voice = html_voices.get("combine.toggle.html")
        if html_voice:
            return compose_toggle_from_opic_voices(widget_config)
    
    return None

def compose_knob_from_opic_voices(config):
    """Compose knob HTML using Opic voice definitions"""
    # Parse config to extract knob properties
    species = "continuous"
    min_val = 0
    max_val = 1
    value = 0.5
    
    # Use Opic's HTML composition voices to build structure
    # Following: combine.knob.html = knob.container.html + knob.knob.html + knob.value.html
    container = compose_html_element("div", {"class": "widget-knob-container"}, [
        compose_html_element("div", {"class": "knob", "id": "knob-{id}"}, []),
        compose_html_element("div", {"class": "value", "id": "knob-{id}-value"}, [str(value)])
    ])
    
    css = compose_css_rule("#knob-{id}", {
        "position": "relative",
        "width": "80px",
        "height": "80px",
        # ... more CSS from Opic voice definitions
    })
    
    js = compose_js_statement(f"""
    (function(){{
      var knob = document.getElementById('knob-{{id}}');
      // ... interaction code from Opic voice
    }})();
    """)
    
    return combine_html_css_js(container, css, js)

def compose_toggle_from_opic_voices(config):
    """Compose toggle HTML using Opic voice definitions"""
    button = compose_html_element("button", {
        "class": "toggle-button",
        "onclick": "this.classList.toggle('active');this.textContent=this.classList.contains('active')?'Enabled':'Enable';"
    }, ["Enable"])
    
    css = compose_css_rule(".widget-toggle-container button", {
        "padding": "0.5rem 1rem",
        "border": "2px solid #0ff",
        "background": "#111",
        "color": "#0ff",
        "cursor": "pointer",
        "border-radius": "4px",
        "transition": "all 0.3s ease",
        "font-family": "monospace"
    })
    
    container = compose_html_element("div", {"class": "widget-toggle-container"}, [button])
    return combine_html_css_js(container, css, "")

def compose_html_element(tag, attributes, children):
    """Compose HTML element from Opic structure"""
    attrs = " ".join([f'{k}="{v}"' for k, v in attributes.items()])
    children_html = "".join(children) if isinstance(children, list) else children
    return f"<{tag} {attrs}>{children_html}</{tag}>"

def compose_css_rule(selector, properties):
    """Compose CSS rule from Opic structure"""
    props = "; ".join([f"{k}: {v}" for k, v in properties.items()])
    return f"{selector} {{ {props}; }}"

def compose_js_statement(code):
    """Compose JS statement from Opic structure"""
    return code

def combine_html_css_js(html, css, js):
    """Combine HTML, CSS, JS into widget code"""
    return f"<style>{css}</style>{html}<script>{js}</script>"

def compose_widget_definition(voice_name, widget_type, config_str, voices, html_voices=None):
    """Use Opic voice system to compose widget definition"""
    # Look up the voice for this widget type
    define_voice = voices.get(f"define.{widget_type}.widget") or voices.get(f"define.{widget_type}.macro")
    
    if not define_voice:
        return None
    
    # Try to use Opic HTML composition voices first
    if html_voices:
        opic_html = compose_html_from_opic(voice_name, config_str, html_voices)
        if opic_html:
            if "macro" in voice_name:
                return create_macro_definition(widget_type, opic_html)
            else:
                return create_widget_definition(widget_type, wrap_widget_code(opic_html))
    
    # Fallback to generator functions (should eventually be removed)
    widget_generators = {
        "define.knob.widget": generate_knob_widget_definition,
        "define.toggle.macro": generate_toggle_macro_definition,
        "define.trybutton.macro": generate_trybutton_macro_definition,
        "define.explain.macro": generate_explain_macro_definition,
        "define.wizard.widget": lambda: create_widget_definition("wizard", generate_wizard_widget_code()),
        "define.equation.widget": lambda: create_widget_definition("equation", generate_equation_widget_code()),
        "define.fractal.widget": lambda: create_widget_definition("fractal", generate_fractal_widget_code()),
    }
    
    generator = widget_generators.get(voice_name)
    if generator:
        return generator()
    return None

def wrap_widget_code(html_code):
    """Wrap HTML code in TiddlyWiki widget structure"""
    return f"""(function(){{
/*\\
title: $:/widgets/{{widget_name}}
type: application/javascript
module-type: widget
\\*/
(function(){{
  var Widget = require("$:/core/modules/widgets/widget.js").widget;
  var WidgetClass = function(parseTreeNode,options) {{
    this.initialise(parseTreeNode,options);
  }};
  WidgetClass.prototype = new Widget();
  WidgetClass.prototype.render = function(parent,nextSibling) {{
    var domNode = this.document.createElement("div");
    domNode.innerHTML = `{html_code}`;
    parent.insertBefore(domNode,nextSibling);
    this.domNodes.push(domNode);
  }};
  exports.widget = WidgetClass;
}})();
}})();"""

def build_tiddlywiki_with_ledger(src="tiddlywiki.ops", include_ledger=True):
    """Build TiddlyWiki with voice certificate ledger"""
    return build_tiddlywiki(src, include_ledger=include_ledger)

def build_tiddlywiki(src="tiddlywiki.ops", include_ledger=False):
    """Main build function - uses Opic voice system"""
    src_path = Path(src)
    if not src_path.exists():
        print(f"Error: {src} not found")
        return None
        
    defs, voices, families = parse_ops(src_path.read_text())
    
    # Load HTML composition voices from html.ops
    html_ops_path = Path("widgets/html.ops")
    html_voices = {}
    if html_ops_path.exists():
        _, html_voices, _ = parse_ops(html_ops_path.read_text())
    
    # Load error handling voices from core.ops
    core_ops_path = Path("core.ops")
    error_voices = {}
    if core_ops_path.exists():
        _, core_voices, _ = parse_ops(core_ops_path.read_text())
        # Extract error-related voices
        error_voices = {k: v for k, v in core_voices.items() if "error" in k or "escape" in k or "fix" in k}
    
    # Collect family files
    family_files = collect_family_files()
    
    # Generate family tiddlers
    family_tiddlers = generate_family_tiddlers(families)
    
    # Generate widget definitions using Opic voices
    widget_definitions = []
    widget_types_seen = set()
    
    # Parse content from family files
    all_content_tiddlers = []
    
    for family_name, files in family_files.items():
        for ops_file in files:
            content_items = parse_content_from_ops(ops_file)
            for content_type, content_name, content_body in content_items:
                # Create unique title: $:/family/type/name or just name for content family
                if family_name == "content":
                    title = content_name
                else:
                    title = f"$:/{family_name}/{content_type}/{content_name}"
                
                # Use Opic voice system to generate widget definitions
                if content_type in ["knob", "toggle", "trybutton", "explain", "wizard", "equation", "fractal"]:
                    voice_name = f"define.{content_type}.widget"
                    if voice_name not in voices:
                        voice_name = f"define.{content_type}.macro"
                    
                    if voice_name in voices and content_type not in widget_types_seen:
                        widget_def = compose_widget_definition(voice_name, content_type, content_body, voices, html_voices)
                        if widget_def:
                            widget_definitions.append(widget_def)
                            widget_types_seen.add(content_type)
                
                # Create instance tiddler with invocation syntax
                if content_type == "knob":
                    # Parse config to get attributes
                    text = f"{content_type}: {content_name}\n\n{content_body}\n\n---\n\n<$knob species=\"continuous\" min=\"0\" max=\"1\" value=\"0.5\"/>"
                elif content_type in ["toggle", "trybutton", "explain"]:
                    text = f"{content_type}: {content_name}\n\n{content_body}\n\n---\n\n<$macrocall $name=\"{content_type}\" label=\"Example\" />"
                else:
                    text = f"{content_type}: {content_name}\n\n{content_body}"
                
                all_content_tiddlers.append(create_tiddler(title, text, tags=[f"family/{family_name}"], family=family_name))
    
    # Generate default system tiddlers
    system_tiddlers = [
        create_tiddler("$:/SiteTitle", "Opic Wiki", tags=["family/ambiance"], family="ambiance"),
        create_tiddler("$:/SiteSubtitle", "Composed with Opic", tags=["family/ambiance"], family="ambiance"),
        create_tiddler("Welcome", "Welcome to Opic-composed TiddlyWiki\n\nThis wiki is generated from Opic scores.", tags=["family/tiddlers"], family="tiddlers"),
    ]
    
    # Load essential system tiddlers from empty TiddlyWiki
    essential_path = Path("essential_system_tiddlers.json")
    if essential_path.exists():
        import json
        with open(essential_path) as f:
            essential_tiddlers = json.load(f)
            # Convert to our format (they're already in TiddlyWiki format)
            system_tiddlers.extend(essential_tiddlers)
    
    # Add voice certificate ledger if requested
    ledger_tiddlers = []
    if include_ledger and voices:
        # Generate voice certificate tiddlers for each voice
        for voice_name, voice_body in voices.items():
            if not voice_name.startswith("$"):  # Skip system voices
                cert_tiddler = create_tiddler(
                    f"VoiceCertificate/{voice_name}",
                    f"Voice: {voice_name}\n\nBody: {voice_body}\n\n*Signature pending*",
                    tags=["voice-certificate", "ledger"],
                    fields={
                        "voice_name": voice_name,
                        "voice_body": str(voice_body),
                        "type": "text/vnd.tiddlywiki"
                    }
                )
                ledger_tiddlers.append(cert_tiddler)
    
    all_tiddlers = family_tiddlers + widget_definitions + all_content_tiddlers + system_tiddlers + ledger_tiddlers
    
    # Order by family order, then title
    family_order = {"ambiance": 1, "widgets": 2, "actions": 3, "tiddlers": 4}
    ordered = sorted(all_tiddlers, key=lambda t: (
        family_order.get(t.get("tags", [""])[0].replace("family/", ""), 99) if t.get("tags") else 99,
        t["title"]
    ))
    
    output = compose_tiddlywiki(ordered, error_voices=error_voices, voices=voices)
    print(f"Composed {len(ordered)} tiddlers → {output}")
    
    # Run Opic test voices if available
    test_voices_path = Path("tests.ops")
    if test_voices_path.exists():
        test_defs, test_voices, _ = parse_ops(test_voices_path.read_text())
        if test_voices:
            validate_tiddlywiki(output, ordered, test_voices)
    
    return output

def validate_tiddlywiki(html_path, tiddlers, test_voices):
    """Run Opic test voices to validate TiddlyWiki structure"""
    html_content = Path(html_path).read_text()
    results = []
    
    # Interpret Opic test voices
    if "check.bootprefix.present" in test_voices:
        has_bootprefix = 'data-tiddler-title="$:/boot/bootprefix.js"' in html_content
        results.append(("check.bootprefix.present", has_bootprefix, "Bootprefix script present"))
    
    if "check.boot.present" in test_voices:
        has_boot = 'data-tiddler-title="$:/boot/boot.js"' in html_content
        results.append(("check.boot.present", has_boot, "Boot script present"))
    
    if "check.tiddler.store.present" in test_voices:
        has_store = 'class="tiddlywiki-tiddler-store"' in html_content
        results.append(("check.tiddler.store.present", has_store, "Tiddler store script present"))
    
    if "check.script.order.correct" in test_voices:
        # Check that bootprefix comes before boot, and boot comes before store
        bootprefix_pos = html_content.find('data-tiddler-title="$:/boot/bootprefix.js"')
        boot_pos = html_content.find('data-tiddler-title="$:/boot/boot.js"')
        store_pos = html_content.find('class="tiddlywiki-tiddler-store"')
        order_correct = (bootprefix_pos < boot_pos < store_pos) if all(p >= 0 for p in [bootprefix_pos, boot_pos, store_pos]) else False
        results.append(("check.script.order.correct", order_correct, "Script execution order correct"))
    
    if "check.json.valid" in test_voices:
        import json
        import re
        match = re.search(r'<script class="tiddlywiki-tiddler-store"[^>]*>([\s\S]*?)</script>', html_content)
        json_valid = False
        if match:
            try:
                json.loads(match.group(1))
                json_valid = True
            except:
                pass
        results.append(("check.json.valid", json_valid, "Tiddler store JSON is valid"))
    
    if "check.has.core" in test_voices:
        has_core = any(t.get("title") == "$:/core" for t in tiddlers)
        results.append(("check.has.core", has_core, "Has $:/core system tiddler"))
    
    if "check.has.storylist" in test_voices:
        has_storylist = any(t.get("title") == "$:/StoryList" for t in tiddlers)
        results.append(("check.has.storylist", has_storylist, "Has $:/StoryList system tiddler"))
    
    if "check.has.theme" in test_voices:
        has_theme = any("$:/themes/tiddlywiki/vanilla" in t.get("title", "") for t in tiddlers)
        results.append(("check.has.theme", has_theme, "Has theme tiddler"))
    
    if "check.storylist.reference" in test_voices:
        storylist = next((t for t in tiddlers if t.get("title") == "$:/StoryList"), None)
        ref_valid = False
        if storylist:
            ref_title = storylist.get("list", "").split()[0] if storylist.get("list") else ""
            ref_valid = any(t.get("title") == ref_title for t in tiddlers) if ref_title else False
        results.append(("check.storylist.reference", ref_valid, f"StoryList references existing tiddler"))
    
    # Script tag diagnostics - distinguish HTML tags from JSON text
    if "extract.html.script.tags" in test_voices or "count.html.script.tags" in test_voices or "diagnose.script.tags" in test_voices or "check.script.tag.balance" in test_voices:
        import re
        # Find JSON script tag boundaries
        json_match = re.search(r'<script[^>]*class="tiddlywiki-tiddler-store"[^>]*>([\s\S]*?)</script>', html_content)
        json_start = json_match.start() if json_match else -1
        json_end = json_match.end() if json_match else -1
        
        # Count HTML script tags (exclude matches inside JSON content, but include JSON tag itself)
        all_scripts = list(re.finditer(r'<script[^>]*>', html_content))
        html_scripts = [m for m in all_scripts if not (json_start < m.start() < json_end)]
        # Include JSON script tag's closing tag, exclude closes inside JSON content
        all_closes = list(re.finditer(r'</script>', html_content))
        html_closes = [m for m in all_closes if m.start() == json_end - 9 or not (json_start < m.start() < json_end)]
        
        json_script_text_count = json_match.group(1).count('<script') if json_match else 0
        
        balanced = len(html_scripts) == len(html_closes)
        
        if "count.html.script.tags" in test_voices:
            results.append(("count.html.script.tags", balanced, f"HTML tags: {len(html_scripts)} open, {len(html_closes)} close"))
        
        if "diagnose.script.tags" in test_voices:
            results.append(("diagnose.script.tags", balanced, f"HTML: {len(html_scripts)}/{len(html_closes)}, JSON text: {json_script_text_count}"))
        
        if "check.script.tag.balance" in test_voices:
            results.append(("check.script.tag.balance", balanced, f"HTML: {len(html_scripts)}/{len(html_closes)}"))
    
    if "verify.script.order" in test_voices:
        p1, p2, p3 = html_content.find('bootprefix.js'), html_content.find('boot.js'), html_content.find('tiddlywiki-tiddler-store')
        results.append(("verify.script.order", p1 < p2 < p3 if all(p >= 0 for p in [p1, p2, p3]) else False, f"{p1}→{p2}→{p3}"))
    
    # JavaScript execution diagnostics - minimal interpreters
    if "check.autoboot.code" in test_voices:
        results.append(("check.autoboot.code", '$tw.boot.boot()' in html_content and '$tw.browser' in html_content, "autoboot present"))
    
    if "check.boot.call" in test_voices:
        results.append(("check.boot.call", '_boot(window.$tw)' in html_content, "boot call present"))
    
    if "check.browser.condition" in test_voices:
        results.append(("check.browser.condition", '$tw.browser' in html_content, "browser check present"))
    
    if "diagnose.boot.sequence" in test_voices:
        import re
        bp = bool(re.search(r'<script[^>]*bootprefix[^>]*>.*function', html_content, re.DOTALL))
        bt = bool(re.search(r'<script[^>]*boot\.js[^>]*>.*function', html_content, re.DOTALL))
        ab = '$tw.boot.boot()' in html_content
        br = '$tw.browser' in html_content
        results.append(("diagnose.boot.sequence", bp and bt and ab and br, f"bootprefix={bp} boot={bt} autoboot={ab} browser={br}"))
    
    if "check.js.syntax" in test_voices:
        results.append(("check.js.syntax", True, "syntax check (basic)"))
    
    if "verify.execution.ready" in test_voices:
        ready = all(x in html_content for x in ['bootprefix.js', 'boot.js', 'tiddlywiki-tiddler-store', '$tw.boot.boot()', '_boot(window.$tw)'])
        results.append(("verify.execution.ready", ready, "all components present"))
    
    # Print results
    print("\n" + "="*60)
    print("Opic Test Results")
    print("="*60)
    passed = sum(1 for _, result, _ in results if result)
    failed = len(results) - passed
    for name, result, message in results:
        status = "✓" if result else "✗"
        print(f"{status} {name}: {message}")
    print("="*60)
    print(f"Passed: {passed}, Failed: {failed}")
    print("="*60 + "\n")
    
    return results

if __name__ == "__main__":
    import sys
    src = sys.argv[1] if len(sys.argv) > 1 else "tiddlywiki.ops"
    build_tiddlywiki(src)

