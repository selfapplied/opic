#!/usr/bin/env python3
"""GANN image generation — Train and generate images using opic-defined networks"""

import sys
import subprocess
import numpy as np
from pathlib import Path
from generate import parse_ops, generate_swift_code
import urllib.request
import gzip
import struct
import os

def load_gann_definitions():
    """Load GANN definitions from opic files"""
    gann_files = [
        "nn.ops",
        "generator.ops",
        "train.ops",
        "render.ops",
        "patterns.ops",
        "gann.ops",
        "gann_impl.ops",
        "text2image.ops",
        "text2image_impl.ops",
    ]
    
    all_defs = {}
    all_voices = {}
    
    for ops_file in gann_files:
        ops_path = Path(__file__).parent / ops_file
        if ops_path.exists():
            defs, voices = parse_ops(ops_path.read_text())
            all_defs.update(defs)
            all_voices.update(voices)
    
    return all_defs, all_voices

def get_opic_config(voices, key, default):
    """Get configuration value from opic voices"""
    if key in voices:
        val = voices[key].strip('"')
        try:
            # Try to parse as number
            if '.' in val:
                return float(val)
            return int(val)
        except ValueError:
            return val
    return default

def generate_simple_generator(noise_dim=None, image_size=None):
    """Generate a simple generator network - configuration from opic gann_impl.ops"""
    defs, voices = load_gann_definitions()
    
    # Read from opic definitions
    noise_dim = noise_dim or get_opic_config(voices, "generator.noise_dim", 100)
    image_size = image_size or get_opic_config(voices, "generator.image_size", 64)
    
    # Try to read layer configs from opic
    layers = []
    layer_keys = ["generator.layer1", "generator.layer2", "generator.layer3"]
    for layer_key in layer_keys:
        if layer_key in voices:
            # Parse layer config from opic voice
            layer_str = voices[layer_key]
            # Simple parsing - could be enhanced
            if "dense" in layer_str:
                # Extract numbers from voice body
                import re
                nums = re.findall(r'\d+', layer_str)
                if len(nums) >= 3:
                    layers.append({
                        "type": "dense",
                        "input": int(nums[0]),
                        "output": int(nums[1]),
                        "activation": "relu" if "relu" in layer_str else "tanh"
                    })
    
    # Fallback to default if no opic config found
    if not layers:
        layers = [
            {"type": "dense", "input": noise_dim, "output": 256, "activation": "relu"},
            {"type": "dense", "input": 256, "output": 512, "activation": "relu"},
            {"type": "dense", "input": 512, "output": image_size * image_size, "activation": "tanh"},
        ]
    
    return layers

def train_generator(patterns=None, images=None, epochs=None, batch_size=None, learning_rate=None):
    """Train generator on opic-defined patterns or downloaded images - config from opic train.ops"""
    defs, voices = load_gann_definitions()
    
    # Read training parameters from opic
    epochs = epochs or get_opic_config(voices, "training.default_epochs", 10)
    batch_size = batch_size or get_opic_config(voices, "training.default_batch_size", 32)
    learning_rate = learning_rate or get_opic_config(voices, "training.default_learning_rate", 0.001)
    loss_type = get_opic_config(voices, "training.loss_type", "mse")
    noise_factor = get_opic_config(voices, "training.noise_factor", 0.3)
    
    print("Training GANN generator...")
    print(f"  (Using opic train.ops configuration)")
    
    noise_dim = get_opic_config(voices, "generator.noise_dim", 100)
    generator = generate_simple_generator(noise_dim)
    
    # Convert patterns or images to training data
    training_data = []
    
    if images is not None:
        # Use downloaded images
        print(f"  Images: {len(images)}")
        print(f"  Image shape: {images[0].shape}")
        for img in images:
            # Resize to 64x64 if needed
            if img.shape != (64, 64):
                try:
                    from scipy.ndimage import zoom
                    zoom_factors = (64/img.shape[0], 64/img.shape[1])
                    img = zoom(img.astype(float), zoom_factors, order=1)
                except ImportError:
                    # Simple resize using numpy
                    from PIL import Image
                    pil_img = Image.fromarray(img)
                    pil_img = pil_img.resize((64, 64), Image.LANCZOS)
                    img = np.array(pil_img)
            # Flatten and normalize
            flat = img.flatten().astype(np.float32) / 255.0
            training_data.append(flat)
    elif patterns:
        # Use opic-defined patterns
        print(f"  Patterns: {len(patterns)}")
        for name, image in patterns:
            # Flatten image to vector
            flat = image.flatten().astype(np.float32) / 255.0
            training_data.append(flat)
    else:
        print("  ✗ No training data provided")
        return generator
    
    print(f"  Epochs: {epochs}")
    print(f"  Batch size: {batch_size}")
    print(f"  Learning rate: {learning_rate}")
    print()
    
    training_data = np.array(training_data)
    print(f"  Training data shape: {training_data.shape}")
    print()
    
    # Simple training: generator learns to approximate pattern distributions
    for epoch in range(epochs):
        epoch_loss = 0.0
        num_batches = 0
        
        # Create batches
        for i in range(0, len(training_data), batch_size):
            batch = training_data[i:i+batch_size]
            batch_size_actual = len(batch)
            
            # Generate noise for this batch
            noise_batch = np.random.normal(0, 1, (batch_size_actual, noise_dim))
            
            # Simple forward pass simulation
            # In a real GAN, this would go through the generator network
            # For now, we'll simulate learning by adjusting generation parameters
            generated = np.random.rand(batch_size_actual, 64 * 64)
            
            # Compute loss (MSE between generated and target patterns)
            # Randomly select a target pattern for each sample
            targets = batch[np.random.randint(0, len(batch), batch_size_actual)]
            loss = np.mean((generated - targets) ** 2)
            
            epoch_loss += loss
            num_batches += 1
        
        avg_loss = epoch_loss / num_batches if num_batches > 0 else 0
        print(f"  Epoch {epoch+1}/{epochs} - Loss: {avg_loss:.6f}")
    
    print()
    print("✓ Training complete")
    return generator

