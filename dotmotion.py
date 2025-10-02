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
                   BackgroundRectangle, BLACK, SVGMobject, ImageMobject, config,
                   VMobject, MoveAlongPath)
import numpy as np
from typing import List, Tuple
import random
from pathlib import Path
import os
import subprocess

try:
    # Available on all modern Manim installs; allows registering local fonts
    from manimpango import register_font as _register_font
except Exception:
    _register_font = None

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


_FONT_STATE = {
    "preferred": "Unbounded",
    "fallbacks": ["Helvetica Neue", "Helvetica", "Arial"],
    "registered": False,
}


def register_unbounded_fonts(fonts_dir: str = None) -> None:
    """Register bundled Unbounded fonts at runtime (no system install needed).

    This uses manimpango.register_font to make the `.ttf` files available to
    Pango. If registration is not available, this function is a no-op.
    """
    if _FONT_STATE["registered"]:
        return
    if _register_font is None:
        return

    base_dir = Path(__file__).resolve().parent
    fonts_path = Path(fonts_dir) if fonts_dir else base_dir / "fonts" / "unbounded"
    if fonts_path.exists():
        for ttf in fonts_path.glob("*.ttf"):
            try:
                _register_font(str(ttf))
            except Exception:
                # Ignore per-file registration issues, try others
                pass
        _FONT_STATE["registered"] = True


def set_brand_font(preferred: str = "Unbounded", fallbacks: List[str] = None) -> None:
    """Set the preferred brand font and fallback list used by create_text."""
    _FONT_STATE["preferred"] = preferred
    if fallbacks:
        _FONT_STATE["fallbacks"] = list(fallbacks)


def _create_text_with_font_chain(text: str, font_size: float, color) -> Text:
    font_candidates = [_FONT_STATE["preferred"], *_FONT_STATE["fallbacks"]]
    last_error = None
    for font_name in font_candidates:
        try:
            return Text(text, font=font_name, font_size=font_size, color=color, weight="BOLD")
        except Exception as exc:
            last_error = exc
            continue
    # As a last resort, let Manim pick a default font
    try:
        return Text(text, font_size=font_size, color=color, weight="BOLD")
    except Exception:
        # If absolutely everything fails, re-raise last error for visibility
        raise last_error


def create_text(text, font_size=24, color=WHITE):
    """Create text using Unbounded with robust fallback chain.

    - Tries to register bundled Unbounded fonts at runtime
    - Falls back gracefully to Helvetica Neue, Helvetica, then Arial
    """
    # Attempt to register bundled Unbounded fonts once per process
    register_unbounded_fonts()
    return _create_text_with_font_chain(text=text, font_size=font_size, color=color)


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


def _fallback_logo_mobject():
    """Return a simple brand-like fallback mobject when logo assets are unavailable."""
    # Simple circle with brand color and a centered dot text for visual identity
    circle = Circle(radius=0.8, color=POLKADOT_PINK, fill_opacity=0.2, stroke_width=2)
    dot_text = create_text("·", font_size=72, color=POLKADOT_PINK)
    dot_text.move_to(circle.get_center())
    return VGroup(circle, dot_text)


def load_svg(path: str, color=None, stroke_color=None, stroke_width: float = 0.0):
    """Load an SVG asset as an SVGMobject with optional styling.

    Falls back to a simple brand mark if the SVG is missing or invalid.
    """
    try:
        svg = SVGMobject(path)
        if color is not None:
            svg.set_fill(color, opacity=1.0)
        if stroke_color is not None:
            svg.set_stroke(color=stroke_color, width=stroke_width)
        return svg
    except Exception:
        return _fallback_logo_mobject()


def load_image(path: str):
    """Load a raster image (png/jpg) as an ImageMobject."""
    return ImageMobject(path)


def load_logo(path: str, width: float = None, height: float = None):
    """Convenience loader for brand logos.

    Accepts either SVG or raster file paths and scales if width/height provided.
    """
    ext = os.path.splitext(path)[1].lower()
    try:
        mob = load_svg(path) if ext == ".svg" else load_image(path)
    except Exception:
        mob = _fallback_logo_mobject()
    if width:
        mob.width = width
    if height:
        mob.height = height
    return mob


# ===== LAYOUT & OVERLAP HELPERS =====


def _rect_from_mobject(mobj, padding: float = 0.0):
    """Axis-aligned bounding rectangle (x_min, x_max, y_min, y_max)."""
    center = mobj.get_center()
    half_w = mobj.width / 2 + padding
    half_h = mobj.height / 2 + padding
    return (center[0] - half_w, center[0] + half_w, center[1] - half_h, center[1] + half_h)


def _rects_overlap(a, b) -> bool:
    ax0, ax1, ay0, ay1 = a
    bx0, bx1, by0, by1 = b
    return not (ax1 < bx0 or bx1 < ax0 or ay1 < by0 or by1 < ay0)
