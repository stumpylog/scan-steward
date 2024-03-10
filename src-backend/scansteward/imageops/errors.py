class ImageOperationError(Exception):
    pass


class ImageOperationMissingRequiredDataError(ImageOperationError):
    pass


class NoImagePathsError(ImageOperationError):
    pass


class NoImageMetadataError(ImageOperationError):
    pass


class ImagePathNotFileError(ImageOperationError):
    pass
