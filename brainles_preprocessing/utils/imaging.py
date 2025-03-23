import itk
from typing import Union, Optional, List
import itk


def __read_image(input_image: Union[str, itk.image]) -> itk.image:
    """
    Read an image from a file or return the image itself.

    Args:
        input_image (Union[str, itk.image]): The input image.

    Returns:
        itk.image: The output image.
    """
    return_image = input_image
    if isinstance(input_image, str):
        return_image = itk.imread(input_image)
    return return_image


def orient_to_rai(input_image: Union[str, itk.image]) -> itk.image:
    """
    Orient the input image to RAI orientation.

    Args:
        input_image (Union[str, itk.image]): The input image.

    Returns:
        itk.image: The output image in RAI orientation.
    """

    img_itk = __read_image(input_image)

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


def bias_corrector(
    input_image: Union[str, itk.image],
    input_mask: Union[str, itk.image],
    n_fitting_levels: Optional[int] = 3,
    n_max_iterations: Optional[Union[int, List[int]]] = None,
    convergence_threshold: Optional[float] = 0.001,
) -> itk.image:
    """
    Correct the bias field of the input image.

    Args:
        input_image (Union[str, itk.image]): The input image.
        input_mask (Union[str, itk.image]): The input mask.
        n_fitting_levels (Optional[int]): The number of fitting levels.
        n_max_iterations (Optional[Union[int, List[int]]]): The maximum number of iterations.
        convergence_threshold (Optional[float]): The convergence threshold.

    Returns:
        itk.image: The output image with corrected bias field.
    """
    img_itk = __read_image(input_image)
    mask_itk = __read_image(input_mask)

    corrector = itk.N4BiasFieldCorrectionImageFilter.New(img_itk, mask_itk)
    corrector.SetNumberOfFittingLevels(n_fitting_levels)
    corrector.SetMaximumNumberOfIterations(n_max_iterations)
    corrector.SetConvergenceThreshold(convergence_threshold)
    corrector.Update()
    return corrector.GetOutput()
