# Dotmotion - Polkadot Animation Toolkit

A comprehensive toolkit for creating elegant and on-brand animations of the Polkadot ecosystem using Manim. This toolkit provides reusable components and helper functions to create consistent, professional-quality animations.

## Current Demo
 [Demo](https://youtu.be/lQP7AkVDR5Y)

## Features

- **Official Brand Elements**: Uses the official Polkadot colors and Unbounded font
- **Ecosystem Components**: Ready-made components for relay chains, parachains, validators, etc.
- **Animation Helpers**: Helper functions for common animation sequences
- **Text Management**: Built-in solutions to prevent text overlapping with animations
- **Customizable**: All components are fully customizable to fit your needs

## Installation

### Recommended Installation with `uv`

The modern, recommended way to install Manim is using `uv`, a fast Python package installer and resolver:

1. **Install `uv`** (if not already installed):
   ```bash
   # macOS and Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Windows
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

2. **Create a new project and install Manim**:
   ```bash
   # Create a new project
   uv init your_project_name
   cd your_project_name
   
   # Add Manim as a dependency
   uv add manim
   
   # Verify installation
   uv run manim checkhealth
   ```

3. **Install Dotmotion**:
   ```bash
   # Clone the repository
   git clone https://github.com/MontaQLabs/DotMotion.git
   
   # Install as development package
   uv add -e ./DotMotion
   ```

### Alternative Installation

If you prefer not to use `uv`, you can also install using traditional methods:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/MontaQLabs/DotMotion.git
   cd DotMotion
   ```

2. **Install dependencies**:
   ```bash
   pip install manim
   pip install -e .
   ```

### Font Setup

The toolkit uses the Unbounded font, which is Polkadot's official font. To ensure animations render correctly:

- **Option 1**: Install the font system-wide (recommended)
  ```bash
  # For macOS
  mkdir -p ~/Library/Fonts/
  cp fonts/unbounded/*.ttf ~/Library/Fonts/
  
  # For Linux
  mkdir -p ~/.local/share/fonts/
  cp fonts/unbounded/*.ttf ~/.local/share/fonts/
  fc-cache -f -v
  
  # For Windows
  # Copy fonts from fonts/unbounded to C:\Windows\Fonts
  ```

- **Option 2**: Use the included fallback
  If you don't install the font, the toolkit will automatically fall back to Helvetica Neue, which still looks good.

## Quick Start Guide

### Installation with `uv` (Recommended)

```bash
# Install uv if you haven't already
# macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Create a new project and install Manim
uv init my_dotmotion_project
cd my_dotmotion_project
uv add manim

# Clone and install Dotmotion
git clone https://github.com/MontaQLabs/DotMotion.git
uv add -e ./DotMotion

# Verify installation
uv run manim checkhealth
```

### LaTeX Installation (Optional)

If you want to render mathematical formulas:

**macOS**: Install MacTeX
```bash
brew install --cask mactex
```

**Linux**: Install TeX Live 
```bash
sudo apt install texlive-full # For Debian/Ubuntu
sudo dnf install texlive-scheme-full # For Fedora
```

**Windows**: Install MiKTeX from https://miktex.org/download

### Creating Your First Animation

1. Create a new file called `my_first_animation.py`:

```python
from manim import Scene, UP, DOWN, LEFT, RIGHT
import dotmotion as dot

class MyFirstAnimation(Scene):
    def construct(self):
        # Create a relay chain
        relay = dot.PolkadotRelay(radius=2.5)
        self.play(dot.Create(relay))
        self.wait(1)
        
        # Add a parachain
        parachain = dot.Parachain(
            name="My Parachain", 
            position=LEFT*3, 
            color=dot.POLKADOT_CYAN
        )
        
        # Connect the parachain to the relay chain
        connection_anims = relay.connect_parachain(parachain, animate=True)
        self.play(*connection_anims)
        self.wait(2)

# Run the animation
if __name__ == "__main__":
    print("Run this with: manim -pqm my_first_animation.py MyFirstAnimation")
```

2. Run your animation:

```bash
# Using uv
uv run manim -pqm my_first_animation.py MyFirstAnimation

# Or, if you have Manim installed globally
manim -pqm my_first_animation.py MyFirstAnimation
```

For more examples, check out the included `dotmotion_demo.py` file.

## Getting Started

### Basic Usage

```python
from manim import Scene, UP, DOWN, LEFT, RIGHT
import dotmotion as dot  # Import the renamed library

class PolkadotDemo(Scene):
    def construct(self):
        # Create relay chain
        relay = dot.PolkadotRelay(radius=2.5)
        
        # Add it to the scene
        self.play(dot.Create(relay))
        
        # Create a parachain
        para = dot.Parachain(name="Acala", 
                           position=LEFT*3, 
                           color=dot.ACALA_COLOR)
        
        # Connect parachain to relay
        self.play(*relay.connect_parachain(para, animate=True))
```

### Running the Demo

```bash
# Using uv (recommended)
# For medium quality preview
uv run manim -pqm dotmotion_demo.py PolkadotOverview

# For high quality render
uv run manim -pqh dotmotion_demo.py PolkadotOverview

# Or, using global Manim installation
manim -pqm dotmotion_demo.py PolkadotOverview
manim -pqh dotmotion_demo.py PolkadotOverview
```

## Best Practices

### Text and Animation Separation

For best results, follow these guidelines to prevent text and animations from overlapping:

1. **Phase-based approach**: Show explanatory text, then clear it before showing animations
2. **Use appropriate spacing**: Keep elements properly spaced on screen
3. **Add transition effects**: Use fade transitions between text and visualizations
4. **Center text when possible**: For maximum readability

### Using Text with Backgrounds

The toolkit provides two ways to display text with backgrounds to prevent overlapping issues:

```python
# Method 1: Use the built-in utility function
from dotmotion import create_text_with_background

# Create text with a background rectangle
text_with_bg = create_text_with_background(
    "This text has a background",
    font_size=32,
    color=dot.POLKADOT_WHITE,
    bg_color=BLACK,  # Background color
    bg_opacity=0.8,  # Background opacity
    buff=0.4  # Padding around text
)
self.play(FadeIn(text_with_bg))

# Method 2: Create a custom display function like in the demo
def display_text_with_background(self, text, position=None, font_size=24, 
                               duration=2.0, dim_background=False):
    """Display text with a background, wait, then clean up"""
    text_obj = dot.create_text(text, font_size=font_size)
    
    # Ensure text fits within screen
    if text_obj.width > SCREEN_WIDTH * 0.8:
        text_obj.scale_to_fit_width(SCREEN_WIDTH * 0.8)
        
    # Position text 
    if position is not None:
        text_obj.move_to(position)
    
    # Add background for readability
    bg = BackgroundRectangle(text_obj, color=BLACK, opacity=0.8, buff=0.4)
    text_group = VGroup(bg, text_obj)
    
    # Optional full screen dimming for maximum contrast
    screen_dim = None
    if dim_background:
        screen_dim = RoundedRectangle(width=14, height=8, 
            corner_radius=0.1, fill_opacity=0.7, stroke_opacity=0,
            color=BLACK)
        self.play(FadeIn(screen_dim))
    
    # Show text, wait, then clean up
    self.play(FadeIn(text_group))
    self.wait(duration)
    self.play(FadeOut(text_group))
    
    if dim_background and screen_dim is not None:
        self.play(FadeOut(screen_dim))
```

## Available Components

- `PolkadotRelay`: The central relay chain
- `Parachain`: Individual parachains that connect to the relay chain
- `Validator`: Validator nodes for staking animations
- `Nominator`: Nominator entities for staking animations
- `Block`: Block representation for blockchain animations
- `XCMMessage`: Cross-chain messaging representation
- `GovernanceSystem`: Governance visualization components

## Color Palette

The toolkit includes the official Polkadot color palette:

- `POLKADOT_PINK`: #FF2670 (Primary brand color)
- `POLKADOT_BLACK`: #000000
- `POLKADOT_WHITE`: #FFFFFF
- `POLKADOT_LIME`: #E4FF07
- `POLKADOT_CYAN`: #07FFFF
- `POLKADOT_VIOLET`: #7916F3

Plus the Storm colors:
- `POLKADOT_STORM_200`: #DCE2E9
- `POLKADOT_STORM_400`: #AEB7CB
- `POLKADOT_STORM_700`: #6E7391

## Troubleshooting

### Font Issues

If you encounter warnings about missing fonts:

1. Verify the Unbounded font is installed in your system fonts directory
2. The toolkit will automatically fallback to Helvetica Neue if Unbounded is unavailable
3. If you still have issues, modify the `create_text` function in `dotmotion.py` to use a font that's available on your system

### Text Overlapping Issues

If you experience text overlapping with animations:

1. Implement the phase-based approach (show text, clear, then show animation)
2. Ensure text stays within screen boundaries by using `scale_to_fit_width`
3. Use `smooth_clear()` to transition between different sections

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Polkadot for their beautiful design system and brand identity
- Manim Community for their excellent animation library