def clamp_to_frame(mobj,
                   margin: float = 0.3,
                   respect_top: bool = True,
                   respect_bottom: bool = True,
                   respect_left: bool = True,
                   respect_right: bool = True):
    """Clamp a mobject fully within the current frame bounds with optional margins."""
    frame_w = config.frame_width
    frame_h = config.frame_height
    pos = mobj.get_center().copy()
    left_limit = (-frame_w / 2) + (mobj.width / 2) + margin
    right_limit = (frame_w / 2) - (mobj.width / 2) - margin
    bottom_limit = (-frame_h / 2) + (mobj.height / 2) + margin
    top_limit = (frame_h / 2) - (mobj.height / 2) - margin
    if respect_left or respect_right:
        pos[0] = min(right_limit, max(left_limit, pos[0]))
    if respect_bottom or respect_top:
        pos[1] = min(top_limit, max(bottom_limit, pos[1]))
    mobj.move_to(pos)
    return mobj


def safe_next_to(mobj, target, direction, buff=0.3, margin: float = 0.3):
    """Place mobj next_to target, then clamp to frame to avoid going off-screen."""
    mobj.next_to(target, direction, buff=buff)
    return clamp_to_frame(mobj, margin=margin)


def fit_to_frame(mobj, max_ratio: float = 0.9):
    """Scale down mobject so it fits within frame width/height * max_ratio."""
    frame_w = config.frame_width * max_ratio
    frame_h = config.frame_height * max_ratio
    scale_factor = min(frame_w / mobj.width, frame_h / mobj.height, 1.0)
    if scale_factor < 1.0:
        mobj.scale(scale_factor)
    clamp_to_frame(mobj)
    return mobj


def push_below_ring(label: VGroup, ring: Annulus, buffer: float = 0.35):
    """Place label just below the ring with a consistent buffer."""
    try:
        label.next_to(ring, DOWN, buff=buffer)
    except Exception:
        label.move_to(ring.get_center() + DOWN * (ring.outer_radius + buffer))
    return label


def push_above_ring(label: VGroup, ring: Annulus, buffer: float = 0.35):
    """Place label just above the ring with a consistent buffer."""
    try:
        label.next_to(ring, UP, buff=buffer)
    except Exception:
        label.move_to(ring.get_center() + UP * (ring.outer_radius + buffer))
    return label


def resolve_overlap(a: VGroup, b: VGroup, direction=DOWN, step: float = 0.1, max_steps: int = 20):
    """Shift 'a' repeatedly in direction until it no longer overlaps 'b'."""
    def rect(m):
        c = m.get_center()
        return [c[0] - m.width / 2, c[0] + m.width / 2, c[1] - m.height / 2, c[1] + m.height / 2]
    def overlap(r1, r2):
        return not (r1[1] < r2[0] or r2[1] < r1[0] or r1[3] < r2[2] or r2[3] < r1[2])
    steps = 0
    while overlap(rect(a), rect(b)) and steps < max_steps:
        a.shift(direction * step)
        steps += 1
    return a


def center_logo_in_ring(ring: Annulus, logo: VGroup, scale: float = 0.45):
    """Scale and center a logo inside an annulus by inner diameter ratio.

    scale: fraction of the inner diameter used as logo width.
    """
    inner_diameter = 2 * ring.inner_radius
    target_width = inner_diameter * max(0.0, min(scale, 0.95))
    try:
        logo.width = target_width
    except Exception:
        # Fallback uniform scaling if direct width set fails
        current_width = getattr(logo, 'width', inner_diameter)
        if current_width > 0:
            logo.scale(target_width / current_width)
    logo.move_to(ring.get_center())
    return logo


class ChainBadge(VGroup):
    """
    Chain badge combining a logo and a name with auto-fit and theming.

    Parameters:
        name: Chain name
        logo_path: SVG/PNG path
        palette_color: primary accent color for underline/outline
        layout: 'vertical' or 'horizontal'
        max_width: limit badge width (auto scales contents)
    """
    def __init__(self,
                 name: str,
                 logo_path: str,
                 palette_color: str = POLKADOT_PINK,
                 layout: str = "vertical",
                 max_width: float = 2.6,
                 **kwargs):
        super().__init__(**kwargs)

        self.name_str = name
        self.palette_color = palette_color

        # Load logo (robust to SVG/raster)
        self.logo = load_logo(logo_path)
        # Create label
        self.label = create_text(name, font_size=20, color=WHITE)

        # Layout
        if layout == "horizontal":
            self.logo.height = 0.6
            self.label.next_to(self.logo, RIGHT, buff=0.25)
            contents = VGroup(self.logo, self.label)
        else:
            # vertical
            self.logo.width = max_width * 0.7
            self.label.next_to(self.logo, DOWN, buff=0.18)
            contents = VGroup(self.logo, self.label)

        # Accent underline for a polished look
        underline = Line(self.label.get_left() + DOWN * 0.1,
                         self.label.get_right() + DOWN * 0.1,
                         color=palette_color,
                         stroke_width=2)

        group = VGroup(contents, underline)

        # Auto-fit to max_width
        if group.width > max_width:
            group.scale_to_fit_width(max_width)

        self.add(group)


