from manim import *
import numpy as np

class PosicionDespEspacio(MovingCameraScene, VectorScene):

    def setup(self):
        MovingCameraScene.setup(self)
        VectorScene.setup(self)
    
    def construct(self):
        
        # Creamos el sistema de referencia
        sr = Axes(x_range=(0, 5), y_range=(0, 5)).add_coordinates()
        sr_text = Text('¡Sistema de referencia!', font_size=35).to_edge(DL).shift(DOWN)

        # Animamos SR y y su texto y movemos la camara
        self.camera.frame.save_state()
        self.play(Create(sr), run_time=2)
        self.wait()
        self.play(self.camera.frame.animate.move_to((0, -1, 0)))
        self.play(Create(sr_text), run_time=2)
        self.wait(0.3)
        self.play(Restore(self.camera.frame))
        self.play(self.camera.frame.animate.move_to((1, 0, 0)).set(width=sr.width*1.5))
        self.wait()
        
        # Creamos vectores de posicion
        # Origen del sistema de referencia
        sr_origin = sr.get_origin()
        
        # Puntos P, Q, texto y vectores
        p = Dot(sr.c2p(2, 3)) # !!!!
        p_text = MathTex(r"P").next_to(p,RIGHT)
        v_p = Arrow(sr_origin, p.get_center(), buff=0, stroke_width=2.5, tip_length=0.2)
        v_p_text = MathTex(r"\vec{r_{P}}").next_to(p, 2 * LEFT + 4 * DOWN)
        
        q = Dot(sr.c2p(4, 2))
        q_text = MathTex(r"Q").next_to(q,RIGHT)
        v_q = Arrow(sr_origin, q.get_center(), buff=0, stroke_width=2.5, tip_length=0.2)
        v_q_text = MathTex(r"\vec{r_{Q}}").next_to(q, 4 * LEFT + 4 * DOWN)
        
        # Animate
        self.play(Create(p), Write(p_text))
        self.wait()
        self.play(Create(q), Write(q_text))
        self.wait()
        self.play(Create(v_p))
        self.play(Write(v_p_text))
        self.wait()
        self.play(Create(v_q))
        self.play(Write(v_q_text))
        self.wait(2)
        
        # Borramos algunos elementos y hacemos zoom
        vectors = VGroup(v_p, v_q, v_p_text, v_q_text)
        self.play(FadeOut(vectors))
        self.wait(2)
        self.play(self.camera.frame.animate.move_to((0, 0, 0)).set(width=sr.width*1.1))
        self.wait()

        # Trayectoria 1, grado 1
        def func1(x):
            return -0.5*x + 4

        graph1 = sr.plot(func1, color=BLUE_B)
        text_graph1 = MathTex(r"T_{1}", color=BLUE_B)
        text_graph1.shift([5.75, -0.75, 0])
        
        # Trayectoria 2, grado 2
        def func2(x):
            return 0.5*x**2 - 3.5*x + 8

        graph2 = sr.plot(func2, color=GREEN_B)
        text_graph2 = MathTex(r"T_{2}", color=GREEN_B)
        text_graph2.shift([5.75, 1.5, 0])
        
        # Trayectoria 3, seno
        def func3(x):
            return np.sin(np.pi/4*x) + 2

        graph3 = sr.plot(func3, color=RED_B)
        text_graph3 = MathTex(r"T_{3}", color=RED_B)
        text_graph3.shift([5.75, -2, 0])

        # Representamos las trayectorias
        self.add(sr, graph1, text_graph1)
        self.play(Create(graph1), Write(text_graph1), runtime=2)
        self.wait()
        
        self.add(sr, graph2, text_graph2)
        self.play(Create(graph2), Write(text_graph2), runtime=2)
        self.wait()
        
        self.add(sr, graph3, text_graph3)
        self.play(Create(graph3), Write(text_graph3), runtime=2)
        self.wait(2)
        
        # Representamos un objeto moviendose en cada trayectoria
        # Trayectoria 1
        t1 = ValueTracker(0)
        initial_point = [sr.coords_to_point(t1.get_value(), func1(t1.get_value()))]

        dot1 = Dot(point=initial_point, color=BLUE, radius=0.1)
        dot1.add_updater(lambda x: x.move_to(sr.c2p(t1.get_value(), func1(t1.get_value()))))
        
        v_1 = Arrow(sr_origin, dot1.get_center(), buff=0, stroke_width=2.5, tip_length=0.2)
        v_1.add_updater(lambda x: x.put_start_and_end_on(sr_origin, dot1.get_center()))
        
        self.add(sr, dot1, v_1)
        self.play(t1.animate.set_value(5), run_time=5)
        self.wait()
        self.play(FadeOut(v_1))
        self.wait(2)

        # Trayectoria 2
        t2 = ValueTracker(0)
        initial_point = [sr.coords_to_point(t2.get_value(), func2(t2.get_value()))]

        dot2 = Dot(point=initial_point, color=GREEN, radius=0.1)
        dot2.add_updater(lambda x: x.move_to(sr.c2p(t2.get_value(), func2(t2.get_value()))))
        
        v_2 = Arrow(sr_origin, dot2.get_center(), buff=0, stroke_width=2.5, tip_length=0.2)
        v_2.add_updater(lambda x: x.put_start_and_end_on(sr_origin, dot2.get_center()))
        
        self.add(sr, dot2, v_2)
        self.play(t2.animate.set_value(5), run_time=5)
        self.wait()
        self.play(FadeOut(v_2))
        self.wait(2)
        
        # Trayectoria 3
        t3 = ValueTracker(5)
        initial_point = [sr.coords_to_point(t3.get_value(), func3(t3.get_value()))]

        dot3 = Dot(point=initial_point, color=RED, radius=0.1)
        dot3.add_updater(lambda x: x.move_to(sr.c2p(t3.get_value(), func3(t3.get_value()))))
        
        v_3 = Arrow(sr_origin, dot3.get_center(), buff=0, stroke_width=2.5, tip_length=0.2)
        v_3.add_updater(lambda x: x.put_start_and_end_on(sr_origin, dot3.get_center()))
        
        self.add(sr, dot3, v_3)
        self.play(t3.animate.set_value(0), run_time=5)
        self.wait()
        self.play(FadeOut(v_3))
        self.wait(2)
        
        # Marcamos el espacio recorrido en cada trayectoria
        space1 = sr.plot(func1, x_range=[2, 4], color=YELLOW_C)
        space2 = sr.plot(func2, x_range=[2, 4], color=YELLOW_C)
        space3 = sr.plot(func3, x_range=[2, 4], color=YELLOW_C)
        spaces = VGroup(space1, space2, space3)
        
        self.add(sr, spaces)
        self.play(Create(spaces), runtime=2)
        self.wait()
        # self.add(sr, space1)
        # self.play(Create(space1), runtime=2)
        # self.wait()
        # self.add(sr, space2)
        # self.play(Create(space2), runtime=2)
        # self.wait()
        
        # Borramos las trayectorias completas y los desplazamientos
        trayectorias = VGroup(graph1, graph2, graph3, 
                              dot1, dot2, dot3,
                              space1, space2, space3,
                              text_graph1, 
                              text_graph2, 
                              text_graph3)
        self.play(FadeOut(trayectorias))
        self.wait(2)
        
        # # Borramos los desplazamientos
        # spaces = VGroup(space1, space2, space3)
        # self.play(FadeOut(spaces))
        # self.wait(2)
        
        # Nombramos los desplazamientos
        space1 = sr.plot(func1, x_range=[2, 4], color=BLUE_C)
        s1_text = MathTex(r"\Delta s_{1}", color=BLUE_C)
        s1_text.shift([2, -0.5, 0])
        space_text1 = VGroup(space1, s1_text)
        
        space2 = sr.plot(func2, x_range=[2, 4], color=GREEN_C)
        s2_text = MathTex(r"\Delta s_{2}", color=GREEN_C)
        s2_text.shift([2, -1, 0])
        space_text2 = VGroup(space2, s2_text)
        
        space3 = sr.plot(func3, x_range=[2, 4], color=RED_C)
        s3_text = MathTex(r"\Delta s_{3}", color=RED_C)
        s3_text.shift([2, 0.5, 0])
        space_text3 = VGroup(space3, s3_text)
        
        self.play(Create(space_text1))
        self.wait(2)
        self.play(Create(space_text2))
        self.wait(2)
        self.play(Create(space_text3))
        self.wait(2)
        
        # Borramos los desplazamientos
        spaces = VGroup(space_text1, space_text2, space_text3)
        self.play(FadeOut(spaces))
        self.wait(2)
        
        # Volvemos a mostrar los vectores de posicion 
        # ahora con subindice inicial y final
        r_i = Arrow(sr_origin, p.get_center(), buff=0, stroke_width=2.5, tip_length=0.2)
        r_i_text = MathTex(r"\vec{r_{i}}").next_to(r_i.get_center())
        
        r_f = Arrow(sr_origin, q.get_center(), buff=0, stroke_width=2.5, tip_length=0.2)
        r_f_text = MathTex(r"\vec{r_{f}}").next_to(r_f.get_center(), DOWN * 0.5)
        
        self.play(Create(r_i), Write(r_i_text))
        self.wait()
        self.play(Create(r_f), Write(r_f_text))
        self.wait(2)
        
        # Alejamos la camara
        self.remove(sr_text)
        self.play(self.camera.frame.animate.move_to((-1, -1, 0)).set(width=sr.width*2))
        self.play(FadeOut(VGroup(p, p_text, q, q_text, r_i, r_i_text)))
        self.wait()
        
        # Mostramos regla del paralelogramo para la resta
        # Vectores
        menos_r_i = Arrow(sr_origin, sr.c2p(-2, -3), buff=0, stroke_width=2.5, tip_length=0.2)
        menos_r_i_text = MathTex(r"\vec{-r_{i}}").next_to(menos_r_i.get_center())
        
        menos_r_i_prima = Line(sr.c2p(4, 2), sr.c2p(2, -1), buff=0, stroke_width=2.5, tip_length=0.2, color=RED)
        # menos_r_i_prima_text = MathTex(r"\vec{-r_{i}'}").next_to(menos_r_i_prima.get_center())
        
        menos_r_f_prima = Line(sr.c2p(-2, -3), sr.c2p(2, -1), buff=0, stroke_width=2.5, tip_length=0.2, color=RED)
        # menos_r_f_prima_text = MathTex(r"\vec{r_{f}'}").next_to(menos_r_f_prima.get_center(), DOWN*0.5)
        
        # self.play(FadeOut(VGroup(r_i, r_i_text)))
        self.play(Create(VGroup(menos_r_i, menos_r_i_text)), run_time=2)
        self.wait()
        self.play(Create(menos_r_i_prima), run_time=0.7)
        self.wait()
        self.play(Create(menos_r_f_prima), run_time=0.7)
        self.wait()
        
        # Vector desplazamiento
        desp = Arrow(sr_origin, sr.c2p(2, -1), buff=0, stroke_width=6, tip_length=0.3, color=BLUE)
        desp_text = MathTex(r"\Delta \vec{r} = \vec{r_f} - \vec{r_i}", color=BLUE).next_to(desp.get_center(), 4 *DOWN + 7.5*RIGHT)
        
        self.play(Create(desp), run_time=3)
        self.wait()
        self.play(Write(desp_text))
        self.wait(2)
        
        # Borramos vectores y recuperamos los originales
        self.play(FadeOut(VGroup(menos_r_i, menos_r_i_text, menos_r_i_prima, menos_r_f_prima)))
        self.wait()
        self.play(Create(VGroup(p, p_text, q, q_text, r_i, r_i_text)), run_time=4)
        # self.play(Create(VGroup(r_i, r_i_text)))
        self.wait(2)
        
        
        # Movemos el vector a la posición original
        desplazamiento = VGroup(desp, desp_text)
        desplazamiento.generate_target()
        desplazamiento.target.shift(r_i.get_vector())
        self.play(MoveToTarget(desplazamiento))
        self.wait(2)
        desp_text_new = MathTex(r"\boldsymbol{\Delta \vec{r} = \vec{r_f} - \vec{r_i} = \vec{d}}", color=BLUE).next_to(desp.get_center(), 4 *DOWN + 7.5*RIGHT)
        self.play(Transform(desp_text, desp_text_new))
        self.wait(4)
