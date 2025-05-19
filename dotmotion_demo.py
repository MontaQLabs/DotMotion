"""
Dotmotion Animation Demo

A premium, cinematic demonstration of the Dotmotion animation toolkit,
showcasing the Polkadot network architecture with professional visual quality.
"""

from manim import (Scene, config, ORIGIN, UP, DOWN, LEFT, RIGHT, FadeIn,
                   FadeOut, Write, Create, Indicate, VGroup, Dot,
                   RoundedRectangle, GrowFromCenter, BackgroundRectangle,
                   BLACK)
import dotmotion as dot
# Import colors directly to use in create_dot_pattern method
from dotmotion import (POLKADOT_PINK, POLKADOT_CYAN, POLKADOT_VIOLET,
                       POLKADOT_LIME)
import numpy as np

# Configure the scene for cinematic quality output
config.background_color = dot.POLKADOT_BLACK  # Official black background
config.frame_rate = 60
config.pixel_width = 1920
config.pixel_height = 1080
config.renderer = "cairo"  # Use cairo for better text rendering

# Constants for better layout
SCREEN_WIDTH = 14  # Coordinates width of the screen
SCREEN_HEIGHT = 8  # Coordinates height of the screen
TITLE_SCALE = 0.75  # Reduced title scaling (previously 0.85)
SUBTITLE_SCALE = 0.6  # Reduced subtitle scaling (previously 0.7)
SECTION_SPACING = 1.5  # Spacing between elements
ANIMATION_SPEED = 0.8  # Adjust global animation speed (< 1 is slower)

# Camera positions
CENTER = ORIGIN
TOP_SECTION = UP * 3.0
BOTTOM_SECTION = DOWN * 3.0

# Text display options
TEXT_DISPLAY_POSITION = DOWN * 2.5  # Default position for explanatory text
TEXT_OVERLAY_OPACITY = 0.8  # Opacity for text background overlay


