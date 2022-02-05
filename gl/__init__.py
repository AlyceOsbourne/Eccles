import moderngl_window as mglw


class GameWindow(mglw.WindowConfig):
    gl_version = (3, 3)
    window_size = (1920, 1080)

    def render(self, time, frametime):
        pass

    def close(self):
        self.wnd.close()


mglw.run_window_config(GameWindow)

while True:
    pass  # todo write thread manager and make engine wait for kill event
