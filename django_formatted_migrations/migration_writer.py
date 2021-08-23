from django.db.migrations.writer import MigrationWriter

# These are dev dependencies
# Code format is of to prevent makemigrations command crash on prod environment
try:
    from add_trailing_comma._main import _fix_src as fix_commas
    from autopep8 import fix_code

    _skip_code_format = False
except ModuleNotFoundError:
    _skip_code_format = True

INDENT = '    '


class FormattedMigrationWriter(MigrationWriter):
    def as_string(self):
        return self._modify_code(
            super().as_string(),
            self._add_docstring,
            self._format_code,
        )

    def _add_docstring(self, code: str) -> str:
        add_after = 'class Migration(migrations.Migration):\n'
        doc = self.migration.name.split('_', maxsplit=1)[1]
        docstring_line = f'{INDENT}"""{doc}."""\n'
        return code.replace(add_after, add_after + docstring_line)

    def _format_code(self, code):
        if _skip_code_format:
            return code
        code = fix_code(code)
        return fix_commas(code, min_version=(3, 6))

    def _modify_code(self, code, *funcs):
        for func in funcs:
            code = func(code)
        return code