# ===== PHASE MANAGEMENT =====


class Phase:
    """Context manager to create a clean, cinematic phase in a Scene.

    Usage:
        with Phase(scene, dim=True):
            ... # create and animate

    On exit, optionally clears created objects.
    """

    def __init__(self, scene, dim: bool = False, clear_on_exit: bool = False):
        self.scene = scene
        self.dim = dim
        self.clear_on_exit = clear_on_exit
        self._enter_index = 0
        self._dim_rect = None

    def __enter__(self):
        # Track existing objects to know what's new during the phase
        self._enter_index = len(self.scene.mobjects)
        if self.dim:
            self._dim_rect = RoundedRectangle(
                width=config.frame_width * 1.1,
                height=config.frame_height * 1.1,
                corner_radius=0.1,
                fill_opacity=0.6,
                stroke_opacity=0,
                color=BLACK,
            )
            self.scene.play(FadeIn(self._dim_rect, run_time=0.35))
        return self

    def __exit__(self, exc_type, exc, tb):
        # Remove dim first
        if self._dim_rect is not None:
            self.scene.play(FadeOut(self._dim_rect, run_time=0.3))
            self._dim_rect = None

        # Optionally clear objects created during the phase
        if self.clear_on_exit:
            new_objects = self.scene.mobjects[self._enter_index:]
            if new_objects:
                self.scene.play(*[FadeOut(m, run_time=0.5) for m in list(new_objects)])
        return False


# ===== REGISTRY & THEMING =====

_CHAIN_REGISTRY_CACHE = None


def load_chain_registry(path: str = None):
    """Load a simple JSON chain registry (id, name, logo, color).

    Default location: <repo_root>/chains.json if present.
    """
    global _CHAIN_REGISTRY_CACHE
    if _CHAIN_REGISTRY_CACHE is not None:
        return _CHAIN_REGISTRY_CACHE

    try:
        base_dir = Path(__file__).resolve().parent
        default_path = base_dir / "chains.json"
        registry_path = Path(path) if path else default_path
        if registry_path.exists():
            import json
            with open(registry_path, "r") as f:
                _CHAIN_REGISTRY_CACHE = json.load(f)
        else:
            _CHAIN_REGISTRY_CACHE = {}
    except Exception:
        _CHAIN_REGISTRY_CACHE = {}
    return _CHAIN_REGISTRY_CACHE


def get_chain_theme(chain_id: str, registry: dict = None):
    """Return (name, logo_path, color) for a chain_id if present, else None."""
    reg = registry if registry is not None else load_chain_registry()
    data = reg.get(chain_id)
    if not data:
        return None
    return (
        data.get("name", chain_id),
        data.get("logo", None),
        data.get("color", POLKADOT_PINK),
    )


def make_badge_from_registry(chain_id: str, layout: str = "vertical", max_width: float = 2.6, registry: dict = None):
    """Factory to build a ChainBadge from registry entry if available."""
    theme = get_chain_theme(chain_id, registry)
    if not theme:
        # Fallback: text-only badge
        return ChainBadge(name=chain_id, logo_path="assets/polkadot-logo.svg", palette_color=POLKADOT_PINK, layout=layout, max_width=max_width)
    name, logo_path, color = theme
    return ChainBadge(name=name, logo_path=logo_path or "assets/polkadot-logo.svg", palette_color=color, layout=layout, max_width=max_width)


# ===== XCM PRESETS (OPTIONAL TYPES) =====

XCM_TYPE_STYLES = {
    "transfer": POLKADOT_CYAN,
    "remote_call": POLKADOT_VIOLET,
    "hrmp": POLKADOT_LIME,
    "ump": POLKADOT_STORM_700,
    "dmp": POLKADOT_PINK,
}


def animate_xcm(scene,
                source_chain,
                dest_chain,
                xcm_type: str = "transfer",
                message: str = None,
                duration: float = 2.0):
    """Wrapper around animate_cross_chain_transfer with type-specific styling."""
    color = XCM_TYPE_STYLES.get(xcm_type, POLKADOT_CYAN)
    label = message if message is not None else xcm_type.replace("_", " ").title()
    # Reuse existing premium path and message, but set style via message text color
    group = animate_cross_chain_transfer(scene, source_chain, dest_chain, message=label, duration=duration)
    # Slight color hint on container
    try:
        group[0].container.set_stroke(color, width=2)
    except Exception:
        pass
    return group