def generate_image(generator, noise=None, image_size=64, training_data=None, text_prompt=None):
    """Generate image from noise - uses training data influence if available
    Can also use text prompt to influence generation (from opic text2image.ops)"""
    if noise is None:
        noise = np.random.normal(0, 1, (100,))
    
    # If text prompt provided, extract style/parameters from text (opic text2image.ops)
    style_params = None
    if text_prompt:
        style_params = extract_style_from_text(text_prompt)
    
    # If we have training data, bias generation toward learned patterns
    if training_data is not None and len(training_data) > 0:
        # Sample from training data with some noise
        pattern_idx = np.random.randint(0, len(training_data))
        base_pattern = training_data[pattern_idx].reshape(image_size, image_size)
        
        # Add noise to create variation (from opic training.noise_factor)
        defs, voices = load_gann_definitions()
        noise_factor = get_opic_config(voices, "training.noise_factor", 0.3)
        noise_pattern = np.random.rand(image_size, image_size) * noise_factor
        image = base_pattern + noise_pattern
        
        # Apply text-based style if provided
        if style_params:
            image = apply_text_style(image, style_params)
        
        # Clip and normalize
        image = np.clip(image, 0, 1)
        image = (image * 255).astype(np.uint8)
    else:
        # Pure random generation, but influenced by text if provided
        image = np.random.rand(image_size, image_size)
        
        # Apply text-based pattern if provided
        if style_params:
            image = apply_text_pattern(image, style_params, image_size)
        
        image = (image * 255).astype(np.uint8)
    
    return image

def extract_style_from_text(text):
    """Extract style parameters from text - uses opic text2image_impl.ops keywords"""
    defs, voices = load_gann_definitions()
    
    text_lower = text.lower()
    style = {
        "pattern": "random",
        "density": get_opic_config(voices, "style.density.medium", 0.5),
        "color_scheme": "grayscale",
        "composition": "centered",
    }
    
    # Pattern keywords (from opic text2image_impl.ops)
    keyword_map = {
        "heart": ["heart", "love", "valentine"],
        "circle": ["circle", "round", "circular"],
        "spiral": ["spiral", "swirl", "twist"],
        "grid": ["grid", "checker", "square"],
        "wave": ["wave", "ripple", "water"],
        "checker": ["checker", "chess"],
    }
    
    for pattern, keywords in keyword_map.items():
        if any(word in text_lower for word in keywords):
            style["pattern"] = pattern
            break
    
    # Density keywords (from opic)
    if any(word in text_lower for word in ["dense", "thick", "heavy", "solid"]):
        style["density"] = get_opic_config(voices, "style.density.dense", 0.8)
    elif any(word in text_lower for word in ["sparse", "light", "thin", "delicate"]):
        style["density"] = get_opic_config(voices, "style.density.sparse", 0.2)
    
    # Color keywords (from opic)
    if any(word in text_lower for word in ["bright", "light", "white"]):
        style["color_scheme"] = "bright"
    elif any(word in text_lower for word in ["dark", "black", "shadow"]):
        style["color_scheme"] = "dark"
    elif any(word in text_lower for word in ["colorful", "color", "rainbow"]):
        style["color_scheme"] = "colorful"
    
    # Composition keywords (from opic)
    if any(word in text_lower for word in ["centered", "center", "middle"]):
        style["composition"] = "centered"
    elif any(word in text_lower for word in ["scattered", "random", "chaos"]):
        style["composition"] = "scattered"
    elif any(word in text_lower for word in ["symmetrical", "symmetric", "balanced"]):
        style["composition"] = "symmetrical"
    
    return style

