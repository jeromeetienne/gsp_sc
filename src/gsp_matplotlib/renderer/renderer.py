# stdlib imports
import io
import os
import typing

# pip imports
import matplotlib.collections
import matplotlib.pyplot
import matplotlib.axes
import matplotlib.figure
import matplotlib.collections
import matplotlib.image
import mpl3d.camera

# local imports
from gsp.core.canvas import Canvas
from gsp.core.viewport import Viewport
from gsp.core.camera import Camera
from gsp.visuals.pixels import Pixels
from gsp.visuals.image import Image
from gsp.visuals.mesh import Mesh


class MatplotlibRenderer:
    def __init__(self) -> None:
        self._figures: dict[str, matplotlib.figure.Figure] = {}
        """Mapping from canvas UUID to matplotlib Figure"""
        self._axes: dict[str, matplotlib.axes.Axes] = {}
        """Mapping from viewport UUID to matplotlib Axes"""
        self._pathCollections: dict[str, matplotlib.collections.PathCollection] = {}
        """Mapping from visual UUID to matplotlib PathCollection. For Pixels visuals."""
        self._polyCollections: dict[str, matplotlib.collections.PolyCollection] = {}
        """Mapping from visual UUID to matplotlib PolyCollection. For Mesh visuals."""
        self._axesImages: dict[str, matplotlib.image.AxesImage] = {}
        """Mapping from visual UUID to matplotlib AxesImage. For Image visuals."""

    def close(self) -> None:
        """Close all matplotlib figures managed by this renderer."""
        for figure in self._figures.values():
            # stop the event loop if any - thus .show(block=True) will return
            figure.canvas.stop_event_loop()
            # close the figure
            matplotlib.pyplot.close(figure)
        self._figures.clear()
        self._axes.clear()
        self._pathCollections.clear()
        self._polyCollections.clear()
        self._axesImages.clear()

    # =============================================================================
    # .render()
    # =============================================================================

    def render(
        self,
        canvas: Canvas,
        viewports: list[Viewport],
        cameras: list[Camera],
        show_image: bool = False,
        return_image: bool = True,
        interactive: bool = False,
        image_format: str = "png",
    ) -> bytes:

        self.__render(canvas, viewports=viewports, cameras=cameras)

        ################################################################################

        image_png_data = b""

        # honor return_image option
        if return_image:
            # Render the image to a PNG buffer
            image_png_buffer = io.BytesIO()
            matplotlib.pyplot.savefig(image_png_buffer, format=image_format)
            image_png_buffer.seek(0)
            image_png_data = image_png_buffer.getvalue()
            image_png_buffer.close()

        # honor show_image option
        if show_image:
            # enter the matplotlib main loop IIF env.var GSP_SC_INTERACTIVE is not set to "False"
            if "GSP_SC_INTERACTIVE" not in os.environ or os.environ["GSP_SC_INTERACTIVE"] != "False":
                matplotlib.pyplot.show(block=True)

        # Handle interactive camera IIF env.var GSP_SC_INTERACTIVE is not set to "False"
        if interactive and ("GSP_SC_INTERACTIVE" not in os.environ or os.environ["GSP_SC_INTERACTIVE"] != "False"):
            figure = matplotlib.pyplot.gcf()
            mpl_axes = figure.get_axes()[0]

            # connect the camera events to the render function
            def camera_update(transform) -> None:
                self.__render(canvas, viewports=viewports, cameras=cameras)

            mpl3d_cameras: list[mpl3d.camera.Camera] = [camera.mpl3d_camera for camera in cameras]
            for mpl3d_camera in mpl3d_cameras:
                mpl3d_camera.connect(mpl_axes, camera_update)

            matplotlib.pyplot.show(block=True)

            for mpl3d_camera in mpl3d_cameras:
                mpl3d_camera.disconnect()

        # return the PNG image data if requested else return empty bytes
        return image_png_data

    ###########################################################################
    ###########################################################################
    # .__render()
    ###########################################################################
    ###########################################################################

    def __render(self, canvas: Canvas, viewports: list[Viewport], cameras: list[Camera]) -> None:

        # Create the matplotlib figure from the canvas if it does not exist yet
        if canvas.uuid in self._figures:
            figure = self._figures[canvas.uuid]
        else:
            # print(f"Creating new figure {canvas.uuid}")
            figure = matplotlib.pyplot.figure(frameon=False, dpi=canvas.dpi)
            figure.set_size_inches(canvas.width / canvas.dpi, canvas.height / canvas.dpi)
            self._figures[canvas.uuid] = figure

        # sanity check - viewports and cameras must have the same length
        assert len(viewports) == len(cameras), "Number of viewports must be equal to number of cameras."

        for viewport, camera in zip(viewports, cameras):
            # create an axes for each viewport
            if viewport.uuid in self._axes:
                axes = self._axes[viewport.uuid]
            else:
                # print(f"Creating new axes for viewport {viewport.uuid}")
                axes_rect = (
                    viewport.origin_x / canvas.width,
                    viewport.origin_y / canvas.height,
                    viewport.width / canvas.width,
                    viewport.height / canvas.height,
                )
                axes: matplotlib.axes.Axes = figure.add_axes(axes_rect)
                axes.set_facecolor(viewport.background_color)
                axes.set_xlim(-1, 1)
                axes.set_ylim(-1, 1)
                axes.get_xaxis().set_visible(False)
                axes.get_yaxis().set_visible(False)
                # Remove the borders
                axes.spines["top"].set_visible(False)
                axes.spines["right"].set_visible(False)
                axes.spines["bottom"].set_visible(False)
                axes.spines["left"].set_visible(False)
                # cache the axes
                self._axes[viewport.uuid] = axes

            for visual in viewport.visuals:
                full_uuid = visual.uuid + viewport.uuid
                if isinstance(visual, Pixels):
                    from .renderer_pixels import MatplotlibRendererPixels

                    MatplotlibRendererPixels.render(
                        self,
                        axes,
                        visual,
                        full_uuid=full_uuid,
                        camera=camera,
                    )
                elif isinstance(visual, Image):
                    from .renderer_image import MatplotlibRendererImage

                    MatplotlibRendererImage.render(
                        self,
                        axes,
                        visual,
                        full_uuid=full_uuid,
                        camera=camera,
                    )
                elif isinstance(visual, Mesh):
                    from .renderer_mesh import MatplotlibRendererMesh

                    MatplotlibRendererMesh.render(
                        self,
                        axes,
                        visual,
                        full_uuid=full_uuid,
                        camera=camera,
                    )
                else:
                    raise NotImplementedError(f"Rendering for visual type {type(visual)} is not implemented.")