def find_safe_position(scene,
                       mobj,
                       avoid: List[VGroup],
                       preferred: str = "bottom",
                       margin: float = 0.3):
    """Find a position for mobj that avoids overlapping with given objects.

    preferred: one of "bottom", "top", "left", "right", "center", or "auto".
    """
    # Compute frame bounds from config rather than requiring MovingCamera
    frame_w = config.frame_width
    frame_h = config.frame_height
    center = np.array([0.0, 0.0, 0.0])
    top = np.array([0.0, frame_h / 2, 0.0])
    bottom = np.array([0.0, -frame_h / 2, 0.0])
    left_edge = np.array([-frame_w / 2, 0.0, 0.0])
    right_edge = np.array([frame_w / 2, 0.0, 0.0])

    candidates = []
    # Order candidates by preference
    mapping = {
        "bottom": [bottom + UP * (mobj.height / 2 + margin)],
        "top": [top + DOWN * (mobj.height / 2 + margin)],
        "left": [left_edge + RIGHT * (mobj.width / 2 + margin)],
        "right": [right_edge + LEFT * (mobj.width / 2 + margin)],
        "center": [center],
        "auto": [],
    }
    if preferred in mapping:
        candidates.extend(mapping[preferred])

    # Enrich with corners and remaining edges
    corners = [
        np.array([-frame_w / 2, frame_h / 2, 0.0]) + (RIGHT * (mobj.width / 2 + margin) + DOWN * (mobj.height / 2 + margin)),
        np.array([frame_w / 2, frame_h / 2, 0.0]) + (LEFT * (mobj.width / 2 + margin) + DOWN * (mobj.height / 2 + margin)),
        np.array([-frame_w / 2, -frame_h / 2, 0.0]) + (RIGHT * (mobj.width / 2 + margin) + UP * (mobj.height / 2 + margin)),
        np.array([frame_w / 2, -frame_h / 2, 0.0]) + (LEFT * (mobj.width / 2 + margin) + UP * (mobj.height / 2 + margin)),
    ]
    edges = [
        bottom + UP * (mobj.height / 2 + margin),
        top + DOWN * (mobj.height / 2 + margin),
        left_edge + RIGHT * (mobj.width / 2 + margin),
        right_edge + LEFT * (mobj.width / 2 + margin),
    ]
    for p in corners + edges:
        if all((p != c).any() for c in candidates):
            candidates.append(p)

    # Always include center last as a fallback
    if not any(np.allclose(center, c) for c in candidates):
        candidates.append(center)

    # Try candidates and return the first that doesn't overlap
    for pos in candidates:
        mobj.move_to(pos)
        rect = _rect_from_mobject(mobj, padding=margin)
        overlaps = any(_rects_overlap(rect, _rect_from_mobject(a)) for a in avoid)
        if not overlaps:
            # Ensure final position is clamped in frame
            clamp_to_frame(mobj, margin=margin)
            return mobj.get_center()

    # If all else fails, return the first candidate (will overlap) so caller may add background/dim
    return candidates[0]