class PolkadotOverview(Scene):
    """
    A comprehensive cinematic overview of the Polkadot network architecture
    """

    def construct(self):
        # Create the welcome screen
        self.welcome_screen()

        # Showcase the ecosystem architecture
        self.ecosystem_demo()

        # Clear the screen with a smooth transition
        self.smooth_clear()

        # Show validator staking mechanism
        self.staking_demo()

        # Clear the screen with a smooth transition
        self.smooth_clear()

        # Show cross-chain messaging system
        self.xcm_demo()

        # Clear the screen with a smooth transition
        self.smooth_clear()

        # Show governance system
        self.governance_demo()

        # Add ending credits
        self.ending_credits()

    def display_text_with_background(self,
                                     text,
                                     position=None,
                                     font_size=24,
                                     duration=2.0,
                                     dim_background=False):
        """
        Display text with a background to ensure readability
        
        Parameters:
            text: Text to display
            position: Optional position override (defaults to bottom of screen)
            font_size: Font size to use
            duration: How long to display the text
            dim_background: Whether to dim the entire background for better contrast
        """
        # Create text object
        text_obj = dot.create_text(text,
                                   font_size=font_size,
                                   color=dot.POLKADOT_WHITE)

        # Ensure text fits within screen
        if text_obj.width > SCREEN_WIDTH * 0.8:
            text_obj.scale_to_fit_width(SCREEN_WIDTH * 0.8)

        # Position text (default to bottom of screen if not specified)
        if position is not None:
            text_obj.move_to(position)
        else:
            text_obj.move_to(TEXT_DISPLAY_POSITION)

        # Create semi-transparent background for better readability
        bg_rect = BackgroundRectangle(text_obj,
                                      color=BLACK,
                                      fill_opacity=0.8,
                                      buff=0.4)

        text_group = VGroup(bg_rect, text_obj)

        # Optional full-screen dim for maximum contrast
        screen_dim = None
        if dim_background:
            screen_dim = RoundedRectangle(width=SCREEN_WIDTH * 1.2,
                                          height=SCREEN_HEIGHT * 1.2,
                                          corner_radius=0.1,
                                          fill_opacity=0.7,
                                          stroke_opacity=0,
                                          color=BLACK)
            self.play(FadeIn(screen_dim, run_time=0.5))

        # Show the text
        self.play(FadeIn(text_group, run_time=0.7))
        self.wait(duration)

        # Clean up
        self.play(FadeOut(text_group, run_time=0.7))
        if dim_background and screen_dim is not None:
            self.play(FadeOut(screen_dim, run_time=0.5))

        return text_group

    def welcome_screen(self):
        """Create an elegant welcome screen with the Polkadot logo and title"""
        # Create main title with reduced scale to prevent off-screen text
        title = self.create_title("The Polkadot Ecosystem",
                                  scale=1.0)  # Reduced from 1.2
        title.move_to(ORIGIN + UP * 0.5)  # Center and position title

        subtitle = self.create_subtitle("A Visual Journey",
                                        scale=0.9)  # Reduced from 1.0
        subtitle.next_to(title, DOWN, buff=0.6)  # Increased spacing

        # Add a decorative dot pattern inspired by Polkadot's visual identity
        dots = self.create_dot_pattern()

        # Show the elements with elegant animations
        self.play(Write(title, run_time=2.0),
                  FadeIn(dots, run_time=3.0, lag_ratio=0.05))
        self.play(Write(subtitle, run_time=1.5))
        self.wait(1)

        # Transition out
        self.play(FadeOut(title, run_time=1.0), FadeOut(subtitle,
                                                        run_time=1.0),
                  FadeOut(dots, run_time=1.5))

    def create_dot_pattern(self):
        """Create a decorative dot pattern that represents the network"""
        dots = VGroup()
        # Create a pattern of dots inspired by Polkadot's visual identity
        colors = [POLKADOT_PINK, POLKADOT_CYAN, POLKADOT_VIOLET, POLKADOT_LIME]

        # Generate dots in a grid pattern with some randomness
        n_dots = 40
        for i in range(n_dots):
            x = (np.random.random() - 0.5) * SCREEN_WIDTH * 0.9
            y = (np.random.random() - 0.5) * SCREEN_HEIGHT * 0.9
            size = np.random.uniform(0.02, 0.08)
            opacity = np.random.uniform(0.4, 0.9)
            color = colors[i % len(colors)]

            dot = Dot(point=[x, y, 0],
                      radius=size,
                      color=color,
                      fill_opacity=opacity)
            dots.add(dot)

        return dots

    def create_title(self, text, scale=1.0):
        """Create a title with the Polkadot font"""
        title = dot.create_text(text,
                                font_size=64 * scale,
                                color=dot.POLKADOT_WHITE)
        # Ensure title fits within screen
        if title.width > SCREEN_WIDTH * 0.8:
            title.scale_to_fit_width(SCREEN_WIDTH * 0.8)
        return title

    def create_subtitle(self, text, scale=1.0):
        """Create a stylish subtitle with the Polkadot font"""
        subtitle = dot.create_text(text,
                                   font_size=38 * scale,
                                   color=POLKADOT_PINK)
        # Ensure subtitle fits within screen
        if subtitle.width > SCREEN_WIDTH * 0.8:
            subtitle.scale_to_fit_width(SCREEN_WIDTH * 0.8)
        return subtitle

    def create_section_title(self, title_text, scale=TITLE_SCALE):
        """Helper to create consistent section titles"""
        return dot.create_text(title_text,
                               font_size=64 * scale,
                               color=dot.POLKADOT_WHITE)

    def create_section_subtitle(self, text, scale=SUBTITLE_SCALE):
        """Helper to create consistent section subtitles"""
        subtitle = dot.create_text(text,
                                   font_size=36 * scale,
                                   color=dot.POLKADOT_STORM_200)
        return subtitle

    def smooth_clear(self):
        """Clear the entire scene with a smooth fade transition"""
        if self.mobjects:  # Only try to clear if there are mobjects
            self.play(*[FadeOut(mob, run_time=1.2) for mob in self.mobjects],
                      run_time=dot.QUICK_FADE)
        else:
            # If no mobjects, just wait a moment
            self.wait(0.5)

    def ecosystem_demo(self):
        """Show the Polkadot network structure with elegant animations"""
        # Create section title and subtitle
        title = self.create_section_title("Polkadot Architecture")
        subtitle = self.create_section_subtitle(
            "The relay chain and parachain ecosystem")
        subtitle.next_to(title, DOWN, buff=0.4)

        title_group = VGroup(title, subtitle)

        # Introduction animation
        self.play(Write(title, run_time=1.5))
        self.play(Write(subtitle, run_time=1))
        self.wait(0.5)

        # Move titles to top and reduce size further to avoid overlap
        self.play(title_group.animate.scale(0.7).to_edge(UP, buff=0.8))

        # Fade out titles during complex animation sequences
        # This prevents text from overlapping with animations
        self.play(title_group.animate.set_opacity(0.2), run_time=0.8)

        # Create relay chain with a pulsing effect
        relay = dot.PolkadotRelay(radius=2.6, n_validators=8)
        relay.move_to(ORIGIN + UP * 0.2)

        # Add relay chain with a more dynamic animation
        self.play(Create(relay.ring, run_time=2.0))
        self.play(Write(relay.name, run_time=1.2),
                  FadeIn(relay.validators, run_time=1.5, lag_ratio=0.1))
        self.wait(0.5)

        # Define parachain positions in a more balanced layout
        # Using golden angle for more aesthetically pleasing distribution
        n_parachains = 5
        golden_angle = np.pi * (3 - np.sqrt(5))  # Golden angle ~137.5 degrees
        radius = 4.2  # Distance from center

        positions = []
        for i in range(n_parachains):
            angle = i * golden_angle
            pos = np.array([radius * np.cos(angle), radius * np.sin(angle), 0])
            positions.append(pos)

        # Create parachains with consistent colors from the palette
        parachains = [
            dot.Parachain(name="Acala",
                          position=positions[0],
                          color=dot.ACALA_COLOR,
                          radius=0.9),
            dot.Parachain(name="Moonbeam",
                          position=positions[1],
                          color=dot.MOONBEAM_COLOR,
                          radius=0.9),
            dot.Parachain(name="Astar",
                          position=positions[2],
                          color=dot.ASTAR_COLOR,
                          radius=0.9),
            dot.Parachain(name="Centrifuge",
                          position=positions[3],
                          color=dot.CENTRIFUGE_COLOR,
                          radius=0.9),
            dot.Parachain(name="Phala",
                          position=positions[4],
                          color=dot.PARALLEL_COLOR,
                          radius=0.9),
        ]

        # Connect parachains to relay chain with elegant animations
        for i, parachain in enumerate(parachains):
            # Slight delay between each parachain for better visual flow
            delay = i * 0.2

            # Get connection animations
            connection_anims = relay.connect_parachain(parachain, animate=True)

            # Play animations with staggered timing
            self.play(*connection_anims, run_time=1.5 + delay)

            # Emphasize each parachain briefly
            self.play(Indicate(parachain,
                               color=parachain.circle.get_color(),
                               scale_factor=1.1),
                      run_time=0.8)

            # Small pause between parachains
            if i < len(parachains) - 1:
                self.wait(0.3)

        # Add a visual pulse across the entire network to show connectivity
        self.pulse_network(relay, parachains)

        # Show block production on relay chain
        dot.animate_block_production(self, relay, n_blocks=3, duration=3.0)

        # Show connectivity from relay to parachains
        self.show_network_connectivity(relay, parachains)

        # Final pause
        self.wait(1)

    def pulse_network(self, relay, parachains):
        """Create a visual pulse across the network to show connectivity"""
        # Create temporary circles for the pulse effect
        pulse_circles = VGroup()

        # Add pulse at relay
        relay_pulse = Dot(radius=relay.radius,
                          color=POLKADOT_PINK,
                          fill_opacity=0.2,
                          stroke_width=0)
        relay_pulse.move_to(relay.get_center())
        pulse_circles.add(relay_pulse)

        # Add pulses at parachains
        for para in parachains:
            para_pulse = Dot(radius=para.radius,
                             color=para.circle.get_color(),
                             fill_opacity=0.2,
                             stroke_width=0)
            para_pulse.move_to(para.get_center())
            pulse_circles.add(para_pulse)

        # Animate the pulse
        self.play(
            *[p.animate.scale(1.5).set_opacity(0) for p in pulse_circles],
            run_time=2.0)

        # Remove the pulse objects
        self.remove(pulse_circles)

    def show_network_connectivity(self, relay, parachains):
        """Show the connectivity between relay and parachains"""
        # Create "data packets" (small dots) traveling along connections
        for para in parachains:
            # Create a small dot
            data_dot = Dot(radius=0.08, color=POLKADOT_PINK)
            data_dot.move_to(relay.get_center())

            # Create return dot
            return_dot = Dot(radius=0.08, color=para.circle.get_color())
            return_dot.move_to(para.get_center())

            # Animate dot moving from relay to parachain
            self.play(data_dot.animate.move_to(para.get_center()),
                      run_time=0.8)

            # Animate dot moving from parachain back to relay
            self.play(return_dot.animate.move_to(relay.get_center()),
                      run_time=0.8)

            # Remove dots
            self.remove(data_dot, return_dot)

    def staking_demo(self):
        """Show validator and nominator mechanics"""
        # Step 1: Clear introduction
        self.smooth_clear()

        # Use the improved text display method instead of overlapping titles
        self.display_text_with_background("Validation & Staking",
                                          position=ORIGIN,
                                          font_size=48,
                                          duration=2.0)

        self.display_text_with_background("How validators secure the network",
                                          position=ORIGIN,
                                          font_size=32,
                                          duration=1.5)

        # Step 3: Create background and validators
        background = self.create_validator_background()
        self.play(FadeIn(background, run_time=1.0))

        # Step 4: First show "Validators" title with background
        self.display_text_with_background("Validators",
                                          position=UP * 2.5,
                                          font_size=32,
                                          duration=1.0)

        # Step 5: Create spaced validators
        validators = VGroup()
        validator_spacing = 3.5  # More spacing
        validator_y_pos = UP * 0.5

        for i in range(4):
            position = validator_y_pos + RIGHT * (i - 1.5) * validator_spacing
            validator = dot.Validator(
                position=position,
                label=f"V{i+1}",  # Shorter label
                color=POLKADOT_VIOLET,
                size=0.65)
            validators.add(validator)

        # Show validators one at a time
        for i, validator in enumerate(validators):
            self.play(FadeIn(validator, run_time=0.8), run_time=0.7)

        # Add brief explanation with background
        self.display_text_with_background(
            "Process transactions & secure the network",
            position=ORIGIN,
            font_size=28,
            duration=1.5)

        # Step 6: Show "Nominators" title with background
        self.display_text_with_background("Nominators",
                                          position=UP * 2.5,
                                          font_size=32,
                                          duration=1.0)

        # Step 7: Create nominators with plenty of spacing
        nominators = VGroup()
        nominator_spacing = 4.5
        nominator_y_pos = DOWN * 2.0

        for i in range(3):
            position = nominator_y_pos + RIGHT * (i - 1) * nominator_spacing
            nominator = dot.Nominator(position=position,
                                      color=POLKADOT_CYAN,
                                      size=0.45)
            nominators.add(nominator)

        # Show nominators with staggered animation
        self.play(FadeIn(nominators, run_time=1.2, lag_ratio=0.2))

        # Add brief explanation with background
        self.display_text_with_background("Stake DOT to back validators",
                                          position=ORIGIN,
                                          font_size=28,
                                          duration=1.5)

        # Step 8: Show staking connections title
        self.display_text_with_background("Staking Connections",
                                          position=UP * 2.5,
                                          font_size=32,
                                          duration=1.0)

        # Connect nominators to validators, one connection at a time
        stakes = [250, 500, 150, 300]

        # First nominator connects to validators
        self.connect_stake(nominators[0], validators[0], stakes[0])
        self.wait(0.3)
        self.connect_stake(nominators[0], validators[1], stakes[1])
        self.wait(0.3)

        # Second nominator connects to validators
        self.connect_stake(nominators[1], validators[1], stakes[2])
        self.wait(0.3)
        self.connect_stake(nominators[1], validators[2], stakes[3])
        self.wait(0.3)

        # Third nominator connects to validators
        self.connect_stake(nominators[2], validators[2], stakes[0])
        self.wait(0.3)
        self.connect_stake(nominators[2], validators[3], stakes[2])
        self.wait(0.8)

        # Step 9: Show validator rewards title with background
        self.display_text_with_background("Validator Rewards",
                                          position=UP * 2.5,
                                          font_size=32,
                                          duration=1.0)

        # Show validator rewards without text overlap
        rewards = VGroup()
        for validator in validators:
            # Create a reward symbol (small glowing circle)
            reward = Dot(radius=0.25,
                         color=POLKADOT_LIME,
                         fill_opacity=0.8,
                         stroke_width=0)
            reward.move_to(validator.get_center())
            rewards.add(reward)

        # Animate rewards appearing one by one
        for reward in rewards:
            self.play(FadeIn(reward, scale=1.5, run_time=0.5), run_time=0.5)
            self.play(reward.animate.scale(0.6).set_opacity(0.3), run_time=0.5)

        self.play(FadeOut(rewards), run_time=0.7)

        # Step 10: Show validator rotation title with background
        self.display_text_with_background("Validator Rotation",
                                          position=UP * 2.5,
                                          font_size=32,
                                          duration=1.0)

        # Animate validator set change with no text overlap
        dot.animate_validator_set_change(self,
                                         validators,
                                         n_new=2,
                                         duration=2.5)
        self.wait(0.8)

        # Final explanation with dimmed background for emphasis
        self.display_text_with_background(
            "Validators are regularly rotated to maintain security",
            position=ORIGIN,
            font_size=28,
            duration=2.0,
            dim_background=True)

        # Final pause
        self.wait(1.0)

    def create_validator_background(self):
        """Create an elegant background for the validator section"""
        # Create a subtle grid pattern
        background = VGroup()

        # Add horizontal lines
        for y in np.arange(-3.5, 4.0, 0.7):
            line = dot.Line(LEFT * 6,
                            RIGHT * 6,
                            color=dot.POLKADOT_STORM_700,
                            stroke_width=0.5,
                            stroke_opacity=0.3)
            line.move_to([0, y, 0])
            background.add(line)

        # Add vertical lines
        for x in np.arange(-6, 6.5, 1.5):
            line = dot.Line(DOWN * 3.5,
                            UP * 3.5,
                            color=dot.POLKADOT_STORM_700,
                            stroke_width=0.5,
                            stroke_opacity=0.3)
            line.move_to([x, 0, 0])
            background.add(line)

        return background

    def connect_stake(self, nominator, validator, amount):
        """Connect a nominator to a validator with a stake amount"""
        connection = nominator.connect_to_validator(validator,
                                                    stake_amount=amount)

        # Create a more engaging animation for the connection
        if isinstance(connection, VGroup):
            line, text = connection
            self.play(Create(line, run_time=0.8))
            self.play(Write(text, run_time=0.6))
        else:
            self.play(Create(connection, run_time=0.8))

    def xcm_demo(self):
        """Show cross-chain messaging with clear separation of text and animations"""
        # ===== PHASE 1: INTRODUCTION =====
        # Clear everything first
        self.smooth_clear()

        # Show title by itself with background dimming for emphasis
        self.display_text_with_background("Cross-Chain Messaging",
                                          position=ORIGIN,
                                          font_size=48,
                                          duration=2.0,
                                          dim_background=True)

        # ===== PHASE 2: RELAY CHAIN =====
        # First, show an explanation of what we're going to see
        self.display_text_with_background(
            "The Relay Chain coordinates communication between parachains",
            position=ORIGIN,
            font_size=32,
            duration=2.0)

        # Create relay chain with ample space around it
        relay = dot.PolkadotRelay(radius=2.0, n_validators=6)
        relay.move_to(ORIGIN)

        # Show relay chain parts one at a time
        self.play(Create(relay.ring, run_time=1.5))
        self.play(Write(relay.name, run_time=0.8))
        self.play(FadeIn(relay.validators, run_time=1.2, lag_ratio=0.1))
        self.wait(0.8)

        # ===== PHASE 3: PARACHAIN 1 (ACALA) =====
        # Show text about first parachain with background
        self.display_text_with_background("Acala: A DeFi hub parachain",
                                          position=UP * 2.5,
                                          font_size=32,
                                          duration=1.5)

        # Create and connect first parachain - positioned far from center
        acala = dot.Parachain(name="Acala",
                              position=LEFT * 5.0 + DOWN * 0.5,
                              color=dot.ACALA_COLOR,
                              radius=1.2)

        acala_connection = relay.connect_parachain(acala, animate=False)
        self.play(Create(acala_connection), run_time=1.0)
        self.play(GrowFromCenter(acala), run_time=1.0)
        self.wait(0.8)

        # ===== PHASE 4: PARACHAIN 2 (MOONBEAM) =====
        # Show text about second parachain with background
        self.display_text_with_background(
            "Moonbeam: An EVM-compatible smart contract platform",
            position=UP * 2.5,
            font_size=32,
            duration=1.5)

        # Create and connect second parachain - positioned far from center on opposite side
        moonbeam = dot.Parachain(name="Moonbeam",
                                 position=RIGHT * 5.0 + DOWN * 0.5,
                                 color=dot.MOONBEAM_COLOR,
                                 radius=1.2)

        moonbeam_connection = relay.connect_parachain(moonbeam, animate=False)
        self.play(Create(moonbeam_connection), run_time=1.0)
        self.play(GrowFromCenter(moonbeam), run_time=1.0)
        self.wait(0.8)

        # ===== PHASE 5: XCM INTRODUCTION =====
        # Introduce XCM with background dimming for emphasis
        self.display_text_with_background(
            "Cross-Consensus Messaging (XCM)\n" +
            "Allows secure communication between different blockchains",
            position=ORIGIN,
            font_size=32,
            duration=2.5,
            dim_background=True)

        # ===== PHASE 6: TOKEN TRANSFER EXAMPLE =====
        # Show example 1 title with background
        self.display_text_with_background(
            "Example 1: Token Transfer\n" +
            "Transferring DOT tokens from Acala to Moonbeam",
            position=ORIGIN,
            font_size=32,
            duration=2.0)

        # Show token transfer animation with no overlapping text
        xcm_msg = dot.animate_cross_chain_transfer(self,
                                                   acala,
                                                   moonbeam,
                                                   message="Transfer DOT",
                                                   duration=2.0)

        # Show token reception
        self.show_token_received(moonbeam)
        self.wait(1.0)

        # Clean up message
        self.play(FadeOut(xcm_msg, run_time=0.7))

        # ===== PHASE 7: NFT TRANSFER EXAMPLE =====
        # Show example 2 title with background
        self.display_text_with_background(
            "Example 2: NFT Transfer\n" +
            "Transferring an NFT from Moonbeam to Acala",
            position=ORIGIN,
            font_size=32,
            duration=2.0)

        # Show NFT transfer animation
        xcm_msg = dot.animate_cross_chain_transfer(self,
                                                   moonbeam,
                                                   acala,
                                                   message="NFT #1337",
                                                   duration=2.0)

        # Show NFT reception
        self.show_nft_received(acala)
        self.wait(1.0)

        # Clean up message
        self.play(FadeOut(xcm_msg, run_time=0.7))

        # ===== PHASE 8: SMART CONTRACT EXAMPLE =====
        # Show example 3 title with background
        self.display_text_with_background(
            "Example 3: Smart Contract Call\n" +
            "Calling a Moonbeam smart contract from Acala",
            position=ORIGIN,
            font_size=32,
            duration=2.0)

        # Show smart contract call animation
        xcm_msg = dot.animate_cross_chain_transfer(self,
                                                   acala,
                                                   moonbeam,
                                                   message="execute(swap)",
                                                   duration=2.0)

        # Show contract execution
        self.show_contract_execution(moonbeam)
        self.wait(1.0)

        # Clean up message
        self.play(FadeOut(xcm_msg, run_time=0.7))

        # ===== PHASE 9: CONCLUSION =====
        # Final explanation about XCM benefits with background dimming
        self.display_text_with_background("Benefits of Cross-Chain Messaging",
                                          position=UP * 2.5,
                                          font_size=32,
                                          duration=1.5)

        # Show bullet points one by one with background
        points = [
            "• Enables truly composable multi-chain applications",
            "• Allows specialized chains to interact seamlessly",
            "• Creates a unified ecosystem of parachains"
        ]

        for point in points:
            self.display_text_with_background(point,
                                              position=ORIGIN,
                                              font_size=28,
                                              duration=1.5)

        # Final pause
        self.wait(1.0)

    def show_token_received(self, parachain):
        """Animate token reception at the destination parachain"""
        # Create token symbol
        token = dot.create_text("🪙", font_size=36, color=POLKADOT_PINK)
        token.move_to(parachain.get_center())

        # Animation for tokens appearing
        self.play(FadeIn(token, scale=1.5))
        self.play(token.animate.scale(0.8).shift(DOWN * 0.2), run_time=0.5)

        # Animation for token processing
        self.play(Indicate(parachain.circle,
                           color=POLKADOT_PINK,
                           scale_factor=1.1),
                  run_time=1.0)

        # Remove token
        self.play(FadeOut(token))

    def show_nft_received(self, parachain):
        """Animate NFT reception at the destination parachain"""
        # Create NFT symbol
        nft = dot.create_text("🐱", font_size=36, color=dot.MOONBEAM_COLOR)
        nft.move_to(parachain.get_center())

        # Animation for NFT appearing
        self.play(FadeIn(nft, scale=1.5))
        self.play(nft.animate.scale(0.8).shift(DOWN * 0.2), run_time=0.5)

        # Animation for NFT processing
        self.play(Indicate(parachain.circle,
                           color=dot.MOONBEAM_COLOR,
                           scale_factor=1.1),
                  run_time=1.0)

        # Remove NFT
        self.play(FadeOut(nft))

    def show_contract_execution(self, parachain):
        """Animate smart contract execution on the destination chain"""
        # Create code symbol
        code = dot.create_text("{ }", font_size=36, color=POLKADOT_LIME)
        code.move_to(parachain.get_center())

        # Animation for code appearing
        self.play(FadeIn(code, scale=1.5))

        # Animation for processing
        self.play(Indicate(parachain.circle,
                           color=POLKADOT_LIME,
                           scale_factor=1.1),
                  run_time=1.0)

        # Animation for execution result
        result = dot.create_text("✓", font_size=30, color=POLKADOT_LIME)
        result.next_to(code, RIGHT, buff=0.2)

        self.play(Write(result))
        self.wait(0.5)

        # Remove code and result
        self.play(FadeOut(code), FadeOut(result))

    def governance_demo(self):
        """Show Polkadot's on-chain governance system"""
        # ===== PHASE 1: INTRODUCTION =====
        # Clear everything first
        self.smooth_clear()

        # Show title and subtitle with background dimming for emphasis
        self.display_text_with_background("On-Chain Governance",
                                          position=ORIGIN + UP * 0.5,
                                          font_size=48,
                                          duration=1.5)

        self.display_text_with_background(
            "How Polkadot evolves through collective decision making",
            position=ORIGIN - UP * 0.5,
            font_size=32,
            duration=2.0,
            dim_background=True)

        # ===== PHASE 2: GOVERNANCE OVERVIEW =====
        # Show overview text with background
        self.display_text_with_background(
            "Governance Components\n" +
            "Three key components work together for decentralized decision making",
            position=ORIGIN,
            font_size=32,
            duration=2.0)

        # Create the governance background
        governance = dot.GovernanceSystem(position=ORIGIN,
                                          width=7.0,
                                          height=4.5)

        # Just show the background and title first
        self.play(FadeIn(governance.bg, run_time=1.2))
        self.play(Write(governance.title, run_time=1.0))
        self.wait(0.8)

        # ===== PHASE 3: COUNCIL COMPONENT =====
        # Show council title and description with background
        self.display_text_with_background(
            "Council\n" +
            "Elected representatives who propose improvements and filter spam",
            position=UP * 3.0,
            font_size=28,
            duration=2.0)

        # Show council component
        self.play(Create(governance.council, run_time=1.0))
        self.play(Write(governance.council_text, run_time=0.8))
        self.wait(0.8)

        # ===== PHASE 4: TECHNICAL COMMITTEE COMPONENT =====
        # Show technical committee title and description with background
        self.display_text_with_background(
            "Technical Committee\n" +
            "Technical experts who review changes and handle emergencies",
            position=UP * 3.0,
            font_size=28,
            duration=2.0)

        # Show technical committee component
        self.play(Create(governance.tech, run_time=1.0))
        self.play(Write(governance.tech_text, run_time=0.8))
        self.wait(0.8)

        # ===== PHASE 5: REFERENDUM COMPONENT =====
        # Show referendum title and description with background
        self.display_text_with_background(
            "Referendum\n" +
            "Token holders vote directly on proposals with stake-weighted voting",
            position=UP * 3.0,
            font_size=28,
            duration=2.0)

        # Show referendum component
        self.play(Create(governance.referendum, run_time=1.0))
        self.play(Write(governance.referendum_text, run_time=0.8))
        self.wait(0.8)

        # ===== PHASE 6: CONNECTION FLOW =====
        # Show connection title and description with background
        self.display_text_with_background(
            "Governance Flow\n" +
            "Proposals flow from Council/Tech Committee to Referendum",
            position=UP * 3.0,
            font_size=28,
            duration=2.0)

        # Create and show connections
        council_to_referendum = dot.Arrow(
            start=governance.council.get_bottom(),
            end=governance.referendum.get_top() + LEFT * 0.5,
            color=POLKADOT_PINK,
            buff=0.2,
            max_tip_length_to_length_ratio=0.15)

        tech_to_referendum = dot.Arrow(start=governance.tech.get_bottom(),
                                       end=governance.referendum.get_top() +
                                       RIGHT * 0.5,
                                       color=POLKADOT_CYAN,
                                       buff=0.2,
                                       max_tip_length_to_length_ratio=0.15)

        # Show connections one at a time
        self.play(Create(council_to_referendum, run_time=1.0))
        self.wait(0.5)
        self.play(Create(tech_to_referendum, run_time=1.0))
        self.wait(1.0)

        # ===== PHASE 7: PROPOSAL EXAMPLE =====
        # Show proposal title and description with background
        self.display_text_with_background(
            "Proposal Example\n" +
            "Following a proposal through the governance process",
            position=UP * 3.0,
            font_size=28,
            duration=2.0)

        # Create a proposal object
        proposal = dot.RoundedRectangle(width=1.2,
                                        height=0.5,
                                        corner_radius=0.1,
                                        color=POLKADOT_PINK,
                                        fill_opacity=0.6,
                                        stroke_width=2)
        proposal_text = dot.create_text("Prop #42",
                                        font_size=16,
                                        color=dot.POLKADOT_WHITE)
        proposal_text.move_to(proposal.get_center())

        proposal_group = VGroup(proposal, proposal_text)
        proposal_group.next_to(governance.council, LEFT, buff=1.5)

        # Step 1: Show proposal creation
        step1_text = dot.create_text(
            "Step 1: Council member creates a proposal",
            font_size=22,
            color=POLKADOT_PINK)
        step1_text.to_edge(UP, buff=0.7)
        self.play(Write(step1_text, run_time=1.0))
        self.wait(0.5)

        # Fade out text before animation
        self.play(FadeOut(step1_text, run_time=0.7))

        # Show proposal appearing
        self.play(FadeIn(proposal_group, scale=1.2, run_time=1.0))
        self.wait(0.8)

        # Step 2: Move to council
        step2_text = dot.create_text("Step 2: Council reviews the proposal",
                                     font_size=22,
                                     color=POLKADOT_PINK)
        step2_text.to_edge(UP, buff=0.7)
        self.play(Write(step2_text, run_time=1.0))
        self.wait(0.5)

        # Fade out text before animation
        self.play(FadeOut(step2_text, run_time=0.7))

        # Move proposal to council
        self.play(proposal_group.animate.move_to(
            governance.council.get_center()),
                  run_time=1.0)

        # Show council reviewing (highlight effect)
        self.play(Indicate(governance.council,
                           color=POLKADOT_PINK,
                           scale_factor=1.1),
                  run_time=1.0)
        self.wait(0.8)

        # Step 3: Move to referendum
        step3_text = dot.create_text(
            "Step 3: Proposal moves to referendum for voting",
            font_size=22,
            color=POLKADOT_PINK)
        step3_text.to_edge(UP, buff=0.7)
        self.play(Write(step3_text, run_time=1.0))
        self.wait(0.5)

        # Fade out text before animation
        self.play(FadeOut(step3_text, run_time=0.7))

        # Move proposal along the arrow path to referendum
        path_points = [
            governance.council.get_bottom(),
            governance.council.get_bottom() + DOWN * 0.5,
            governance.referendum.get_top() + UP * 0.5,
            governance.referendum.get_center()
        ]

        # Create a path animation along the points
        for i in range(len(path_points) - 1):
            self.play(proposal_group.animate.move_to(path_points[i + 1]),
                      run_time=0.7)

        self.wait(0.8)

        # Step 4: Voting process
        step4_text = dot.create_text(
            "Step 4: Token holders vote on the referendum",
            font_size=22,
            color=POLKADOT_PINK)
        step4_text.to_edge(UP, buff=0.7)
        self.play(Write(step4_text, run_time=1.0))
        self.wait(0.5)

        # Fade out text before animation
        self.play(FadeOut(step4_text, run_time=0.7))

        # Show voting happening
        vote_yes = dot.create_text("YES: 67%",
                                   font_size=18,
                                   color=POLKADOT_LIME)
        vote_no = dot.create_text("NO: 33%",
                                  font_size=18,
                                  color=dot.POLKADOT_STORM_400)

        # Position votes to the right side to avoid overlap
        vote_yes.move_to(RIGHT * 3.5 + UP * 0.2)
        vote_no.next_to(vote_yes, DOWN, buff=0.3)

        # Show votes appearing
        self.play(Write(vote_yes, run_time=0.8))
        self.play(Write(vote_no, run_time=0.8))

        # Show vote counting up animation
        for i in range(3):
            self.play(vote_yes.animate.become(
                dot.create_text(f"YES: {58 + 3*i}%",
                                font_size=18,
                                color=POLKADOT_LIME).move_to(
                                    vote_yes.get_center())),
                      vote_no.animate.become(
                          dot.create_text(
                              f"NO: {42 - 3*i}%",
                              font_size=18,
                              color=dot.POLKADOT_STORM_400).move_to(
                                  vote_no.get_center())),
                      run_time=0.6)

        # Show final vote tally
        self.play(vote_yes.animate.set_color(POLKADOT_LIME).scale(1.2),
                  vote_no.animate.set_opacity(0.5),
                  run_time=0.8)

        # Show checkmark for approval
        checkmark = dot.create_text("✓", font_size=36, color=POLKADOT_LIME)
        checkmark.next_to(proposal_group, RIGHT, buff=0.2)
        self.play(Write(checkmark, run_time=0.8))
        self.wait(1.0)

        # Clean up voting elements
        self.play(FadeOut(vote_yes),
                  FadeOut(vote_no),
                  FadeOut(checkmark),
                  run_time=0.8)

        # Step 5: Implementation
        step5_text = dot.create_text(
            "Step 5: Approved proposal is automatically implemented",
            font_size=22,
            color=POLKADOT_LIME)
        step5_text.to_edge(UP, buff=0.7)
        self.play(Write(step5_text, run_time=1.0))
        self.wait(0.5)

        # Fade out text before animation
        self.play(FadeOut(step5_text, run_time=0.7))

        # Show implementation effect
        self.play(proposal_group.animate.set_color(POLKADOT_LIME),
                  Indicate(governance.bg,
                           color=POLKADOT_LIME,
                           scale_factor=1.02),
                  run_time=1.5)
        self.wait(0.8)

        # ===== PHASE 8: CONCLUSION =====
        # Show conclusion title and bullet points with background
        self.display_text_with_background("Benefits of On-Chain Governance",
                                          position=UP * 2.5,
                                          font_size=32,
                                          duration=1.5)

        # Show bullet points one by one with background
        points = [
            "• Enables forkless runtime upgrades",
            "• Allows the network to evolve without hard forks",
            "• Gives stakeholders direct control over the protocol"
        ]

        for point in points:
            self.display_text_with_background(point,
                                              position=ORIGIN,
                                              font_size=28,
                                              duration=1.5)

        # Final pause
        self.wait(1.0)

    def ending_credits(self):
        """Create elegant ending credits with no overlapping"""
        # First clear everything
        self.smooth_clear()
        self.wait(0.5)

        # Create decorative background
        dots = self.create_dot_pattern()
        self.play(FadeIn(dots, run_time=2.0, lag_ratio=0.05))

        # Show title with background dimming for emphasis
        self.display_text_with_background("Thanks for Watching",
                                          position=ORIGIN,
                                          font_size=48,
                                          duration=2.0,
                                          dim_background=True)

        # Show toolkit info with background
        self.display_text_with_background(
            "Created with Dotmotion Animation Toolkit",
            position=ORIGIN,
            font_size=32,
            duration=2.0)

        # Show website info with background
        self.display_text_with_background("polkadot.network",
                                          position=ORIGIN,
                                          font_size=32,
                                          duration=2.0)

        # Final pause
        self.wait(1.0)


if __name__ == "__main__":
    print("Run this with: manim -pqh dotmotion_demo.py PolkadotOverview")
    print("For higher quality: manim -pql dotmotion_demo.py PolkadotOverview")
