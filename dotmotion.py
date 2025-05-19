"""
Dotmotion - Polkadot Animation Library

A comprehensive animation toolkit for creating Polkadot ecosystem
visualizations using Manim. Includes components and animations for
relay chains, parachains, validators, nominators, governance, and more.

Usage:
    from dotmotion import PolkadotRelay, Parachain, Validator
    
    # Create a relay chain
    relay = PolkadotRelay()
    self.play(Create(relay))
    
    # Add a parachain
    para1 = Parachain(name="Acala", position=LEFT*3, color=ACALA_COLOR)
    self.play(relay.connect_parachain(para1))
"""

from manim import (VGroup, Circle, Text, Dot, Annulus, Polygon, Line,
                   RoundedRectangle, Arrow, DOWN, UP, LEFT, RIGHT, ORIGIN, TAU,
                   WHITE, Create, FadeIn, FadeOut, GrowFromCenter, Write,
                   BackgroundRectangle, BLACK)
import numpy as np
from typing import List, Tuple
import random

# ===== POLKADOT THEME CONSTANTS =====

# Official Polkadot palette from brand hub
POLKADOT_PINK = "#FF2670"  # Primary brand color
POLKADOT_BLACK = "#000000"
POLKADOT_WHITE = "#FFFFFF"
POLKADOT_LIME = "#E4FF07"
POLKADOT_CYAN = "#07FFFF"
POLKADOT_VIOLET = "#7916F3"

# Storm colors for additional styling
POLKADOT_STORM_200 = "#DCE2E9"
POLKADOT_STORM_400 = "#AEB7CB"
POLKADOT_STORM_700 = "#6E7391"

# Common parachain colors - using complementary colors
ACALA_COLOR = "#E40C5B"
MOONBEAM_COLOR = "#07FFFF"  # Using official cyan
ASTAR_COLOR = "#7916F3"  # Using official violet
PARALLEL_COLOR = "#E4FF07"  # Using official lime
CENTRIFUGE_COLOR = "#FF8A00"  # Orange complementary

# Animation durations for consistency
QUICK_FADE = 0.5
NORMAL_FADE = 1.0
NORMAL_CREATE = 1.5
COMPLEX_CREATE = 2.0

# ===== UTILITY FUNCTIONS =====


def create_text(text, font_size=24, color=WHITE):
    """Helper function to create text with the official Polkadot font
    
    Uses the Unbounded font (now installed in the system) with fallback 
    to Helvetica Neue
    """
    try:
        # First try to use the Unbounded font
        return Text(text,
                    font="Unbounded",
                    font_size=font_size,
                    color=color,
                    weight="BOLD")
    except Exception:
        # Fall back to Helvetica Neue if Unbounded is not available
        return Text(text,
                    font="Helvetica Neue",
                    font_size=font_size,
                    color=color,
                    weight="BOLD")


def create_text_with_background(text,
                                font_size=24,
                                color=WHITE,
                                bg_color=BLACK,
                                bg_opacity=0.8,
                                buff=0.4):
    """Create text with a background rectangle for better readability
    
    This helps prevent text from being hard to read when it overlaps with animations
    
    Parameters:
        text: The text to display
        font_size: Font size
        color: Text color
        bg_color: Background color
        bg_opacity: Background opacity
        buff: Padding around text
        
    Returns:
        VGroup containing the background and text
    """
    # Create the text
    text_obj = create_text(text, font_size=font_size, color=color)

    # Create the background
    bg = BackgroundRectangle(text_obj,
                             color=bg_color,
                             fill_opacity=bg_opacity,
                             buff=buff)

    # Group them together
    text_group = VGroup(bg, text_obj)

    return text_group