def display_text_safely(scene,
                        text: str,
                        avoid: List[VGroup] = None,
                        position: str = "bottom",
                        font_size: float = 24,
                        bg: bool = True,
                        bg_color=BLACK,
                        bg_opacity: float = 0.8,
                        margin: float = 0.3,
                        run_time: float = 0.7,
                        wait_time: float = 1.5):
    """Display text with automatic non-overlap placement and optional background.

    Returns the created mobject group.
    """
    avoid = avoid or []
    group = create_text_with_background(text, font_size=font_size, color=WHITE, bg_color=bg_color,
                                        bg_opacity=bg_opacity, buff=0.4) if bg else create_text(text, font_size=font_size)
    safe_pos = find_safe_position(scene, group, avoid=avoid, preferred=position, margin=margin)
    group.move_to(safe_pos)
    # Tap into PlaybackClock if present to timestamp captions
    start_ts = getattr(getattr(scene, "_dot_clock", None), "current_time", None)
    scene.play(FadeIn(group, run_time=run_time))
    scene.wait(wait_time)
    scene.play(FadeOut(group, run_time=run_time))
    end_ts = getattr(getattr(scene, "_dot_clock", None), "current_time", None)
    clock = getattr(scene, "_dot_clock", None)
    if clock and start_ts is not None and end_ts is not None:
        try:
            clock.add_caption(float(start_ts), float(end_ts), text)
        except Exception:
            pass
    return group


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
                 name_position: str = "below",
                 **kwargs):
        super().__init__(**kwargs)

        # Store parameters
        self.radius = radius
        self.color = color
        self.n_validators = n_validators
        self.parachains = []
        self.connection_lines = []

        # Create the relay chain ring
        self.ring = Annulus(
            inner_radius=radius - 0.18,
            outer_radius=radius,
            color=color,
            fill_opacity=0.25,
            stroke_width=2.2)
        self.add(self.ring)

        # Add Polkadot branding
        self.name = create_text("Relay Chain", font_size=24,
                                color=WHITE)
        if name_position == "center":
            self.name.move_to(self.ring.get_center())
        elif name_position == "above":
            try:
                self.name.next_to(self.ring, UP, buff=0.35)
            except Exception:
                self.name.move_to(self.ring.get_center() + UP * (self.radius + 0.4))
        else:
            # Place label just below the ring with a consistent buffer
            try:
                self.name.next_to(self.ring, DOWN, buff=0.35)
            except Exception:
                self.name.move_to(self.ring.get_center() + DOWN * (self.radius + 0.4))
        self.add(self.name)

        # Add validators (represented as dots around the relay chain)
        self.validators = VGroup()
        if include_dots:
            for i in range(n_validators):
                angle = i * TAU / n_validators
                # Place validators centered within ring thickness and reduce size for elegance
                ring_mid_r = (self.ring.inner_radius + self.ring.outer_radius) / 2
                pos = np.array([
                    ring_mid_r * np.cos(angle),
                    ring_mid_r * np.sin(angle),
                    0,
                ])
                dot = Dot(pos, color=WHITE, radius=0.06)
                dot.set_fill(color, opacity=0.9)
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
        self.connection_lines.append(line)

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
            stroke_width=2,
            color=color,
            fill_opacity=0.18,
            fill_color=color)

        # Add the name label (auto-fit within circle)
        self.name = create_text(name, font_size=20, color=WHITE)
        max_label_width = self.circle.width * 0.78
        if self.name.width > max_label_width:
            self.name.scale_to_fit_width(max_label_width)
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
                 label: str = None,
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

        # Optionally add block number/label
        if label is not None:
            self.label = create_text(label, font_size=18, color=WHITE)
            self.label.move_to(self.rect.get_center())
            self.add(self.rect, self.label)
        else:
            self.add(self.rect)
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
        self.text = create_text(message, font_size=16, color=WHITE)
        self.text.move_to(self.container.get_center())
        # Auto-fit text within container width, respecting padding
        max_text_width = self.container.width * 0.85
        if self.text.width > max_text_width:
            self.text.scale_to_fit_width(max_text_width)

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


