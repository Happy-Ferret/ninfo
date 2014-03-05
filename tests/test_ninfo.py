import ninfo

import importlib
from nose.tools import eq_
import logging

logging.basicConfig(level=logging.INFO)

class Wrapper:
    def __init__(self, name):
        self.name=name
    def load(self):
         return importlib.import_module(self.name)

test_plugins = {
    "a": Wrapper("tests.plug_a"),
}

def test_plugin_loading():
    n=ninfo.Ninfo(plugin_modules=test_plugins)
    assert 'a' in n
    assert 'b' not in n

    plugin = n.get_plugin('a')
    assert plugin is not None

    plugin = n.get_plugin('b')
    assert plugin is None

def test_plugin_lazy_loading():
    n=ninfo.Ninfo(plugin_modules=test_plugins)
    assert 'a' in n
    assert 'a' not in n.plugin_instances

    plugin = n.get_plugin('a')
    assert plugin is not None
    assert 'a' in n.plugin_instances

def test_plugin_lazy_init():
    n=ninfo.Ninfo(plugin_modules=test_plugins)
    plugin = n.get_plugin('a')
    assert plugin is not None
    assert 'a' in n.plugin_instances

    assert plugin.initialized is False

    res = n.get_info("a", "example.com")
    assert plugin.initialized is True

    eq_(res, "AAAAAAAAAAA")

def test_plugin_compatible_types():
    n=ninfo.Ninfo(plugin_modules=test_plugins)

    cases = [
        ("example.com", True),
        ("1.2.3.4", False),
        ("00:11:22:33:44:55", False),
    ]
    for arg, expected in cases:
        yield _plugin_compatible_type_case, n, arg, expected

def _plugin_compatible_type_case(n, arg, expected):
    assert n.compatible_argument("a", arg) == expected
