"""
http://djangosnippets.org/snippets/2485/
"""

from os import path
from django.core.exceptions import ImproperlyConfigured
from django.db.models.loading import get_app
from django.template.base import TemplateDoesNotExist
from django.template.loaders.filesystem import Loader as FileSystemLoader
from django.template.loaders.app_directories import (
    Loader as AppDirLoader, app_template_dirs)


__all__ = ('SpecificAppLoader', 'ReverseAppDirLoader')


class SpecificAppLoader(FileSystemLoader):
    """ Template loader that only serves templates from specific
    app's template directory.

    This is useful to allow overriding a template while inheriting
    from the original.

    Expects template names in the form of:

        app_label:some/template/name.html
    """

    def load_template_source(self, template_name, template_dirs=None):
        if ":" not in template_name:
            raise TemplateDoesNotExist()

        app_name, template_name = template_name.split(":", 1)
        try:
            app = get_app(app_name)
        except ImproperlyConfigured:
            raise TemplateDoesNotExist()
        else:
            if path.basename(app.__file__).startswith('__init__'):
                # When "app.models" is a directory, app.__file__ will
                # be app/models/__init.py.
                app_dir = path.dirname(path.dirname(app.__file__))
            else:
                app_dir = path.dirname(app.__file__)
            app_templ_dir = path.join(app_dir, 'templates')
            if not path.isdir(app_templ_dir):
                raise TemplateDoesNotExist()

            return FileSystemLoader.load_template_source(
                self, template_name, template_dirs=[app_templ_dir])


class ReverseAppDirLoader(AppDirLoader):
    """Modifies the behavior of Django's app directories template
    loader to search the list of installed apps in reverse.

    This is allows later apps to override templates in earlier apps,
    like builtin apps, which are usually listed first.

    (It appears as if Django expects you to use the filesystem loader
    for replacing admin templates.)
    """

    def get_template_sources(self, template_name, template_dirs=None):
        if not template_dirs:
            template_dirs = app_template_dirs
        return AppDirLoader.get_template_sources(
            self, template_name, reversed(template_dirs))
