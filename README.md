# Dotmotion - Polkadot Animation Toolkit

A comprehensive toolkit for creating elegant and on-brand animations of the Polkadot ecosystem using Manim. This toolkit provides reusable components and helper functions to create consistent, professional-quality animations.

## Features

- **Official Brand Elements**: Uses the official Polkadot colors and Unbounded font
- **Ecosystem Components**: Ready-made components for relay chains, parachains, validators, etc.
- **Animation Helpers**: Helper functions for common animation sequences
- **Text Management**: Built-in solutions to prevent text overlapping with animations
- **Customizable**: All components are fully customizable to fit your needs

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/MontaQLabs/DotMotion.git
   cd dotmotion
   ```

2. **Install dependencies**:
   ```bash
   pip install manim
   # Additional dependencies if needed
   ```

3. **Font Setup**:
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
# For medium quality preview
manim -pqm polkadot_demo.py PolkadotOverview

# For high quality render
manim -pqh polkadot_demo.py PolkadotOverview
```

## Best Practices

### Text and Animation Separation

For best results, follow these guidelines to prevent text and animations from overlapping:

1. **Phase-based approach**: Show explanatory text, then clear it before showing animations
2. **Use appropriate spacing**: Keep elements properly spaced on screen
3. **Add transition effects**: Use fade transitions between text and visualizations
4. **Center text when possible**: For maximum readability

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
