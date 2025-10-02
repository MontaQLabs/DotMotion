from manim import (Scene, ORIGIN, UP, DOWN, LEFT, RIGHT, FadeIn, FadeOut,
                   Write, Create, Indicate, VGroup, config)
import numpy as np
import dotmotion as dot


class OneMinutePolkadot(Scene):
    """~60s polished overview using assets and overlap-safe text."""

    def construct(self):
        # Title (minimal)
        title = dot.create_text("Polkadot", font_size=56)
        subtitle = dot.create_text("A Multi-Chain Network",
                                   font_size=28, color=dot.POLKADOT_PINK)
        subtitle.next_to(title, DOWN, buff=0.6)
        self.play(Write(title, run_time=1.2))
        self.play(Write(subtitle, run_time=0.8))
        self.wait(0.6)
        self.play(FadeOut(title), FadeOut(subtitle))

        # PHASE 1: Ecosystem core
        relay = dot.PolkadotRelay(radius=2.4, n_validators=8, name_position="above")
        self.play(Create(relay.ring, run_time=1.2, rate_func=lambda t: t*t*(3-2*t)))
        self.play(Write(relay.name, run_time=0.7))
        self.play(FadeIn(relay.validators, run_time=0.9, lag_ratio=0.12))

        # Parachains from registry themes
        registry = dot.load_chain_registry()
        mythos_name, _, mythos_color = dot.get_chain_theme("mythos", registry) or ("Mythos", None, dot.ACALA_COLOR)
        moonbeam_name, _, moonbeam_color = dot.get_chain_theme("moonbeam", registry) or ("Moonbeam", None, dot.MOONBEAM_COLOR)
        hydration_name, _, hydration_color = dot.get_chain_theme("hydration", registry) or ("Hydration", None, dot.ASTAR_COLOR)

        paras = [
            dot.Parachain(name=mythos_name, position=LEFT * 4.6 + UP * 1.4, color=mythos_color, radius=0.9),
            dot.Parachain(name=moonbeam_name, position=RIGHT * 4.6 + DOWN * 1.0, color=moonbeam_color, radius=0.9),
            dot.Parachain(name=hydration_name, position=RIGHT * 4.4 + UP * 1.9, color=hydration_color, radius=0.9),
        ]
        paras_group = VGroup(*paras)
        for p in paras:
            self.play(*relay.connect_parachain(p, animate=True), run_time=1.0)
            self.play(Indicate(p, color=p.circle.get_color(), scale_factor=1.05), run_time=0.5)

        # Brand mark (SVG in assets) using helper
        logo = dot.load_logo("assets/polkadot-logo.svg")
        dot.center_logo_in_ring(relay.ring, logo, scale=0.45)
        self.play(FadeIn(logo, run_time=0.7))

        # Ensure label sits fully above the ring edge and avoid logo overlap
        dot.push_above_ring(relay.name, relay.ring, buffer=0.38)
        dot.resolve_overlap(relay.name, logo, direction=UP, step=0.1, max_steps=16)
        dot.clamp_to_frame(relay.name, margin=0.2)

        # Ensure ring/validators render cleanly around the logo
        try:
            relay.ring.set_z_index(1)
            relay.validators.set_z_index(2)
            logo.set_z_index(3)
            relay.name.set_z_index(4)
        except Exception:
            self.bring_to_front(relay.ring, relay.validators, logo, relay.name)

        # Now create and place badges outside each circle along outward vector
        badges = VGroup()
        badge_dirs = []
        for p, cid in zip(paras, ["mythos", "moonbeam", "hydration"]):
            badge = dot.make_badge_from_registry(cid, layout="horizontal", max_width=1.5)
            pc = p.get_center()
            dir_vec = (pc / (np.linalg.norm(pc) + 1e-6))
            badge.next_to(p, dir_vec, buff=0.38)
            badge.shift(dir_vec * 0.2)
            dot.resolve_overlap(badge, logo, direction=dir_vec, step=0.12, max_steps=20)
            dot.resolve_overlap(badge, relay.name, direction=dir_vec, step=0.12, max_steps=20)
            dot.clamp_to_frame(badge, margin=0.2)
            badges.add(badge)
            badge_dirs.append(dir_vec)
        # Resolve inter-badge collisions
        for i in range(len(badges)):
            for j in range(i + 1, len(badges)):
                dot.resolve_overlap(badges[j], badges[i], direction=badge_dirs[j], step=0.12, max_steps=20)
        self.play(FadeIn(badges, run_time=0.6, lag_ratio=0.15))

        # Non-overlapping explanatory text
        avoid = [relay, *paras, logo, badges]
        dot.display_text_safely(self,
                                "Relay chain coordinates security and messaging",
                                avoid=avoid,
                                position="bottom",
                                font_size=28,
                                bg=True,
                                wait_time=1.2)

        # PHASE 2: XCM example with background dimming for focus
        dim = dot.RoundedRectangle(width=config.frame_width * 1.1,
                                   height=config.frame_height * 1.1,
                                   corner_radius=0.1,
                                   fill_opacity=0.65,
                                   stroke_opacity=0,
                                   color=dot.BLACK)
        self.play(FadeIn(dim, run_time=0.4))
        xcm = dot.animate_xcm(self, paras[0], paras[1], xcm_type="transfer", message="XCM: Transfer", duration=1.8)
        self.play(FadeOut(xcm, run_time=0.3))
        self.play(FadeOut(dim, run_time=0.3))

        dot.display_text_safely(self,
                                "XCM enables secure cross-chain communication",
                                avoid=avoid,
                                position="bottom",
                                font_size=28,
                                bg=True,
                                margin=0.4,
                                wait_time=1.2)

        # PHASE 4: Transition — clear all elements and end
        if hasattr(relay, "connection_lines") and relay.connection_lines:
            self.play(*[FadeOut(l, run_time=0.3) for l in relay.connection_lines])
        self.play(FadeOut(logo), FadeOut(paras_group), FadeOut(badges), FadeOut(relay), run_time=0.7)

        # PHASE 5: Ending — fully clear the scene before final card
        if self.mobjects:
            self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.7)

        # Ending
        thanks = dot.create_text("Thanks for Watching", font_size=48)
        self.play(Write(thanks, run_time=0.8))
        self.wait(0.7)
        self.play(FadeOut(thanks, run_time=0.6))


if __name__ == "__main__":
    print("Run: manim -pqm examples/one_min_demo.py OneMinutePolkadot")


