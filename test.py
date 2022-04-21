import os
import sys

import glfw
import OpenGL.GL as gl
import imgui
from imgui.integrations.glfw import GlfwRenderer

active = {"window": True, "child": False, "tooltip": False, "menu bar": False, "popup": False, "popup modal": False,
    "popup context item": False, "popup context window": False, "drag drop": False, "group": False, "tab bar": False,
    "list box": False, "popup context void": False, "table": False, }
path_to_font = None  # "path/to/font.ttf"

opened_state = True


# Frame commands from the video
def frame_commands():
    io = imgui.get_io()
    if io.key_ctrl and io.keys_down[glfw.KEY_Q]:
        sys.exit(0)

    if imgui.begin_main_menu_bar():
        if imgui.begin_menu("File"):
            clicked, selected = imgui.menu_item("Quit", "Ctrl+Q")
            if clicked:
                sys.exit(0)
            imgui.end_menu()
        imgui.end_main_menu_bar()

    with imgui.begin("A Window!"):
        if imgui.button("select"):
            imgui.open_popup("select-popup")

        try:
            with imgui.begin_popup("select-popup") as popup:
                if popup.opened:
                    imgui.text("Select one")
                    raise Exception
        except Exception:
            print("caught exception and no crash!")


def render_frame(impl, window, font):
    glfw.poll_events()
    impl.process_inputs()
    imgui.new_frame()

    gl.glClearColor(0.1, 0.1, 0.1, 1)
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)

    if font is not None:
        imgui.push_font(font)
    frame_commands()
    if font is not None:
        imgui.pop_font()

    imgui.render()
    impl.render(imgui.get_draw_data())
    glfw.swap_buffers(window)


def impl_glfw_init():
    width, height = 1600, 900
    window_name = "minimal ImGui/GLFW3 example"

    if not glfw.init():
        print("Could not initialize OpenGL context")
        sys.exit(1)

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)

    window = glfw.create_window(int(width), int(height), window_name, None, None)
    glfw.make_context_current(window)

    if not window:
        glfw.terminate()
        print("Could not initialize Window")
        sys.exit(1)

    return window


def main():
    imgui.create_context()
    window = impl_glfw_init()

    impl = GlfwRenderer(window)

    io = imgui.get_io()
    jb = io.fonts.add_font_from_file_ttf(path_to_font, 30) if path_to_font is not None else None
    impl.refresh_font_texture()

    while not glfw.window_should_close(window):
        render_frame(impl, window, jb)

    impl.shutdown()
    glfw.terminate()


if __name__ == "__main__":
    main()
