# stdlib imports
import os
import __main__


# pip imports
import matplotlib.pyplot
import matplotlib.animation
import matplotlib.artist

# local imports
import gsp
import gsp_matplotlib
from .gsp_animator_types import GSPAnimatorFunc

__dirname__ = os.path.dirname(os.path.abspath(__file__))


class GspAnimatorMatplotlib:
    """
    Animator for GSP scenes using a matplotlib renderer.
    """

    def __init__(
        self,
        matplotlib_renderer: gsp_matplotlib.MatplotlibRenderer,
        target_fps: int = 30,
        video_path: str | None = None,
        video_writer: str | None = None,
    ):
        self._matplotlib_renderer = matplotlib_renderer
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

    def animate(self, canvas: gsp.core.Canvas, camera: gsp.core.Camera, animator_callbacks: list[GSPAnimatorFunc]):
        """
        Animate the given canvas and camera using the provided callbacks to update visuals.
        """
        # render once to get the image size
        self._matplotlib_renderer.render(canvas, camera)

        def mpl_animate(frame_index: int) -> list[matplotlib.artist.Artist]:
            # notify all animator callbacks
            changed_visuals: list[gsp.core.VisualBase] = []
            for callback in animator_callbacks:
                _changed_visuals = callback()
                changed_visuals.extend(_changed_visuals)

            # convert all changed visuals to mpl artists
            changed_mpl_artists: list[matplotlib.artist.Artist] = []
            for visual in changed_visuals:
                mpl_artist = self._get_mpl_artists(canvas, visual)
                changed_mpl_artists.append(mpl_artist)

            # return the changed mpl artists
            return changed_mpl_artists

        figure = matplotlib.pyplot.gcf()

        # detect if we are in not interactive mode - used during testing
        gsp_sc_interactive = "GSP_SC_INTERACTIVE" not in os.environ or os.environ["GSP_SC_INTERACTIVE"] != "False"

        # if we are not in interactive mode, save a preview image and return
        if gsp_sc_interactive == False:
            # get the main script name
            main_script_name = os.path.basename(__main__.__file__) if hasattr(__main__, "__file__") else "interactive"
            main_script_basename = os.path.splitext(main_script_name)[0]
            # buid the output image path
            image_path = os.path.join(__dirname__, "../../output", f"{main_script_basename}_animator.png")
            image_path = os.path.abspath(image_path)
            # save the current figure in a image file
            figure.savefig(image_path)
            # log the event
            print(f"Saved animation preview image to: {image_path}")
            return

        # =============================================================================
        # Initialize the animation
        # =============================================================================
        anim = matplotlib.animation.FuncAnimation(figure, mpl_animate, frames=100, interval=1000.0 / self._target_fps)
        # save the animation if a path is provided
        if self._video_path is not None:
            anim.save(self._video_path, writer=self._video_writer, fps=self._target_fps)

        # show the animation
        matplotlib.pyplot.show()

    # TODO move that in the matplotlib renderer?
    def _get_mpl_artists(self, canvas: gsp.core.Canvas, visual_base: gsp.core.VisualBase) -> matplotlib.artist.Artist:
        """
        Get the matplotlib artists corresponding to a given visual in the canvas.
        This is needed for the matplotlib FuncAnimation to update only the relevant artists.
        """
        for viewport in canvas.viewports:
            for visual in viewport.visuals:
                # if it is not the visual we are looking for, skip it
                if visual != visual_base:
                    continue

                # get the mpl artist corresponding to the visual
                if isinstance(visual, gsp.visuals.Pixels):
                    pixels: gsp.visuals.Pixels = visual
                    patchCollections = self._matplotlib_renderer._pathCollections[pixels.uuid + viewport.uuid]
                    mpl_artist = patchCollections
                    return mpl_artist
                else:
                    assert False, "Visual type not supported yet"
        assert False, "Visual not found in canvas"
