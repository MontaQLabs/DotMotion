from manim import (Scene, VGroup, ORIGIN, UP, DOWN, LEFT, RIGHT, FadeIn, FadeOut,
                   Write, Create, Indicate, config, RoundedRectangle)
import dotmotion as dot


class DotmotionPitch(Scene):
    """90s pitch video: problem -> solution -> features -> credibility -> CTA."""

    def construct(self):
        config.background_color = dot.POLKADOT_BLACK

        # Title card
        title = dot.create_text("Dotmotion", font_size=64)
        subtitle = dot.create_text("Cinematic Polkadot Animations in Minutes",
                                   font_size=32, color=dot.POLKADOT_PINK)
        subtitle.next_to(title, DOWN, buff=0.5)
        manim_tag = dot.create_text("Manim-based library",
                                    font_size=24, color=dot.POLKADOT_STORM_200)
        manim_tag.next_to(subtitle, DOWN, buff=0.35)
        self.play(Write(title, run_time=1.2))
        self.play(Write(subtitle, run_time=0.9))
        self.play(Write(manim_tag, run_time=0.6))
        self.wait(0.6)
        self.play(FadeOut(title), FadeOut(subtitle), FadeOut(manim_tag))

        # Problem statement (dimmed)
        with dot.Phase(self, dim=True, clear_on_exit=True):
            dot.display_text_safely(self,
                                    "Explaining Polkadot is hard without visuals",
                                    position="center", font_size=34, bg=True, wait_time=1.6)
            dot.display_text_safely(self,
                                    "Generic tools look clunky. Timing and layout break.",
                                    position="center", font_size=28, bg=True, wait_time=1.4)

        # Solution card
        with dot.Phase(self, dim=False, clear_on_exit=False):
            headline = dot.create_text("Meet Dotmotion", font_size=56)
            tagline = dot.create_text("A purpose-built toolkit for Polkadot",
                                      font_size=30, color=dot.POLKADOT_STORM_200)
            tagline.next_to(headline, DOWN, buff=0.4)
            self.play(Write(headline, run_time=0.9))
            self.play(Write(tagline, run_time=0.8))
            self.wait(0.6)
        # Remove headline/tagline before starting visuals to avoid overlaps
        self.play(FadeOut(headline, run_time=0.4), FadeOut(tagline, run_time=0.4))

        # Quick demo: Relay + 3 parachains + premium XCM
        relay = dot.PolkadotRelay(radius=2.2, n_validators=8, name_position="above")
        self.play(Create(relay.ring, run_time=1.2))
        self.play(Write(relay.name, run_time=0.6), FadeIn(relay.validators, run_time=0.9, lag_ratio=0.1))
        # Parachains from registry
        reg = dot.load_chain_registry()
        mythos_name, _, mythos_color = dot.get_chain_theme("mythos", reg) or ("Mythos", None, dot.ACALA_COLOR)
        moonbeam_name, _, moonbeam_color = dot.get_chain_theme("moonbeam", reg) or ("Moonbeam", None, dot.MOONBEAM_COLOR)
        hydration_name, _, hydration_color = dot.get_chain_theme("hydration", reg) or ("Hydration", None, dot.ASTAR_COLOR)
        paras = [
            dot.Parachain(name=mythos_name, position=LEFT * 4.4 + UP * 1.2, color=mythos_color, radius=0.85),
            dot.Parachain(name=moonbeam_name, position=RIGHT * 4.4 + DOWN * 0.8, color=moonbeam_color, radius=0.85),
            dot.Parachain(name=hydration_name, position=RIGHT * 4.2 + UP * 1.7, color=hydration_color, radius=0.85),
        ]
        for p in paras:
            self.play(*relay.connect_parachain(p, animate=True), run_time=0.9)

        # Center logo
        logo = dot.load_logo("assets/polkadot-logo.svg")
        dot.center_logo_in_ring(relay.ring, logo, scale=0.42)
        self.play(FadeIn(logo, run_time=0.5))
        dot.push_above_ring(relay.name, relay.ring, buffer=0.38)
        dot.resolve_overlap(relay.name, logo, direction=UP, step=0.1, max_steps=16)

        # Feature bullets
        bullets = [
            "Collision-safe text and badges",
            "Premium XCM animations (curves, glow, particles)",
            "Registry-driven logos, names, and palettes",
            "Phase-based sequencing and auto-clean",
        ]
        for b in bullets:
            dot.display_text_safely(self, b, position="bottom", font_size=26, bg=True, margin=0.4, wait_time=0.9)

        # (Removed explicit Manim foundation caption per request)

        # Hide relay visuals to avoid overlap during math interlude
        if hasattr(relay, "connection_lines") and relay.connection_lines:
            self.play(*[FadeOut(l, run_time=0.25) for l in relay.connection_lines])
        self.play(FadeOut(logo), *[FadeOut(p) for p in paras], FadeOut(relay), run_time=0.5)

        # Tokenomics intro (no overlap with relay visuals)
        dot.display_text_safely(self,
                                "Tokenomics visuals for Polkadot & parachains",
                                position="center", font_size=30, bg=True, margin=0.4, wait_time=1.0)

        # Mathematical interlude: tokenomics curves (fallback if MathTex not available)
        from manim import Axes, ValueTracker, always_redraw, Dot as MDot
        axes = Axes(x_range=[0, 10, 1], y_range=[0, 1, 0.2], x_length=6, y_length=3)
        axes.move_to(ORIGIN + UP * 1.6)
        self.play(Create(axes), run_time=0.6)

        # Try to show a formula label (inflation decay); fallback to plain text
        formula_group = None
        latex_ok = True
        try:
            from manim import MathTex
            formula = MathTex(r"I(t) = I_0 e^{-k t} \quad\text{(inflation)}")
            formula.scale(0.7)
            formula.to_edge(UP, buff=0.6)
            formula_group = formula
        except Exception:
            latex_ok = False
            formula_group = dot.create_text("I(t) = I0 e^{-k t}  (inflation)", font_size=26, color=dot.POLKADOT_STORM_200)
            formula_group.to_edge(UP, buff=0.6)
        self.play(FadeIn(formula_group, run_time=0.5))

        import math
        k = ValueTracker(0.25)
        I0 = 1.0
        infl_curve = axes.plot(lambda x: I0 * math.exp(-k.get_value() * x), color=dot.POLKADOT_PINK)
        self.play(Create(infl_curve), run_time=0.8)
        # moving point on curve at x=t
        t = ValueTracker(0.0)
        moving = always_redraw(lambda: MDot(axes.coords_to_point(t.get_value(), I0 * math.exp(-k.get_value() * t.get_value())), radius=0.06, color=dot.POLKADOT_LIME))
        self.add(moving)
        self.play(t.animate.set_value(10), run_time=1.6)
        # Animate parameter change to show different inflation regimes
        self.play(k.animate.set_value(0.65), run_time=1.2)
        # Update curve by replacing with new sampled function
        new_curve = axes.plot(lambda x: I0 * math.exp(-k.get_value() * x), color=dot.POLKADOT_PINK)
        self.play(infl_curve.animate.become(new_curve), run_time=0.8)
        self.play(FadeOut(moving), FadeOut(infl_curve), FadeOut(formula_group), FadeOut(axes), run_time=0.5)

        # Matrix adjacency-like grid animation
        from manim import VGroup as MGroup
        # Matrix section: heatmap A and vector v, show A·v -> v' (Markov step)
        import random
        size = 5
        A = [[round(random.uniform(0.0, 1.0), 2) for _ in range(size)] for _ in range(size)]
        # normalize rows to sum to 1 for Markov-like interpretation
        for i in range(size):
            s = sum(A[i]) or 1.0
            A[i] = [a / s for a in A[i]]
        v = [1.0 / size] * size

        def color_for_value(x):
            # map 0..1 to storm->cyan
            return dot.POLKADOT_STORM_700 if x < 0.25 else (dot.POLKADOT_STORM_400 if x < 0.5 else (dot.POLKADOT_PINK if x < 0.75 else dot.POLKADOT_CYAN))

        grid = MGroup()
        cell_refs = []
        for i in range(size):
            row = MGroup()
            row_cells = []
            for j in range(size):
                val = A[i][j]
                cell = RoundedRectangle(width=0.5, height=0.5, corner_radius=0.06,
                                         color=color_for_value(val), fill_opacity=0.35, stroke_width=1)
                label = dot.create_text(f"{val:.2f}", font_size=16, color=dot.POLKADOT_WHITE)
                label.move_to(cell.get_center())
                # Fit text inside cell with padding
                max_label_w = cell.width * 0.82
                if label.width > max_label_w:
                    label.scale_to_fit_width(max_label_w)
                g = VGroup(cell, label)
                row.add(g)
                row_cells.append(g)
            row.arrange(RIGHT, buff=0.1)
            grid.add(row)
            cell_refs.append(row_cells)
        grid.arrange(DOWN, buff=0.1)
        grid.move_to(ORIGIN)

        # Vector v (as a column to the right)
        vec = MGroup()
        vec_cells = []
        for i in range(size):
            val = v[i]
            r = RoundedRectangle(width=0.5, height=0.5, corner_radius=0.06,
                                 color=color_for_value(val), fill_opacity=0.35, stroke_width=1)
            label = dot.create_text(f"{val:.2f}", font_size=16, color=dot.POLKADOT_WHITE)
            label.move_to(r.get_center())
            max_label_w = r.width * 0.82
            if label.width > max_label_w:
                label.scale_to_fit_width(max_label_w)
            g = VGroup(r, label)
            vec.add(g)
            vec_cells.append(g)
        vec.arrange(DOWN, buff=0.1)
        vec.next_to(grid, RIGHT, buff=0.7)

        # Result v' (to the right of v)
        res = MGroup()
        res_cells = []
        for i in range(size):
            r = RoundedRectangle(width=0.5, height=0.5, corner_radius=0.06,
                                 color=dot.POLKADOT_STORM_700, fill_opacity=0.12, stroke_width=1)
            label = dot.create_text("0.00", font_size=16, color=dot.POLKADOT_STORM_200)
            label.move_to(r.get_center())
            max_label_w = r.width * 0.82
            if label.width > max_label_w:
                label.scale_to_fit_width(max_label_w)
            g = VGroup(r, label)
            res.add(g)
            res_cells.append(g)
        res.arrange(DOWN, buff=0.1)
        res.next_to(vec, RIGHT, buff=0.7)

        # Optional label A v -> v'
        from manim import MathTex
        av_lbl = MathTex(r"v' = A\\, v").scale(0.8)
        # Ensure the MathTex label stays on one line and within frame
        av_lbl.next_to(grid, UP, buff=0.35)
        max_av_w = grid.width * 1.2
        if av_lbl.width > max_av_w:
            av_lbl.scale_to_fit_width(max_av_w)

        # Explanatory captions
        explain_top = dot.create_text("Transition matrix A (probabilities)", font_size=26, color=dot.POLKADOT_STORM_200)
        explain_top.to_edge(UP, buff=0.6)
        explain_bottom = dot.create_text("Multiply by state vector v to get next distribution v'", font_size=24, color=dot.POLKADOT_STORM_400)
        explain_bottom.to_edge(DOWN, buff=0.6)

        layout_group = VGroup(grid, vec, res, av_lbl)
        # Slightly reduce to avoid overflow
        layout_group.scale(1.05)
        layout_group.move_to(ORIGIN)
        self.play(FadeIn(layout_group, run_time=0.6), FadeIn(explain_top, run_time=0.5), FadeIn(explain_bottom, run_time=0.5))

        # Animate multiplication row by row
        import numpy as np
        A_np = np.array(A)
        v_np = np.array(v)
        res_np = A_np.dot(v_np)
        for i in range(size):
            # highlight row i
            self.play(*[cell_refs[i][j][0].animate.set_fill(dot.POLKADOT_LIME, opacity=0.45) for j in range(size)], run_time=0.2)
            # pulse vector
            self.play(*[vec_cells[j][0].animate.set_fill(dot.POLKADOT_PINK, opacity=0.45) for j in range(size)], run_time=0.2)
            # set result cell value
            val = float(res_np[i])
            # Update result label and fit inside the cell
            new_lbl = dot.create_text(f"{val:.2f}", font_size=16, color=dot.POLKADOT_WHITE)
            max_label_w = res_cells[i][0].width * 0.82
            if new_lbl.width > max_label_w:
                new_lbl.scale_to_fit_width(max_label_w)
            new_lbl.move_to(res_cells[i][0].get_center())
            res_cells[i][1].become(new_lbl)
            res_cells[i][0].set_fill(dot.POLKADOT_CYAN, opacity=0.45)
            self.wait(0.15)
            # unhighlight
            self.play(*[cell_refs[i][j][0].animate.set_fill(color_for_value(A[i][j]), opacity=0.35) for j in range(size)],
                      *[vec_cells[j][0].animate.set_fill(color_for_value(v[j]), opacity=0.35) for j in range(size)], run_time=0.2)

        self.play(FadeOut(layout_group), FadeOut(explain_top), FadeOut(explain_bottom), run_time=0.5)

        # Restore relay visuals for the XCM highlight
        self.play(FadeIn(relay), *[FadeIn(p) for p in paras], FadeIn(logo), run_time=0.5)

        # XCM highlight
        dim = dot.RoundedRectangle(width=config.frame_width * 1.1,
                                   height=config.frame_height * 1.1,
                                   corner_radius=0.1,
                                   fill_opacity=0.55,
                                   stroke_opacity=0,
                                   color=dot.BLACK)
        self.play(FadeIn(dim, run_time=0.3))
        xcm = dot.animate_xcm(self, paras[0], paras[1], xcm_type="transfer", message="XCM: Transfer", duration=1.7)
        self.play(FadeOut(xcm, run_time=0.25), FadeOut(dim, run_time=0.25))

        # Clean before CTA
        if hasattr(relay, "connection_lines") and relay.connection_lines:
            self.play(*[FadeOut(l, run_time=0.25) for l in relay.connection_lines])
        self.play(FadeOut(logo), *[FadeOut(p) for p in paras], FadeOut(relay), run_time=0.6)

        # CTA
        cta = dot.create_text("Tell your Polkadot story, beautifully.", font_size=40)
        self.play(Write(cta, run_time=0.9))
        self.wait(0.8)
        self.play(FadeOut(cta, run_time=0.6))

        # End card
        end = dot.create_text("Dotmotion", font_size=56)
        url = dot.create_text("github.com/montaq/DotMotion", font_size=28, color=dot.POLKADOT_STORM_200)
        url.next_to(end, DOWN, buff=0.4)
        self.play(Write(end, run_time=0.8))
        self.play(Write(url, run_time=0.6))
        self.wait(0.8)
        self.play(FadeOut(end), FadeOut(url), run_time=0.6)


if __name__ == "__main__":
    print("Run: manim -pqm dotmotion_pitch.py DotmotionPitch")

