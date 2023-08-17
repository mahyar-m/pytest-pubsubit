import re


class ImportParser:
    @staticmethod
    def parse(sql_command: str) -> (str, str):
        match = re.match('(import|import_global) (.*)$', sql_command, re.I)
        if not match:
            return None, None

        return 'local' if match.group(1).lower() == "import" else 'global', match.group(2)
