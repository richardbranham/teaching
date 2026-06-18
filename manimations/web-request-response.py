from manim import *

class WebRequestFlow(Scene):
    def construct(self):
        # Create nodes
        browser = Rectangle(width=3, height=1.5, color=BLUE).shift(3*LEFT + 1*UP)
        browser_text = Text("User's Browser").move_to(browser.get_center())
        internet = Ellipse(width=5, height=3, color=GREEN).shift(0.5*UP)
        internet_text = Text("Internet").move_to(internet.get_center())
        server = Rectangle(width=3, height=1.5, color=RED).shift(3*RIGHT + 1*UP)
        server_text = Text("Web Server").move_to(server.get_center())
        response_area = Rectangle(width=4, height=1.5, color=YELLOW).shift(3*LEFT + 2.5*DOWN)
        response_text = Text("Page Rendered in Browser").scale(0.6).move_to(response_area.get_center())

        # Draw initial objects
        self.play(Create(browser), Write(browser_text))
        self.wait(0.5)
        self.play(Create(internet), Write(internet_text))
        self.wait(0.5)
        self.play(Create(server), Write(server_text))
        self.wait(0.5)
        self.play(Create(response_area), Write(response_text))
        self.wait(0.5)

        # Arrow: Browser -> Internet (Request)
        arrow_req = Arrow(
            start=browser.get_right() + UP*0.2,
            end=internet.get_left() + DOWN*0.2,
            buff=0.1,
            color=BLUE
        )
        req_label = Text("Request").scale(0.5).next_to(arrow_req, UP)
        self.play(GrowArrow(arrow_req), Write(req_label))
        self.wait(1)

        # Arrow: Internet -> Server (Request)
        arrow_req2 = Arrow(
            start=internet.get_right() + DOWN*0.1,
            end=server.get_left() + UP*0.1,
            buff=0.1,
            color=BLUE
        )
        self.play(GrowArrow(arrow_req2))
        self.wait(1)

        # Pause at server to show processing
        processing = Text("Processing Request...", color=RED).scale(0.7).next_to(server, DOWN)
        self.play(Write(processing))
        self.wait(1.5)
        self.play(FadeOut(processing))

        # Arrow: Server -> Internet (Response)
        arrow_res = Arrow(
            start=server.get_left() + UP*0.2,
            end=internet.get_right() + DOWN*0.2,
            buff=0.1,
            color=YELLOW
        )
        res_label = Text("Response").scale(0.5).next_to(arrow_res, UP)
        self.play(GrowArrow(arrow_res), Write(res_label))
        self.wait(1)

        # Arrow: Internet -> Browser (Response)
        arrow_res2 = Arrow(
            start=internet.get_left() + DOWN*0.1,
            end=browser.get_right() + UP*0.1,
            buff=0.1,
            color=YELLOW
        )
        self.play(GrowArrow(arrow_res2))
        self.wait(1)

        # Animate page rendering
        render_text = Text("Rendering page...").scale(0.7).next_to(browser, DOWN)
        self.play(Write(render_text))
        self.wait(2)
        self.play(FadeOut(render_text))

        # Final highlight around the browser box to show page is ready
        glow = SurroundingRectangle(browser, color=YELLOW, buff=0.2)
        self.play(Create(glow))
        self.wait(2)
        self.play(FadeOut(glow))

        # Fade out everything
        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )
