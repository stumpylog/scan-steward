from django.apps import AppConfig


class ScanStewwardConfig(AppConfig):
    name = "scansteward"

    verbose_name = "ScanSteward"

    def ready(self):
        from scansteward.signals.handlers import cleanup_files_on_delete  # noqa: F401
        from scansteward.signals.handlers import mark_image_as_dirty  # noqa: F401
        from scansteward.signals.handlers import mark_images_as_dirty_on_fk_change  # noqa: F401
        from scansteward.signals.handlers import mark_images_as_dirty_on_m2m_change  # noqa: F401

        AppConfig.ready(self)