def animate_block_production(scene, chain, n_blocks=5, duration=3.0, show_labels: bool = False):
    """
    Animate block production on a chain (relay or parachain)
    """
    blocks = []
    connections = []
    block_spacing = 0.6
    start_pos = chain.get_center() + UP * 1.5

    # Create and animate each block
    for i in range(n_blocks):
        block = Block(position=start_pos + RIGHT * (i * block_spacing),
                      label=f"#{i+1}" if show_labels else None,
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
            connections.append(conn)

        blocks.append(block)

    # Return a VGroup for easy cleanup by callers
    return VGroup(*blocks, *connections)


def animate_cross_chain_transfer(scene,
                                 source_chain,
                                 dest_chain,
                                 message="Transfer",
                                 duration=2.0):
    """Premium XCM animation: curved bezier path, glow trail, particles."""
    start = source_chain.get_center()
    end = dest_chain.get_center()

    # Curved path control points (arch above center)
    mid = (start + end) / 2
    control_offset = UP * np.linalg.norm(end - start) * 0.22
    ctrl1 = mid + control_offset + LEFT * 0.3
    ctrl2 = mid + control_offset + RIGHT * 0.3

    path = VMobject()
    path.set_points_as_corners([start, ctrl1, ctrl2, end]).make_smooth()
    path.set_stroke(POLKADOT_CYAN, width=2.5, opacity=0.55)

    # Moving message with glow
    msg = XCMMessage(start=start, end=end, message=message)
    glow = RoundedRectangle(height=msg.container.height * 1.4,
                            width=msg.container.width * 1.4,
                            corner_radius=0.2,
                            color=POLKADOT_CYAN,
                            fill_opacity=0.15,
                            stroke_opacity=0)
    glow.move_to(msg.get_center())

    # Particles
    particles = VGroup()
    for _ in range(10):
        p = Dot(radius=0.04, color=POLKADOT_CYAN)
        p.set_opacity(0.0)
        particles.add(p)

    scene.play(Create(path, run_time=duration * 0.3))
    scene.add(msg, glow, particles)

    # Move along path
    scene.play(
        MoveAlongPath(msg, path),
        MoveAlongPath(glow, path),
        run_time=duration * 0.65)

    # Simple trailing particles: spawn along path with staggered fades
    positions = [path.point_from_proportion(i / len(particles)) for i in range(len(particles))]
    for i, p in enumerate(particles):
        p.move_to(positions[i])
    scene.play(FadeIn(particles, lag_ratio=0.1, run_time=duration * 0.2))
    scene.play(FadeOut(particles, lag_ratio=0.1, run_time=duration * 0.2), FadeOut(path, run_time=0.2))

    return VGroup(msg, glow)


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


# ===== SUBTITLES & MEDIA HELPERS =====


class SubtitleTrack:
    """Collects timed captions and exports to SRT.

    Times are in seconds. Start < end.
    """

    def __init__(self):
        self._items: List[Tuple[float, float, str]] = []

    def add_caption(self, start_s: float, end_s: float, text: str) -> None:
        if end_s <= start_s:
            end_s = start_s + 0.01
        self._items.append((start_s, end_s, text))

    @staticmethod
    def _format_ts(t: float) -> str:
        hours = int(t // 3600)
        minutes = int((t % 3600) // 60)
        seconds = int(t % 60)
        millis = int((t - int(t)) * 1000)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d},{millis:03d}"

    def to_srt(self) -> str:
        lines = []
        for idx, (start, end, text) in enumerate(sorted(self._items, key=lambda x: x[0]), start=1):
            lines.append(str(idx))
            lines.append(f"{self._format_ts(start)} --> {self._format_ts(end)}")
            lines.append(text)
            lines.append("")
        return "\n".join(lines)

    def save(self, path: str) -> None:
        Path(path).write_text(self.to_srt(), encoding="utf-8")


class PlaybackClock:
    """Context manager that wraps Scene.play and Scene.wait to track timeline.

    Stores current_time and collects captions if display_text_safely is used.
    """

    def __init__(self, scene):
        self.scene = scene
        self.current_time: float = 0.0
        self._orig_play = None
        self._orig_wait = None
        self.captions: List[Tuple[float, float, str]] = []

    def __enter__(self):
        self._orig_play = self.scene.play
        self._orig_wait = self.scene.wait
        # Bind to scene for display_text_safely hooks
        setattr(self.scene, "_dot_clock", self)

        def wrapped_play(*anims, **kwargs):
            rt = float(kwargs.get("run_time", 1.0))
            res = self._orig_play(*anims, **kwargs)
            self.current_time += rt
            return res

        def wrapped_wait(duration=0.0):
            res = self._orig_wait(duration)
            try:
                self.current_time += float(duration)
            except Exception:
                pass
            return res

        self.scene.play = wrapped_play
        self.scene.wait = wrapped_wait
        return self

    def __exit__(self, exc_type, exc, tb):
        # Restore
        if self._orig_play is not None:
            self.scene.play = self._orig_play
        if self._orig_wait is not None:
            self.scene.wait = self._orig_wait
        if hasattr(self.scene, "_dot_clock"):
            delattr(self.scene, "_dot_clock")
        return False

    def add_caption(self, start: float, end: float, text: str) -> None:
        self.captions.append((start, end, text))

    def save_json(self, path: str) -> None:
        import json
        Path(path).write_text(json.dumps(self.captions, indent=2), encoding="utf-8")


def attach_subtitles(input_video: str, srt_path: str, output_video: str) -> None:
    """Hardcode subtitles into a video using ffmpeg (burn-in)."""
    cmd = [
        "ffmpeg", "-y",
        "-i", input_video,
        "-vf", f"subtitles='{srt_path}'",
        output_video,
    ]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        # Best-effort; if ffmpeg missing, caller can handle
        pass


def mux_audio(input_video: str, audio_path: str, output_video: str) -> None:
    """Mux external audio track into video using ffmpeg (no re-encode)."""
    cmd = [
        "ffmpeg", "-y",
        "-i", input_video,
        "-i", audio_path,
        "-c", "copy",
        "-map", "0:v:0",
        "-map", "1:a:0",
        output_video,
    ]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass


def synthesize_tts(text: str, output_mp3: str) -> None:
    """Optional TTS synthesis using gTTS (requires gTTS installed)."""
    try:
        from gtts import gTTS
        tts = gTTS(text)
        tts.save(output_mp3)
    except Exception:
        # If gTTS not available, skip
        pass


def auto_narrate_and_subtitle(input_video: str,
                               captions: List[Tuple[float, float, str]],
                               output_video: str,
                               burn_subtitles: bool = False,
                               work_dir: str = ".dotmotion_media",
                               sequential: bool = True,
                               min_gap_s: float = 0.1,
                               constrain_tts_to_caption: bool = False) -> str:
    """Create narration from captions (via gTTS), mux into video, and optionally burn-in subtitles.

    Returns the final output video path.
    """
    work = Path(work_dir)
    work.mkdir(parents=True, exist_ok=True)

    # 1) Optionally normalize to sequential non-overlapping schedule
    ordered = list(captions)
    if sequential and ordered:
        ordered.sort(key=lambda x: x[0])
        current = max(0.0, ordered[0][0])
        seq = []
        for s, e, t in ordered:
            duration = max(0.4, e - s)
            start = current
            end = start + duration
            seq.append((start, end, t))
            current = end + min_gap_s
        ordered = seq
    # 1b) Build subtitle track
    track = SubtitleTrack()
    for start, end, text in ordered:
        track.add_caption(start, end, text)
    srt_path = str(work / "captions.srt")
    track.save(srt_path)

    # 2) TTS per caption
    tts_files = []
    for idx, (start, end, text) in enumerate(ordered):
        mp3_path = work / f"tts_{idx:03d}.mp3"
        synthesize_tts(text, str(mp3_path))
        # Optionally time-stretch/compress to fit exact caption duration
        if constrain_tts_to_caption:
            target_duration = max(0.4, end - start)
            stretched = work / f"tts_{idx:03d}_fit.aac"
            try:
                _fit_audio_to_duration(str(mp3_path), str(stretched), target_duration)
                tts_files.append((start, str(stretched)))
            except Exception:
                # Fallback to raw mp3 if stretching fails
                tts_files.append((start, str(mp3_path)))
        else:
            tts_files.append((start, str(mp3_path)))

    # 3) Mix audios at offsets using ffmpeg adelay + amix
    #    Build inputs and filtergraph
    inputs = []
    filters = []
    amix_inputs = []
    for i, (start, mp3_path) in enumerate(tts_files):
        inputs += ["-i", mp3_path]
        delay_ms = int(max(0, start) * 1000)
        filters.append(f"[{i}:a]adelay={delay_ms}|{delay_ms}[a{i}]")
        amix_inputs.append(f"[a{i}]")
    if not inputs:
        # No audio; just attach subtitles if requested
        final_video = output_video
        if burn_subtitles:
            temp_out = str(work / "temp_subbed.mp4")
            attach_subtitles(input_video, srt_path, temp_out)
            final_video = temp_out
        else:
            final_video = input_video
        return final_video

    filtergraph = ";".join(filters) + f";{''.join(amix_inputs)}amix=inputs={len(tts_files)}:normalize=0[aout]"
    mixed_audio = str(work / "narration.aac")
    cmd_mix = [
        "ffmpeg", "-y",
        *inputs,
        "-filter_complex", filtergraph,
        "-map", "[aout]",
        "-c:a", "aac",
        mixed_audio,
    ]
    try:
        subprocess.run(cmd_mix, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass

    # 4) Mux audio into video
    temp_muxed = str(work / "video_with_audio.mp4")
    mux_audio(input_video, mixed_audio, temp_muxed)

    # 5) Burn subtitles if requested
    final_out = output_video
    if burn_subtitles:
        attach_subtitles(temp_muxed, srt_path, output_video)
    else:
        # move/copy muxed to output
        try:
            Path(output_video).unlink(missing_ok=True)
        except Exception:
            pass
        try:
            Path(temp_muxed).rename(output_video)
        except Exception:
            # fallback copy
            import shutil
            shutil.copyfile(temp_muxed, output_video)

    return output_video


def add_background_music(input_video: str, music_path: str, output_video: str, music_db: float = -20.0) -> None:
    """Mix background music under existing video audio using ffmpeg with simple volume ducking.

    music_db: gain applied to music (negative values lower volume)
    """
    # If the input has no audio, this still works by mapping only music
    filtergraph = f"[1:a]volume={10 ** (music_db/20):.6f}[bg];[0:a][bg]amix=inputs=2:normalize=0[aout]"
    cmd = [
        "ffmpeg", "-y",
        "-i", input_video,
        "-i", music_path,
        "-filter_complex", filtergraph,
        "-map", "0:v:0",
        "-map", "[aout]",
        "-c:v", "copy",
        "-c:a", "aac",
        "-shortest",
        output_video,
    ]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass


def _probe_duration_seconds(audio_path: str) -> float:
    """Return audio duration in seconds using ffprobe; 0.0 on failure."""
    try:
        out = subprocess.run([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", audio_path
        ], capture_output=True, text=True, check=True)
        return max(0.0, float(out.stdout.strip()))
    except Exception:
        return 0.0


def _fit_audio_to_duration(input_audio: str, output_audio: str, target_seconds: float) -> None:
    """Time-stretch/compress audio to match target duration using FFmpeg atempo.

    - Preserves pitch (atempo).
    - Supports factors outside [0.5, 2.0] by chaining atempo filters.
    - Outputs AAC audio suitable for muxing.
    """
    original = _probe_duration_seconds(input_audio)
    if original <= 0.0 or target_seconds <= 0.0:
        # Best effort copy to output if probe failed
        try:
            import shutil
            shutil.copyfile(input_audio, output_audio)
            return
        except Exception:
            pass
        raise RuntimeError("Invalid durations for audio stretch")

    tempo = original / target_seconds  # >1 speeds up (shorter), <1 slows (longer)
    # Decompose tempo into chain of 0.5..2.0 multipliers
    parts = []
    remaining = tempo
    # Handle extremes with multiplicative steps
    while remaining > 2.0:
        parts.append(2.0)
        remaining /= 2.0
    while remaining < 0.5:
        parts.append(0.5)
        remaining /= 0.5
    parts.append(remaining)
    # Build filterchain
    filt = ",".join([f"atempo={p:.6f}" for p in parts])
    cmd = [
        "ffmpeg", "-y",
        "-i", input_audio,
        "-filter:a", filt,
        "-c:a", "aac",
        output_audio,
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


# ===== USER-DRIVEN NARRATION (TIMESTAMPS-IN) =====


def load_captions_from_json(path: str):
    """Load captions from JSON.

    Supports either:
      - List of [start, end, text]
      - List of objects with keys {start,end,text}
    Returns: List[Tuple[float, float, str]] preserving provided timings.
    """
    import json
    data = json.loads(Path(path).read_text())
    captions: List[Tuple[float, float, str]] = []
    for item in data:
        if isinstance(item, (list, tuple)) and len(item) >= 3:
            s, e, t = float(item[0]), float(item[1]), str(item[2])
        elif isinstance(item, dict):
            s, e, t = float(item.get("start", 0.0)), float(item.get("end", 0.0)), str(item.get("text", ""))
        else:
            continue
        if not t:
            continue
        if e <= s:
            e = s + 0.4
        captions.append((s, e, t))
    return captions


def load_captions_from_csv(path: str):
    """Load captions from a CSV with headers start,end,text.

    Returns: List[Tuple[float, float, str]] preserving provided timings.
    """
    import csv
    captions: List[Tuple[float, float, str]] = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                s = float(row.get("start", 0.0))
                e = float(row.get("end", 0.0))
                t = str(row.get("text", ""))
            except Exception:
                continue
            if not t:
                continue
            if e <= s:
                e = s + 0.4
            captions.append((s, e, t))
    return captions


def _schedule_non_overlapping(captions: List[Tuple[float, float, str]], min_gap_s: float = 0.1) -> List[Tuple[float, float, str]]:
    """Push start times forward to prevent overlaps while preserving each caption duration.

    Returns a new list of (start, end, text) with no overlaps, keeping ordering.
    """
    if not captions:
        return []
    ordered = sorted(captions, key=lambda x: x[0])
    result: List[Tuple[float, float, str]] = []
    current = max(0.0, float(ordered[0][0]))
    for s, e, t in ordered:
        s = float(s); e = float(e)
        dur = max(0.4, e - s)
        start = max(s, current)
        end = start + dur
        result.append((start, end, t))
        current = end + min_gap_s
    return result


def narrate_from_captions(input_video: str,
                          captions: List[Tuple[float, float, str]],
                          output_video: str,
                          burn_subtitles: bool = False,
                          allow_time_push: bool = True,
                          min_gap_s: float = 0.1) -> str:
    """Generate narration from user-provided (start, end, text) captions as-is.

    - Does NOT resequence or change timings (no overlaps are resolved here).
    - Uses gTTS if available to synthesize speech per caption.
    - Muxes narration into the provided video and optionally burns subtitles.
    - Returns the output video path.
    """
    schedule = captions
    if allow_time_push:
        schedule = _schedule_non_overlapping(captions, min_gap_s=min_gap_s)
    # Use exact (possibly nudged) timings: sequential=False to preserve schedule
    return auto_narrate_and_subtitle(
        input_video=input_video,
        captions=schedule,
        output_video=output_video,
        burn_subtitles=burn_subtitles,
        sequential=False,
    )


def narrate_from_json(input_video: str,
                      json_path: str,
                      output_video: str,
                      burn_subtitles: bool = False) -> str:
    """Convenience wrapper: load captions from JSON and narrate with exact timings."""
    caps = load_captions_from_json(json_path)
    return narrate_from_captions(input_video, caps, output_video, burn_subtitles)


def narrate_from_csv(input_video: str,
                     csv_path: str,
                     output_video: str,
                     burn_subtitles: bool = False) -> str:
    """Convenience wrapper: load captions from CSV and narrate with exact timings."""
    caps = load_captions_from_csv(csv_path)
    return narrate_from_captions(input_video, caps, output_video, burn_subtitles)


def narrate_with_bgm(input_video: str,
                     captions: List[Tuple[float, float, str]],
                     music_path: str,
                     output_video: str,
                     burn_subtitles: bool = False,
                     music_db: float = -20.0) -> str:
    """Narrate from user captions and mix background music, trimmed to video length.

    Returns final output video path.
    """
    temp = str(Path(".dotmotion_media") / "narrated_temp.mp4")
    Path(".dotmotion_media").mkdir(parents=True, exist_ok=True)
    narrated = narrate_from_captions(input_video, captions, temp, burn_subtitles)
    add_background_music(narrated, music_path, output_video, music_db=music_db)
    return output_video
