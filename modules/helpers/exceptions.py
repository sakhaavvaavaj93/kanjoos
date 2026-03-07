class DurationLimitError(Exception):
    """Raised when a video/audio file exceeds the allowed duration."""
    pass


class FFmpegReturnCodeError(Exception):
    """Raised when an FFmpeg process fails with a non-zero return code."""
    pass
