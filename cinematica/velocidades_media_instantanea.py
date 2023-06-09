from manim import *
import numpy as np
import sympy as sym
from scipy.linalg import norm

class Velocidades(MovingCameraScene, VectorScene):

    def setup(self):
        MovingCameraScene.setup(self)
        VectorScene.setup(self)
    
    def construct(self):
        
        # Creamos el sistema de referencia
        sr = Axes(x_range=(0, 5), y_range=(0, 5)).add_coordinates()

        # Plantamos el sistema de referencia
        self.camera.frame.save_state()
        self.play(Create(sr), run_time=2)
        self.wait()
        
        # Puntos P, Q
        p = Dot(sr.c2p(1, 3))
        p_text = MathTex(r"P").next_to(p,RIGHT)

        q = Dot(sr.c2p(4, 2))
        q_text = MathTex(r"Q").next_to(q,1.3*LEFT)
  
        # Animate
        self.play(Create(p), Write(p_text))
        self.wait()
        self.play(Create(q), Write(q_text))
        self.wait()
        
        # Definimos una serie de trayectorias
        # Trayectoria 1, parabola + seno
        def func1(x):
            return 1/3*x**2 - 2*x + 14/3 + 1/16*np.sin(3*np.pi*x)

        traj1 = sr.plot(func1, x_range=[1, 4], color=BLUE_B)
        text_traj1 = MathTex(r"T_{1}", color=BLUE_B)
        text_traj1.shift([2, -1.5, 0])
        
        self.play(Create(traj1), Write(text_traj1), runtime=2)
        self.wait()

        # Trayectoria 2, parabola + seno
        def func2(x):
            return -2/3*x**2 + 3*x + 2/3 + 1/10*np.sin(2*np.pi*x)

        traj2 = sr.plot(func2, x_range=[1, 4], color=GREEN_B)
        text_traj2 = MathTex(r"T_{2}", color=GREEN_B)
        text_traj2.shift([3, 1, 0])
        
        self.play(Create(traj2), Write(text_traj2), runtime=2)
        self.wait()

        # Representamos un objeto moviendose en cada trayectoria
        # Trayectoria 1
        t1 = ValueTracker(1)
        initial_point = [sr.coords_to_point(t1.get_value(), func1(t1.get_value()))]

        dot1 = Dot(point=initial_point, color=BLUE, radius=0.1)
        dot1.add_updater(lambda x: x.move_to(sr.c2p(t1.get_value(), func1(t1.get_value()))))
        
        # Trayectoria 2
        t2 = ValueTracker(1)
        initial_point = [sr.coords_to_point(t2.get_value(), func2(t2.get_value()))]

        dot2 = Dot(point=initial_point, color=GREEN, radius=0.1)
        dot2.add_updater(lambda x: x.move_to(sr.c2p(t2.get_value(), func2(t2.get_value()))))
        
        # Tiempos
        t0_text = MathTex(r"t_0").next_to(p,LEFT)
        tf_text = MathTex(r"t_f").next_to(q,0.75*DOWN + 0.25*RIGHT)
        
        # Animamos al mismo tiempo
        dots = VGroup(dot1, dot2)
        self.add(sr, dots)
        self.play(Write(t0_text), run_time=2)
        self.wait()
        times = AnimationGroup(t1.animate.set_value(4), t2.animate.set_value(4))
        self.play(times, run_time=8)
        self.play(Write(tf_text))
        self.wait(2)
    
        # Calculamos el espacio recorrido
        # Para ello usamos la integral del arco
        # Trayectoria 1
        # x = sym.Symbol('x', real=True) 
        # f1 = 1/3*x**2 - 2*x + 14/3 + 1/16*sym.sin(3*sym.pi*x)
        # d_f1 = sym.diff(f1)
        # curva1 = sym.root(1 * sym.Abs(d_f1)**2, 2)
        # I_exacta_curva1 = float(sym.integrate(curva1, (x, 1, 4)))
        I_exacta_curva1 = 1.92822265625
        print(I_exacta_curva1)
        
        # Trayectoria 2
        # x = sym.Symbol('x', real=True) 
        # f2 = -2/3*x**2 + 3*x + 2/3 + 1/10*sym.sin(2*sym.pi*x)
        # d_f2 = sym.diff(f2)
        # curva2 = sym.root(1 * sym.Abs(d_f2)**2, 2)
        # I_exacta_curva2 = float(sym.integrate(curva2, (x, 1, 4)))
        I_exacta_curva2 = 3.2833251953125
        print(I_exacta_curva2)

        # Movemos la camara
        self.play(self.camera.frame.animate.move_to((4, 2, 0)).set(width=sr.width*2))
        self.wait()
        
        # Ceamos dos lineas rectas en las que se van 
        # a convertir las trayectorias iniciales
        def f_recta1(x):
            return 7
        
        def f_recta2(x):
            return 6

        recta1 = sr.plot(f_recta1, x_range=[6, 6 + I_exacta_curva1], color=BLUE, stroke_width=4)
        text_recta1 = MathTex(r"\Delta s_{1}", color=BLUE).next_to(recta1, UP + 3 * LEFT)
        recta2 = sr.plot(f_recta2, x_range=[6, 6 + I_exacta_curva2], color=GREEN, stroke_width=4)
        text_recta2 = MathTex(r"\Delta s_{2}", color=GREEN).next_to(recta2, UP + 3 * LEFT)

        # FadeOut some elements
        initial_elements = VGroup(p, q, p_text, q_text, 
                                  text_traj1, text_traj2, 
                                  t0_text, tf_text,
                                  dots)
        
        self.play(FadeOut(initial_elements), run_time=0.5)
        
        # Transformar curvas en recta
        self.add(traj1, traj2)
        self.play(Transform(traj1, recta1), Write(text_recta1), run_time=3)
        self.wait()
        self.play(Transform(traj2, recta2), Write(text_recta2), run_time=3)
        self.wait()
        
        # Movemos la camara
        self.play(self.camera.frame.animate.move_to((13, 5, 0)).set(width=sr.width*1.25))
        self.wait(1.5)
        
        # Animamos los puntos
        # Trayectoria 1
        t1 = ValueTracker(6)
        initial_point = [sr.coords_to_point(t1.get_value(), f_recta1(t1.get_value()))]

        dot1 = Dot(point=initial_point, color=BLUE, radius=0.1)
        dot1.add_updater(lambda x: x.move_to(sr.c2p(t1.get_value(), f_recta1(t1.get_value()))))
        
        # Trayectoria 2
        t2 = ValueTracker(6)
        initial_point = [sr.coords_to_point(t2.get_value(), f_recta2(t2.get_value()))]

        dot2 = Dot(point=initial_point, color=GREEN, radius=0.1)
        dot2.add_updater(lambda x: x.move_to(sr.c2p(t2.get_value(), f_recta2(t2.get_value()))))
        
        # Tiempos
        t0_text = MathTex(r"t_0").next_to(p,LEFT)
        tf_text = MathTex(r"t_f").next_to(q,0.75*DOWN + 0.25*RIGHT)
        
        # Animamos al mismo tiempo
        dots = VGroup(dot1, dot2)
        self.add(sr, dots)
        self.wait()
        times = AnimationGroup(t1.animate.set_value(6 + I_exacta_curva1), 
                               t2.animate.set_value(6 + I_exacta_curva2))
        self.play(times, run_time=6)
        self.wait()
        
        # Quitamos puntos
        self.play(FadeOut(dots))
        self.wait()
        
        # Movemos la camara
        self.play(self.camera.frame.animate.move_to((14, 7, 0)).set(width=sr.width*1.25))
        self.wait(2)
        
        # Animamos formulas
        formula1 = MathTex(r"v \propto  \Delta s").scale(1.25)
        formula1.shift([19, 9, 0])
        formula2 = MathTex(r"v \propto \frac{1}{t_f - t_0}").scale(1.25)
        formula2.shift([19, 7, 0])
        formula3 = MathTex(r"v \propto \frac{1}{\Delta t}").scale(1.25)
        formula3.shift([19, 7, 0])
        
        self.play(Write(formula1))
        self.wait(3)
        self.play(Write(formula2))
        self.wait(2)
        self.play(Transform(formula2, formula3))
        self.wait(2)
        
        rectangle = Rectangle(height=3.7, width=5, color=ORANGE)
        rectangle.shift([19, 7.7, 0])
        self.play(Create(rectangle))
        self.wait(4)
        
        # Representar la formula final de la velocidad
        formula4 = MathTex(r"v_m = \frac{\Delta s}{\Delta t}").scale(1.25)
        formula4.shift([19, 7.75, 0])
        formula5 = MathTex(r"v_m = \frac{s_f - s_0}{t_f - t_0}").scale(1.25)
        formula5.shift([19, 7.75, 0])
        rectangle_2 = Rectangle(height=2.7, width=4.5, color=ORANGE)
        rectangle_2.shift([19, 7.7, 0])
        
        self.play(FadeOut(VGroup(formula2, formula1)))
        self.play(Create(formula4), run_time=2)
        self.play(Transform(rectangle, rectangle_2))
        self.wait(2)
        self.play(Transform(formula4, formula5))
        self.wait(3)
        
        # FadeOut elements y mover camara
        self.play(self.camera.frame.animate.move_to((7, 5, 0)).set(width=sr.width*3), run_time=2)
        self.play(FadeOut(formula4, rectangle, traj1, traj2, text_recta1, text_recta2))
        self.play(self.camera.frame.animate.move_to((0, 0, 0)).set(width=sr.width*1.2), run_time=2)
        self.wait(2)
        
        # Recuperate elements
        traj = sr.plot(func2, x_range=[1, 4], color=GREEN_B)
        text_traj = MathTex(r"T", color=GREEN_B)
        text_traj.shift([3, 1, 0])
        
        new_elements = VGroup(p, q, traj, t0_text, tf_text) 
        
        self.play(FadeIn(new_elements), run_time=3)
        self.wait(3)
       
        # Aproximamos por segmentos los espacios recorridos
        seg1 = Line(sr.c2p(1, func2(1)), sr.c2p(2, func2(2)), buff=0, stroke_width=2.5, color=YELLOW)
        seg2 = Line(sr.c2p(2, func2(2)), sr.c2p(3, func2(3)), buff=0, stroke_width=2.5, color=YELLOW)
        seg3 = Line(sr.c2p(3, func2(3)), sr.c2p(4, func2(4)), buff=0, stroke_width=2.5, color=YELLOW)
        text_seg1 = MathTex(r"\Delta s_1", color=YELLOW).next_to(seg1.get_center(), 0.3*DOWN).scale(0.75)
        text_seg2 = MathTex(r"\Delta s_2", color=YELLOW).next_to(seg2.get_center(), 0.5*DOWN).scale(0.75)
        text_seg3 = MathTex(r"\Delta s_3", color=YELLOW).next_to(seg3.get_center(), 0.5*DOWN).scale(0.75)
        segments = VGroup(seg1, text_seg1, seg2, text_seg2, seg3, text_seg3)
        
        self.play(Create(segments), run_time=3)
        self.wait(4)
        
        # Nos centramos en uno de los segmentos
        segments = VGroup(seg2, text_seg2, seg3, text_seg3)
        self.play(FadeOut(segments), run_time=2)
        self.wait()
        
        # Creamos un punto final y un tiempo final nuevos
        q_new = Dot(sr.c2p(2, func2(2)))
        tf_text_new = MathTex(r"t_f").next_to(q_new.get_center(), UP*0.5)
        self.play(Transform(VGroup(q, tf_text), VGroup(q_new, tf_text_new), 
                            replace_mobject_with_target_in_scene=True))
        self.wait(2)
        
        # Movemos camara
        self.play(self.camera.frame.animate.move_to((-2, 1, 0)).set(width=sr.width*0.5), run_time=2)
        self.wait(2)
        
        # Escalamos puntos y texto para que se vea mejor
        # y borramos elementos
        self.play(
            FadeOut(text_seg1),
            p.animate.scale(0.5),
            q_new.animate.scale(0.5),
            t0_text.animate.scale(0.5),
            tf_text_new.animate.scale(0.5)
        )
        self.wait()
        
        # Calculamos la velocidad inicial
        # Suponemos que tarda 2 segundos.
        # Asumimos velocidad constante en todo el recorrido
        t_total = 2
        def calcular_desplazamiento(r_inicio, r_final):
            return (r_final - r_inicio)
        
        def calcular_modulo_velocidad(r_inicio, r_final, t_total):
            return norm(calcular_desplazamiento(r_inicio, r_final) / t_total)

        v_modulo = calcular_modulo_velocidad(p.get_center(), q.get_center(), t_total)
        
        # Trasladamos el vector a el punto P
        def trasladar_y_calcular_extremos(p_inicio, vector):
            p_inicio = p_inicio
            p_final = p_inicio + vector
            return (p_inicio, p_final)
        
        def update_velocidad_media(r_inicio, r_final, v_modulo):
            desp = calcular_desplazamiento(r_inicio, r_final)
            v_director_desp = desp / norm(desp)
            v_media = v_director_desp * v_modulo
            return trasladar_y_calcular_extremos(r_inicio, v_media)[1]
        
        v_punto_inicio, v_punto_final = trasladar_y_calcular_extremos(
                                                                    p.get_center(), 
                                                                    update_velocidad_media(
                                                                        p.get_center(), 
                                                                        q_new.get_center(), 
                                                                        v_modulo))
        v_media = Arrow(v_punto_inicio, v_punto_final, 
                        buff=0, stroke_width=1.5, tip_length=0.1, color=RED)
        v_media_text = MathTex(r"\vec{v_m}", color=RED).next_to(v_media.get_center(), LEFT*0.5 + UP*1.5).scale(0.5)

        # Creamos un updater para el punto y el segmento asociados
        tracker = ValueTracker(2)
        q_new.add_updater(lambda x: x.move_to(sr.c2p(tracker.get_value(), func2(tracker.get_value()))))
        tf_text_new.add_updater(lambda x: x.next_to(q_new.get_center(), UP*0.5))
        seg1.add_updater(lambda x: x.put_start_and_end_on(p.get_center(), q_new.get_center()))
        v_media.add_updater(
            lambda x: x.put_start_and_end_on(
                p.get_center(),
                update_velocidad_media(
                    p.get_center(), q_new.get_center(), v_modulo
                    )
                )
            )
        v_media_text.add_updater(lambda x: x.next_to(v_media.get_center(), LEFT*0.5 + UP*0.7))
        
        # Animate the vector and segments
        self.add(tracker, seg1, tf_text_new, v_media, v_media_text)
        self.play(FadeIn(v_media, v_media_text))
        self.wait()
        self.play(tracker.animate.set_value(1.05), run_time=6)
        self.wait()
        
        # Quitamos algunos elementos
        self.play(FadeOut(seg1, q_new, t0_text, tf_text_new))
        self.wait()
        
        # Zoom in
        self.play(self.camera.frame.animate.move_to((-3, 1.1, 0)).set(width=sr.width*0.25), run_time=2)
        self.wait(3)
        
        # Transform velocidad
        v_instantanea_text = MathTex(r"\vec{v}", color=RED).next_to(v_media.get_center(), LEFT*0.5 + UP*0.5).scale(0.5)
        self.play(Transform(v_media_text, v_instantanea_text),
                  replace_mobject_with_target_in_scene=True)
        self.wait()

        # Zoom out
        self.play(self.camera.frame.animate.move_to((0, 1, 0)).set(width=sr.width*0.9), run_time=2)
        self.wait()
        
        # Aumentamos tamaño de los elementos
        v_media.scale(1)
        v_media_text.scale(1)
        self.wait()
        
        # Animamos la velocidad como tangente al desplazamiento
        # Para ello modificamos ligeramente los updaters
        # Creamos un updater para el punto y el segmento asociados.
        tracker2 = ValueTracker(1)
        ds = 0.1
        p.add_updater(lambda x: x.move_to(sr.c2p(tracker2.get_value(), func2(tracker2.get_value()))))
        v_media.clear_updaters()
        v_media_text.clear_updaters()
        v_media.add_updater(
            lambda x: x.put_start_and_end_on(
                p.get_center(),
                update_velocidad_media(
                    p.get_center(), 
                    sr.c2p(tracker2.get_value() + ds, func2(tracker2.get_value() + ds)), 
                    v_modulo
                    )
                )
            )
        v_media_text.add_updater(lambda x: x.next_to(v_media.get_center(), LEFT*0.5 + UP*0.7))
        
        # Animate the vector and segments
        v_media.scale(1)
        v_media_text.scale(1)
        self.play(tracker2.animate.set_value(4), run_time=8)
        self.wait(4)
        
        
       
        
        