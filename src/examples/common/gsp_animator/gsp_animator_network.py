# stdlib imports
import io
import os
import __main__

# pip imports
import numpy as np
import matplotlib.pyplot
import matplotlib.image
import matplotlib.animation

# local imports
import gsp_sc
from gsp_sc.core import canvas
from .gsp_animator_types import GSPAnimatorFunc

__dirname__ = os.path.dirname(os.path.abspath(__file__))


class GspAnimatorNetwork:
    """
    Animator for GSP scenes using a network renderer and matplotlib for display.

    Note: this requires a running GSP server. See the README for instructions.
    Note: it uses pip matplotlib, not the GSP matplotlib renderer.
    """

    def __init__(
        self,
        network_renderer: gsp_sc.renderer.network.NetworkRenderer,
        target_fps: int = 30,
        video_path: str | None = None,
        video_writer: str | None = None,
    ):
        self._network_renderer = network_renderer
        self._target_fps = target_fps
        self._video_path = video_path
        self._video_writer: str | None = None

        # guess the video writer from the file extension if not provided
        if self._video_path is not None:
            if video_writer is not None:
                self._video_writer = video_writer
            else:
                video_ext = os.path.splitext(self._video_path)[1].lower()
                if video_ext in [".mp4", ".m4v", ".mov"]:
                    self._video_writer = "ffmpeg"
                elif video_ext in [".gif", ".apng", ".webp"]:
                    self._video_writer = "pillow"
                else:
                    raise ValueError(f"Unsupported video format: {video_ext}")

    def animate(self, canvas: gsp_sc.core.Canvas, camera: gsp_sc.core.Camera, animator_callbacks: list[GSPAnimatorFunc]):
        """
        Animate the given canvas and camera using the provided callbacks to update visuals.
        """

        # create a matplotlib figure of the right size
        figure = matplotlib.pyplot.figure(frameon=False, dpi=canvas.dpi)
        figure.set_size_inches(canvas.width / canvas.dpi, canvas.height / canvas.dpi)

        # get the only axes in the figure
        mpl_axes = figure.add_axes((0, 0, 1, 1))

        # create an np.array to hold the image
        image_data_np = np.zeros((canvas.height, canvas.width, 3), dtype=np.uint8)
        axes_image = mpl_axes.imshow(image_data_np)

        # detect if we are in not interactive mode - used during testing
        gsp_sc_interactive = "GSP_SC_INTERACTIVE" not in os.environ or os.environ["GSP_SC_INTERACTIVE"] != "False"
        screenshot_saved = False

        # function called at each animation frame
        def mpl_animate(frame_index: int):
            nonlocal screenshot_saved

            # notify all animator callbacks
            changed_visuals: list[gsp_sc.core.VisualBase] = []
            for animator_callback in animator_callbacks:
                _changed_visuals = animator_callback()
                changed_visuals.extend(_changed_visuals)

            # render the scene to get the new image
            image_png_data = self._network_renderer.render(canvas, camera)
            image_data_io = io.BytesIO(image_png_data)
            image_data_np = matplotlib.image.imread(image_data_io, format="png")

            # update the image data
            axes_image.set_data(image_data_np)

            # if we are not in interactive mode, save a preview image and return
            if gsp_sc_interactive is False:
                # get the main script name
                main_script_name = os.path.basename(__main__.__file__) if hasattr(__main__, "__file__") else "interactive"
                main_script_basename = os.path.splitext(main_script_name)[0]
                # buid the output image path
                image_path = os.path.join(__dirname__, "../../output", f"{main_script_basename}_animator.png")
                image_path = os.path.abspath(image_path)
                # save image_png_data in a image file
                with open(image_path, "wb") as image_file:
                    image_file.write(image_png_data)
                # mark the screenshot as saved
                screenshot_saved = True
                # log the event
                print(f"Saved animation preview image to: {image_path}")
                anim.event_source.stop()
                return []

            # return the changed mpl artists
            changed_mpl_artists = [axes_image]
            return changed_mpl_artists

        # =============================================================================
        # Initialize the animation
        # =============================================================================
        anim = matplotlib.animation.FuncAnimation(figure, mpl_animate, frames=100, interval=1000.0 / self._target_fps)
        # save the animation if a path is provided
        if self._video_path is not None:
            anim.save(self._video_path, writer=self._video_writer, fps=self._target_fps)

        # =============================================================================
        # if not interactive, wait for the screenshot to be saved, and then close the figure
        # =============================================================================
        if gsp_sc_interactive is False:

            def close_figure_if_screenshot():
                nonlocal screenshot_saved
                if screenshot_saved is False:
                    return
                # Stop the animation and close the figure
                print("Screenshot saved, now closing the figure")
                mpl_timer.stop()
                matplotlib.pyplot.close(figure)

            mpl_timer = figure.canvas.new_timer(interval=500)
            mpl_timer.add_callback(close_figure_if_screenshot)
            mpl_timer.start()

        # show the animation
        matplotlib.pyplot.show()
