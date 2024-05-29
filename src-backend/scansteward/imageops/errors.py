class ImageOperationError(Exception):
    """
    Base exception for all errors which arise from this library
    """


class NoImagePathsError(ImageOperationError):
    """
    A metadata read operation did not include an images to read
    """


class NoImageMetadataError(ImageOperationError):
    """
    No metadata was provided to a metadata write operation
    """


class ImagePathNotFileError(ImageOperationError):
    """
    A provided image path is not a file
    """
