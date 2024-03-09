class ImageOperationError(Exception):
    pass


class ImageOperationMissingRequiredDataError(ImageOperationError):
    pass


class NoImagePathsError(ImageOperationError):
    pass


class ImagePathNotFileError(ImageOperationError):
    pass