def hex_to_rgb(hex_color: str) -> Tuple[float, float, float]:
    """Convert hex color to RGB tuple with values from 0 to 1"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i + 2], 16) / 255 for i in (0, 2, 4))


# ===== COMPONENTS =====


class PolkadotRelay(VGroup):
    """
    Polkadot Relay Chain with customizable appearance
    """

    def __init__(self,
                 radius: float = 2.5,
                 color: str = POLKADOT_PINK,
                 n_validators: int = 6,
                 include_dots: bool = True,
                 **kwargs):
        super().__init__(**kwargs)

        # Store parameters
        self.radius = radius
        self.color = color
        self.n_validators = n_validators
        self.parachains = []

        # Create the relay chain ring
        self.ring = Annulus(
            inner_radius=radius - 0.15,  # Thicker ring
            outer_radius=radius,
            color=color,
            fill_opacity=0.4,  # More visible
            stroke_width=3)  # Thicker stroke
        self.add(self.ring)

        # Add Polkadot branding
        self.name = create_text("Relay Chain", font_size=26,
                                color=WHITE)  # Larger text
        self.name.move_to(self.ring.get_center())
        self.add(self.name)

        # Add validators (represented as dots around the relay chain)
        self.validators = VGroup()
        if include_dots:
            for i in range(n_validators):
                angle = i * TAU / n_validators
                pos = np.array(
                    [radius * np.cos(angle), radius * np.sin(angle), 0])
                dot = Dot(pos, color=WHITE, radius=0.12)  # Larger dots
                dot.set_fill(color, opacity=0.9)  # More vibrant
                self.validators.add(dot)
            self.add(self.validators)

    def connect_parachain(self, parachain, animate=False):
        """Connect a parachain to the relay chain"""
        # Add to our internal list
        self.parachains.append(parachain)

        # Calculate connection point on relay
        direction = parachain.get_center() - self.ring.get_center()
        direction_norm = direction / np.linalg.norm(direction)
        connection_point = self.ring.get_center(
        ) + direction_norm * self.radius

        # Create connection line
        line = Line(connection_point,
                    parachain.get_center() + direction_norm *
                    (-parachain.radius),
                    stroke_width=3,
                    color=POLKADOT_CYAN)

        # Create animation group
        if animate:
            return [Create(line), GrowFromCenter(parachain)]
        else:
            # Just return the elements to be added
            return VGroup(line, parachain)


class Parachain(VGroup):
    """
    Parachain circle with customizable appearance and content
    """

    def __init__(self,
                 name: str = "Parachain",
                 position=RIGHT * 4,
                 radius: float = 1.0,
                 color: str = MOONBEAM_COLOR,
                 **kwargs):
        super().__init__(**kwargs)
        self.radius = radius
        self.chain_name = name

        # Create the parachain circle
        self.circle = Circle(
            radius=radius,
            stroke_width=3,  # Thicker stroke
            color=color,
            fill_opacity=0.25,  # More visible
            fill_color=color)

        # Add the name label
        self.name = create_text(name, font_size=22, color=WHITE)  # Larger text
        self.name.move_to(self.circle.get_center())

        # Combine elements
        self.add(self.circle, self.name)
        self.move_to(position)


class Validator(VGroup):
    """
    Validator node with customizable appearance
    """

    def __init__(self,
                 position=ORIGIN,
                 size: float = 0.5,
                 color: str = POLKADOT_VIOLET,
                 active: bool = True,
                 label: str = None,
                 **kwargs):
        super().__init__(**kwargs)

        # Create hexagon shape for validator
        self.hexagon = Polygon(
            *[
                np.array([size * np.cos(angle), size * np.sin(angle), 0])
                for angle in np.linspace(0, TAU, 7)[:-1]
            ],
            color=color,
            fill_opacity=0.8 if active else 0.3,  # More vibrant
            stroke_width=3)  # Thicker stroke
        self.add(self.hexagon)

        # Add label if provided
        if label:
            self.label = create_text(label, font_size=18,
                                     color=WHITE)  # Larger text
            self.label.next_to(self.hexagon, DOWN, buff=0.2)
            self.add(self.label)

        # Position the validator
        self.move_to(position)


class Nominator(VGroup):
    """
    Nominator with connections to validators
    """

    def __init__(self,
                 position=LEFT * 3,
                 size: float = 0.3,
                 color: str = POLKADOT_CYAN,
                 **kwargs):
        super().__init__(**kwargs)

        # Create circle for nominator
        self.circle = Circle(
            radius=size,
            color=color,
            fill_opacity=0.7,  # More vibrant
            stroke_width=2)
        self.add(self.circle)

        # Position
        self.move_to(position)

    def connect_to_validator(self,
                             validator,
                             stake_amount=None,
                             animate=False):
        """Connect this nominator to a validator with optional stake amount"""
        # Create connection line
        line = Arrow(
            self.get_center(),
            validator.get_center(),
            buff=0.25,  # Adjusted buffer
            color=POLKADOT_CYAN,
            stroke_width=2,  # Thicker stroke
            max_tip_length_to_length_ratio=0.12)  # Better arrowhead

        # Add stake amount if provided
        if stake_amount:
            stake_text = create_text(f"{stake_amount} DOT",
                                     font_size=14,
                                     color=WHITE)  # Larger text
            stake_text.next_to(line.get_center(), UP, buff=0.15)

            if animate:
                return [Create(line), Write(stake_text)]
            else:
                return VGroup(line, stake_text)
        else:
            if animate:
                return Create(line)
            else:
                return line


class Block(VGroup):
    """
    Block representation for blockchain animations
    """

    def __init__(self,
                 position=ORIGIN,
                 label: str = "#1",
                 color: str = POLKADOT_PINK,
                 size: float = 0.5,
                 **kwargs):
        super().__init__(**kwargs)

        # Create block shape
        self.rect = RoundedRectangle(
            height=size,
            width=size * 1.6,  # Wider blocks
            corner_radius=0.12,  # Rounder corners
            color=color,
            fill_opacity=0.6,  # More vibrant
            stroke_width=2.5)  # Thicker stroke

        # Add block number/label
        self.label = create_text(label, font_size=18,
                                 color=WHITE)  # Larger text
        self.label.move_to(self.rect.get_center())

        # Combine elements
        self.add(self.rect, self.label)
        self.move_to(position)


class Transaction(VGroup):
    """
    Transaction representation for blockchain animations
    """

    def __init__(self,
                 start=LEFT * 2,
                 end=RIGHT * 2,
                 color: str = POLKADOT_PINK,
                 **kwargs):
        super().__init__(**kwargs)

        # Create transaction arrow
        self.arrow = Arrow(start=start,
                           end=end,
                           color=color,
                           buff=0.3,
                           stroke_width=2,
                           max_tip_length_to_length_ratio=0.1,
                           **kwargs)

        self.add(self.arrow)


class XCMMessage(VGroup):
    """
    Cross-Consensus Message (XCM) for cross-chain communication
    """

    def __init__(self,
                 start=LEFT * 3,
                 end=RIGHT * 3,
                 message: str = "XCM",
                 color: str = POLKADOT_VIOLET,
                 **kwargs):
        super().__init__(**kwargs)

        # Create message container - slightly larger
        self.container = RoundedRectangle(
            height=0.7,
            width=1.4,
            corner_radius=0.15,
            color=color,
            fill_opacity=0.5,  # More vibrant
            stroke_width=2)

        # Add message text
        self.text = create_text(message, font_size=16,
                                color=WHITE)  # Larger text
        self.text.move_to(self.container.get_center())

        # Add to group
        self.add(self.container, self.text)
        self.move_to(start)

        # Store destination for animations
        self.start_pos = start
        self.end_pos = end


class PolkadotEcosystem(VGroup):
    """
    Full Polkadot ecosystem with relay chain and multiple parachains
    """

    def __init__(self,
                 n_parachains: int = 5,
                 parachain_names: List[str] = None,
                 parachain_colors: List[str] = None,
                 relay_radius: float = 3.0,
                 **kwargs):
        super().__init__(**kwargs)

        # Create relay chain
        self.relay = PolkadotRelay(radius=relay_radius)
        self.add(self.relay)

        # Default parachain names if not provided
        if not parachain_names:
            parachain_names = [
                "Acala", "Moonbeam", "Astar", "Parallel", "Centrifuge"
            ]
            parachain_names = parachain_names[:n_parachains]

        # Default colors if not provided
        if not parachain_colors:
            parachain_colors = [
                ACALA_COLOR, MOONBEAM_COLOR, ASTAR_COLOR, PARALLEL_COLOR,
                CENTRIFUGE_COLOR
            ]
            parachain_colors = parachain_colors[:n_parachains]

        # Create parachains
        self.parachains = {}
        angles = np.linspace(0, TAU, n_parachains, endpoint=False)

        for i in range(n_parachains):
            angle = angles[i]
            pos = np.array([(relay_radius + 2.5) * np.cos(angle),
                            (relay_radius + 2.5) * np.sin(angle), 0])

            # Create parachain
            parachain = Parachain(name=parachain_names[i],
                                  position=pos,
                                  color=parachain_colors[i],
                                  radius=1.0)

            # Connect to relay
            connection = Line(self.relay.get_center() + np.array([
                relay_radius * np.cos(angle), relay_radius * np.sin(angle), 0
            ]),
                              pos - np.array([np.cos(angle),
                                              np.sin(angle), 0]),
                              color=POLKADOT_CYAN,
                              stroke_width=2)

            # Store in dictionary
            self.parachains[parachain_names[i]] = parachain

            # Add to group
            self.add(connection, parachain)


class GovernanceSystem(VGroup):
    """
    Polkadot governance components
    """

    def __init__(self,
                 position=ORIGIN,
                 width: float = 5.0,
                 height: float = 3.0,
                 **kwargs):
        super().__init__(**kwargs)

        # Background
        self.bg = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.25,  # Rounder corners
            color=POLKADOT_VIOLET,
            fill_opacity=0.15,  # Slightly more visible
            stroke_width=2)

        # Title
        self.title = create_text("Governance", font_size=28,
                                 color=WHITE)  # Larger text
        self.title.move_to(self.bg.get_top() + DOWN * 0.4)

        # Components - more consistent sizing and better visual hierarchy
        self.council = RoundedRectangle(
            width=1.8,
            height=0.7,
            corner_radius=0.15,
            color=POLKADOT_PINK,
            fill_opacity=0.6,  # More vibrant
            stroke_width=2)
        self.council.move_to(self.bg.get_center() + LEFT * 1.8 + UP * 0.5)
        self.council_text = create_text("Council", font_size=18,
                                        color=WHITE)  # Larger text
        self.council_text.move_to(self.council.get_center())

        self.tech = RoundedRectangle(
            width=1.8,
            height=0.7,
            corner_radius=0.15,
            color=POLKADOT_CYAN,
            fill_opacity=0.6,  # More vibrant
            stroke_width=2)
        self.tech.move_to(self.bg.get_center() + RIGHT * 1.8 + UP * 0.5)
        self.tech_text = create_text("Tech Comm", font_size=18,
                                     color=WHITE)  # Larger text
        self.tech_text.move_to(self.tech.get_center())

        self.referendum = RoundedRectangle(
            width=2.2,
            height=0.7,
            corner_radius=0.15,
            color=POLKADOT_STORM_700,
            fill_opacity=0.6,  # More vibrant
            stroke_width=2)
        self.referendum.move_to(self.bg.get_center() + DOWN * 1.0)
        self.referendum_text = create_text("Referendum",
                                           font_size=18,
                                           color=WHITE)  # Larger text
        self.referendum_text.move_to(self.referendum.get_center())

        # Add all components
        self.add(self.bg, self.title, self.council, self.council_text,
                 self.tech, self.tech_text, self.referendum,
                 self.referendum_text)

        # Position the whole system
        self.move_to(position)


# ===== ANIMATION PRESETS =====


def animate_block_production(scene, chain, n_blocks=5, duration=3.0):
    """
    Animate block production on a chain (relay or parachain)
    """
    blocks = []
    block_spacing = 0.6
    start_pos = chain.get_center() + UP * 1.5

    # Create and animate each block
    for i in range(n_blocks):
        block = Block(position=start_pos + RIGHT * (i * block_spacing),
                      label=f"#{i+1}",
                      color=POLKADOT_PINK)

        if i == 0:
            scene.play(Create(block), run_time=duration / n_blocks)
        else:
            prev_block = blocks[-1]
            # Create connection line
            conn = Line(prev_block.get_right(),
                        block.get_left(),
                        color=POLKADOT_STORM_700)
            scene.play(Create(conn),
                       Create(block),
                       run_time=duration / n_blocks)

        blocks.append(block)

    # Return the blocks for future reference
    return blocks


def animate_cross_chain_transfer(scene,
                                 source_chain,
                                 dest_chain,
                                 message="Transfer",
                                 duration=2.0):
    """
    Animate XCM message from one chain to another
    """
    # Create the XCM message
    xcm = XCMMessage(start=source_chain.get_center(),
                     end=dest_chain.get_center(),
                     message=message)

    # Animate message creation and movement
    scene.play(Create(xcm), run_time=duration / 3)
    scene.play(xcm.animate.move_to(xcm.end_pos), run_time=duration * 2 / 3)

    return xcm


def animate_validator_set_change(scene, validators, n_new=2, duration=2.0):
    """
    Animate validator set changing for era rotation
    
    Parameters:
        scene: The Manim scene to apply animations to
        validators: A VGroup containing validator objects to change
        n_new: Number of validators to replace
        duration: Animation duration in seconds
    """
    # Get positions of current validators
    val_positions = [v.get_center() for v in validators]

    # Remove some validators
    remove_idx = random.sample(range(len(val_positions)), n_new)
    removal_animations = [
        FadeOut(validators[i], run_time=duration / 2) for i in remove_idx
    ]
    scene.play(*removal_animations)

    # Add new validators
    new_validators = VGroup()
    for i in remove_idx:
        # Create with different color initially
        new_val = Validator(position=val_positions[i],
                            color=POLKADOT_VIOLET,
                            active=True)
        new_validators.add(new_val)

    # Animate new validators coming in
    scene.play(FadeIn(new_validators, run_time=duration / 2))

    # Return the new validators
    return new_validators
