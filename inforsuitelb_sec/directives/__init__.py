import os

from inforsuitelb_sec.directives.directive import Directive

DIRECTIVES = {}


def import_directives():
    files_list = os.listdir(os.path.dirname(__file__))
    for directive_file in files_list:
        if not directive_file.endswith(".py") or directive_file.startswith("_"):
            continue
        __import__(
            "inforsuitelb_sec.directives." + os.path.splitext(directive_file)[0], None, None, [""]
        )


def get_all():
    if len(DIRECTIVES):
        return DIRECTIVES

    import_directives()
    for klass in Directive.__subclasses__():
        if not klass.InforSuiteLB_name:
            continue
        DIRECTIVES[klass.InforSuiteLB_name] = klass

    return DIRECTIVES
