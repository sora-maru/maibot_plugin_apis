import sys
import importlib.util
from pathlib import Path

plugin_root = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    'maibot_plugin_apis', plugin_root / '__init__.py',
    submodule_search_locations=[str(plugin_root)],
)
package = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = package
spec.loader.exec_module(package)
