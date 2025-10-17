# stdlib imports
import os
import sys

# pip imports
import numpy as np
import matplotlib.pyplot

# local imports
import gsp

__dirname__ = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(__dirname__, "../output")


class ExamplesUtils:
    @staticmethod
    def preamble():
        """
        If in testing mode, set random seeds for reproducibility.
        """

        # detect if we are in not interactive mode - used during testing
        gsp_sc_interactive = "GSP_SC_INTERACTIVE" not in os.environ or os.environ["GSP_SC_INTERACTIVE"] != "False"

        # if not in testing mode, return now
        if gsp_sc_interactive == True:
            return

        # set random seed for reproducibility
        np.random.seed(0)
        gsp.core.random.Random.set_random_seed(0)

    @staticmethod
    def postamble():
        """
        If in testing mode, save the current matplotlib.pyplot figure to the output directory.
        else do nothing.

        Returns:
        - should_exit (bool): True if the calling script should exit after saving the image,
          False otherwise.

        Usage:
        ```python
        should_exit = ExamplesUtils.postamble()
        if should_exit:
            sys.exit(0)
        ```
        """
        # detect if we are in not interactive mode - used during testing
        gsp_sc_interactive = "GSP_SC_INTERACTIVE" not in os.environ or os.environ["GSP_SC_INTERACTIVE"] != "False"

        # if not in testing mode, return now
        MPLSC_TESTING = os.environ.get("MPLSC_TESTING", "False")
        if gsp_sc_interactive == True:
            return False

        # get the __file__ of the calling script
        example_filename = getattr(sys.modules.get("__main__"), "__file__", None)
        assert example_filename is not None, "Could not determine example filename"

        # Extract example basename and directory
        example_basename = os.path.basename(example_filename).replace(".py", "")

        # save the output to a file
        image_path = os.path.join(output_path, f"{example_basename}.png")
        matplotlib.pyplot.savefig(image_path)
        print(f"Saved output to {image_path}")

        return True
