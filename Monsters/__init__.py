"""يحمّل كل ملفات الوحوش في هذا المجلد تلقائياً."""
import importlib
import pkgutil

for _, _name, _ in pkgutil.iter_modules(__path__):
    importlib.import_module(f"{__name__}.{_name}")
