from django.core.management.commands.makemigrations import (
    Command as MakeMigrationsCommand,
)

from django_formatted_migrations.migration_writer import (
    FormattedMigrationWriter,
)


class Command(MakeMigrationsCommand):

    migration_writer_class = FormattedMigrationWriter

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._patch_writer(super().write_migration_files)
        self._patch_writer(super().handle_merge)

    def _patch_writer(self, func):
        func.__globals__['MigrationWriter'] = self.migration_writer_class
