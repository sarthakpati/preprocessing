import itk.itkOrientImageFilterPython
from typing import Union
import itk
import numpy as np


def orient_to_rai(input_image: Union[str, itk.image]) -> itk.image:
    """
    Orient the input image to RAI orientation.

    Args:
        input_image (Union[str, itk.image]): The input image.

    Returns:
        itk.image: The output image in RAI orientation.
    """

    img_itk = input_image
    if isinstance(input_image, str):
        img_itk = itk.imread(input_image)

    itk_so_enums = (
        itk.SpatialOrientationEnums
    )  # keep the next long line below style threshold
    itk_lps = itk_so_enums.ValidCoordinateOrientations_ITK_COORDINATE_ORIENTATION_RAI
    orienter = itk.OrientImageFilter.New(
        img_itk,
        use_image_direction=True,
        desired_coordinate_orientation=itk_lps,
    )

    orienter.UpdateOutputInformation()
    orienter.Update()
    return orienter.GetOutput()