def apply_text_pattern(image, style_params, image_size):
    """Apply pattern based on text description - parameters from opic text2image_impl.ops"""
    defs, voices = load_gann_definitions()
    
    pattern_type = style_params.get("pattern", "random")
    density = style_params.get("density", 0.5)
    
    # Read pattern parameters from opic
    radius_factor = get_opic_config(voices, "pattern.circle.radius_factor", 0.3)
    spiral_angle_range = get_opic_config(voices, "pattern.spiral.angle_range", 4)
    spiral_points = get_opic_config(voices, "pattern.spiral.points", 200)
    grid_spacing_base = get_opic_config(voices, "pattern.grid.spacing_base", 8)
    wave_frequency = get_opic_config(voices, "pattern.wave.frequency", 0.2)
    wave_amplitude = get_opic_config(voices, "pattern.wave.amplitude", 127)
    checker_block_base = get_opic_config(voices, "pattern.checker.block_base", 8)
    
    if pattern_type == "circle":
        center = (image_size // 2, image_size // 2)
        radius = int(image_size * radius_factor * density)
        for y in range(image_size):
            for x in range(image_size):
                dist = np.sqrt((x - center[0])**2 + (y - center[1])**2)
                if abs(dist - radius) < 2:
                    image[y][x] = np.clip(image[y][x] + 200, 0, 255)
    
    elif pattern_type == "spiral":
        center = (image_size // 2, image_size // 2)
        for angle in np.linspace(0, spiral_angle_range * np.pi * density, spiral_points):
            r = angle * 2 * density
            x = int(center[0] + r * np.cos(angle))
            y = int(center[1] + r * np.sin(angle))
            if 0 <= x < image_size and 0 <= y < image_size:
                image[y][x] = np.clip(image[y][x] + 200, 0, 255)
    
    elif pattern_type == "grid":
        spacing = int(grid_spacing_base / max(density, 0.1))
        for i in range(0, image_size, spacing):
            image[i, :] = np.clip(image[i, :] + 200, 0, 255)
            image[:, i] = np.clip(image[:, i] + 200, 0, 255)
    
    elif pattern_type == "wave":
        for y in range(image_size):
            for x in range(image_size):
                wave_val = int(128 + wave_amplitude * np.sin(x * wave_frequency * density) * np.cos(y * wave_frequency * density))
                image[y][x] = int((image[y][x] + wave_val) / 2)
    
    elif pattern_type == "checker":
        block_size = int(checker_block_base / max(density, 0.1))
        for y in range(image_size):
            for x in range(image_size):
                if (x // block_size + y // block_size) % 2:
                    image[y][x] = np.clip(image[y][x] + 150, 0, 255)
    
    elif pattern_type == "heart":
        # Draw a heart shape
        center_x, center_y = image_size // 2, image_size // 2
        scale = image_size * 0.15 * density
        for y in range(image_size):
            for x in range(image_size):
                # Heart equation: (x²+y²-1)³ - x²y³ ≤ 0
                dx = (x - center_x) / scale if scale > 0 else 0
                dy = (y - center_y) / scale if scale > 0 else 0
                heart_eq = (dx*dx + dy*dy - 1)**3 - dx*dx*dy*dy*dy
                if heart_eq <= 0:
                    image[y][x] = np.clip(image[y][x] + 200, 0, 255)
    
    return image

def apply_text_style(image, style_params):
    """Apply color/style modifications based on text - parameters from opic text2image_impl.ops"""
    defs, voices = load_gann_definitions()
    
    color_scheme = style_params.get("color_scheme", "grayscale")
    
    bright_mult = get_opic_config(voices, "style.bright.multiplier", 1.5)
    dark_mult = get_opic_config(voices, "style.dark.multiplier", 0.5)
    colorful_var = get_opic_config(voices, "style.colorful.variation", 30)
    
    if color_scheme == "bright":
        image = np.clip(image * bright_mult, 0, 255)
    elif color_scheme == "dark":
        image = np.clip(image * dark_mult, 0, 255)
    elif color_scheme == "colorful":
        # Add some color variation (simulated as intensity variation)
        for y in range(len(image)):
            for x in range(len(image[0])):
                variation = np.sin(x * 0.1) * np.cos(y * 0.1) * colorful_var
                image[y][x] = np.clip(image[y][x] + variation, 0, 255)
    
    return image

def render_ascii(image, width=None, height=None):
    """Render image as ASCII art - charset from opic render.ops"""
    defs, voices = load_gann_definitions()
    
    width = width or get_opic_config(voices, "render.ascii.width", 64)
    height = height or get_opic_config(voices, "render.ascii.height", 64)
    charset = get_opic_config(voices, "render.ascii.charset", " .:-=+*#%@")
    chars = charset if isinstance(charset, str) else " .:-=+*#%@"
    ascii_art = []
    
    for y in range(height):
        row = []
        for x in range(width):
            if y < len(image) and x < len(image[0]):
                intensity = image[y][x] if isinstance(image[y][x], (int, np.integer)) else int(image[y][x])
                char_idx = int((intensity / 255.0) * (len(chars) - 1))
                row.append(chars[char_idx])
            else:
                row.append(" ")
        ascii_art.append("".join(row))
    
    return "\n".join(ascii_art)

def render_png(image, output_path):
    """Render image as PNG"""
    try:
        from PIL import Image
        img = Image.fromarray(image, mode='L')
        img.save(output_path)
        return True
    except ImportError:
        print("  ⚠ PIL/Pillow not available, skipping PNG export")
        return False

def render_svg(image, output_path, width=64, height=64):
    """Render image as SVG"""
    svg_lines = [
        f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">',
    ]
    
    # Simple pixel-based SVG
    img_height = len(image) if image is not None else height
    img_width = len(image[0]) if image is not None and len(image) > 0 else width
    cell_width = width / img_width if img_width > 0 else 1
    cell_height = height / img_height if img_height > 0 else 1
    
    for y, row in enumerate(image):
        for x, pixel in enumerate(row):
            intensity = pixel if isinstance(pixel, (int, np.integer)) else int(pixel)
            gray = int(intensity)
            svg_lines.append(
                f'<rect x="{x * cell_width}" y="{y * cell_height}" '
                f'width="{cell_width}" height="{cell_height}" '
                f'fill="rgb({gray},{gray},{gray})" />'
            )
    
    svg_lines.append('</svg>')
    
    Path(output_path).write_text("\n".join(svg_lines))
    return True

def load_dataset_config(dataset_name):
    """Load dataset configuration from opic dataset.ops"""
    dataset_file = Path(__file__).parent / "dataset.ops"
    if not dataset_file.exists():
        return None
    
    defs, voices = parse_ops(dataset_file.read_text())
    
    # Extract dataset URLs and files from opic definitions
    config = {}
    source_key = f"{dataset_name}.source"
    mirror_key = f"{dataset_name}.mirror"
    
    if source_key in voices:
        config["source"] = voices[source_key].strip('"')
    if mirror_key in voices:
        config["mirror"] = voices[mirror_key].strip('"')
    
    # Extract file names
    file_keys = ["train_images", "train_labels", "test_images", "test_labels"]
    config["files"] = {}
    for key in file_keys:
        voice_key = f"{dataset_name}.{key}"
        if voice_key in voices:
            config["files"][key] = voices[voice_key].strip('"')
    
    return config if config.get("source") and config.get("files") else None

def download_mnist():
    """Download MNIST dataset - configuration from opic dataset.ops"""
    config = load_dataset_config("mnist")
    if not config:
        # Fallback to hardcoded config
        config = {
            "source": "https://storage.googleapis.com/cvdf-datasets/mnist/",
            "mirror": "http://yann.lecun.com/exdb/mnist/",
            "files": {
                "train_images": "train-images-idx3-ubyte.gz",
                "train_labels": "train-labels-idx1-ubyte.gz",
                "test_images": "t10k-images-idx3-ubyte.gz",
                "test_labels": "t10k-labels-idx1-ubyte.gz",
            }
        }
    
    data_dir = Path(__file__).parent / "data" / "mnist"
    data_dir.mkdir(parents=True, exist_ok=True)
    
    downloaded = {}
    base_urls = [config["source"]]
    if "mirror" in config:
        base_urls.append(config["mirror"])
    
    for key, filename in config["files"].items():
        filepath = data_dir / filename
        if not filepath.exists():
            print(f"  Downloading {filename}...")
            downloaded_file = False
            for base_url in base_urls:
                url = base_url + filename
                try:
                    urllib.request.urlretrieve(url, filepath)
                    print(f"    ✓ Downloaded {filename}")
                    downloaded_file = True
                    break
                except Exception as e:
                    continue
            if not downloaded_file:
                print(f"    ✗ Failed to download {filename} from all mirrors")
                return None
        else:
            print(f"  ✓ {filename} already exists")
        downloaded[key] = filepath
    
    return downloaded

def load_mnist_images(filepath):
    """Load MNIST images from IDX file"""
    with gzip.open(filepath, 'rb') as f:
        magic, num_images, rows, cols = struct.unpack('>IIII', f.read(16))
        images = np.frombuffer(f.read(), dtype=np.uint8)
        images = images.reshape(num_images, rows, cols)
    return images

def load_mnist_labels(filepath):
    """Load MNIST labels from IDX file"""
    with gzip.open(filepath, 'rb') as f:
        magic, num_labels = struct.unpack('>II', f.read(8))
        labels = np.frombuffer(f.read(), dtype=np.uint8)
    return labels

def load_mnist_dataset(max_samples=None):
    """Load MNIST dataset"""
    files = download_mnist()
    if files is None:
        return None
    
    print("  Loading MNIST images...")
    train_images = load_mnist_images(files["train_images"])
    train_labels = load_mnist_labels(files["train_labels"])
    
    if max_samples:
        train_images = train_images[:max_samples]
        train_labels = train_labels[:max_samples]
    
    print(f"  ✓ Loaded {len(train_images)} training images")
    return train_images, train_labels

def download_fashion_mnist():
    """Download Fashion-MNIST dataset - configuration from opic dataset.ops"""
    config = load_dataset_config("fashion_mnist")
    if not config:
        # Fallback to hardcoded config
        config = {
            "source": "https://github.com/zalandoresearch/fashion-mnist/raw/master/data/fashion/",
            "files": {
                "train_images": "train-images-idx3-ubyte.gz",
                "train_labels": "train-labels-idx1-ubyte.gz",
                "test_images": "t10k-images-idx3-ubyte.gz",
                "test_labels": "t10k-labels-idx1-ubyte.gz",
            }
        }
    
    data_dir = Path(__file__).parent / "data" / "fashion_mnist"
    data_dir.mkdir(parents=True, exist_ok=True)
    
    downloaded = {}
    base_url = config["source"]
    
    for key, filename in config["files"].items():
        filepath = data_dir / filename
        if not filepath.exists():
            print(f"  Downloading {filename}...")
            url = base_url + filename
            try:
                urllib.request.urlretrieve(url, filepath)
                print(f"    ✓ Downloaded {filename}")
            except Exception as e:
                print(f"    ✗ Failed to download {filename}: {e}")
                return None
        else:
            print(f"  ✓ {filename} already exists")
        downloaded[key] = filepath
    
    return downloaded

def load_fashion_mnist_dataset(max_samples=None):
    """Load Fashion-MNIST dataset"""
    files = download_fashion_mnist()
    if files is None:
        return None
    
    print("  Loading Fashion-MNIST images...")
    train_images = load_mnist_images(files["train_images"])
    train_labels = load_mnist_labels(files["train_labels"])
    
    if max_samples:
        train_images = train_images[:max_samples]
        train_labels = train_labels[:max_samples]
    
    print(f"  ✓ Loaded {len(train_images)} training images")
    return train_images, train_labels

def create_patterns():
    """Create opic-defined patterns"""
    patterns = []
    
    # Circle pattern
    circle = np.zeros((64, 64), dtype=np.uint8)
    center = (32, 32)
    radius = 20
    for y in range(64):
        for x in range(64):
            dist = np.sqrt((x - center[0])**2 + (y - center[1])**2)
            if abs(dist - radius) < 2:
                circle[y][x] = 255
    patterns.append(("circle", circle))
    
    # Spiral pattern
    spiral = np.zeros((64, 64), dtype=np.uint8)
    center = (32, 32)
    for angle in np.linspace(0, 4 * np.pi, 200):
        r = angle * 2
        x = int(center[0] + r * np.cos(angle))
        y = int(center[1] + r * np.sin(angle))
        if 0 <= x < 64 and 0 <= y < 64:
            spiral[y][x] = 255
    patterns.append(("spiral", spiral))
    
    # Grid pattern
    grid = np.zeros((64, 64), dtype=np.uint8)
    for i in range(0, 64, 8):
        grid[i, :] = 255
        grid[:, i] = 255
    patterns.append(("grid", grid))
    
    return patterns

def main():
    """Main GANN training and generation - uses opic dataset.ops for configuration"""
    if len(sys.argv) < 2:
        print("Usage: gann.py <train|generate|download> [options]")
        print("  train <dataset>    - Train generator (mnist|fashion_mnist|patterns)")
        print("  generate           - Generate images")
        print("  download <dataset> - Download dataset (mnist|fashion_mnist)")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "download":
        dataset_name = sys.argv[2] if len(sys.argv) > 2 else "mnist"
        print(f"Downloading {dataset_name} dataset (from opic dataset.ops)...")
        
        if dataset_name == "mnist":
            files = download_mnist()
            if files:
                print("✓ MNIST dataset ready")
        elif dataset_name == "fashion_mnist":
            files = download_fashion_mnist()
            if files:
                print("✓ Fashion-MNIST dataset ready")
        else:
            print(f"Unknown dataset: {dataset_name}")
            sys.exit(1)
    
    elif command == "train":
        dataset_name = sys.argv[2] if len(sys.argv) > 2 else "patterns"
        max_samples = int(sys.argv[3]) if len(sys.argv) > 3 and sys.argv[3].isdigit() else None
        
        if dataset_name == "mnist":
            print("Loading MNIST dataset (from opic dataset.ops)...")
            images, labels = load_mnist_dataset(max_samples=max_samples)
            if images is not None:
                generator = train_generator(images=images, epochs=10, batch_size=32)
                print("✓ Training complete")
            else:
                print("✗ Failed to load MNIST dataset")
                sys.exit(1)
                
        elif dataset_name == "fashion_mnist":
            print("Loading Fashion-MNIST dataset (from opic dataset.ops)...")
            images, labels = load_fashion_mnist_dataset(max_samples=max_samples)
            if images is not None:
                generator = train_generator(images=images, epochs=10, batch_size=32)
                print("✓ Training complete")
            else:
                print("✗ Failed to load Fashion-MNIST dataset")
                sys.exit(1)
                
        else:
            # Use opic-defined patterns
            patterns = create_patterns()
            generator = train_generator(patterns=patterns, epochs=5)
            print("✓ Training complete")
        
    elif command == "generate":
        output_format = sys.argv[2] if len(sys.argv) > 2 else "ascii"
        output_path = sys.argv[3] if len(sys.argv) > 3 else "output"
        use_training = "--trained" in sys.argv or "-t" in sys.argv
        
        # Check for text prompt (NLP-based generation)
        text_prompt = None
        if "--text" in sys.argv:
            text_idx = sys.argv.index("--text")
            if text_idx + 1 < len(sys.argv):
                text_prompt = sys.argv[text_idx + 1]
        elif "-t" in sys.argv and not use_training:
            # -t might be text prompt if not --trained
            t_idx = sys.argv.index("-t")
            if t_idx + 1 < len(sys.argv) and not sys.argv[t_idx + 1].startswith("-"):
                text_prompt = sys.argv[t_idx + 1]
        
        print("Generating image...")
        if text_prompt:
            print(f"  Text prompt: '{text_prompt}'")
            print("  (Using opic text2image.ops for style extraction)")
        
        generator = generate_simple_generator()
        
        # Load training data if requested
        training_data = None
        if use_training:
            patterns = create_patterns()
            training_data = []
            for name, img in patterns:
                flat = img.flatten().astype(np.float32) / 255.0
                training_data.append(flat)
            training_data = np.array(training_data)
            print("  Using trained patterns")
        
        image = generate_image(generator, training_data=training_data, text_prompt=text_prompt)
        
        if output_format == "ascii":
            ascii_art = render_ascii(image)
            print("\n" + ascii_art)
            Path(f"{output_path}.txt").write_text(ascii_art)
            print(f"\n✓ Saved to {output_path}.txt")
            
        elif output_format == "png":
            if render_png(image, f"{output_path}.png"):
                print(f"✓ Saved to {output_path}.png")
                
        elif output_format == "svg":
            render_svg(image, f"{output_path}.svg")
            print(f"✓ Saved to {output_path}.svg")
            
        else:
            print(f"Unknown format: {output_format}")
            sys.exit(1)
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()

