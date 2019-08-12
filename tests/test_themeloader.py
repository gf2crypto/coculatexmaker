"""Test for theme's loader."""
from io import StringIO
import unittest
from tempfile import TemporaryDirectory
from os import (makedirs,
                path)
from yaml import safe_load
import coculatex.config as config
from coculatex.themeloader import (load_theme,
                                   themes_iter)


class ThemeLoaderTestCase(unittest.TestCase):
    """Test Case for function `extract_variables`."""

    def setUp(self):
        """Prepartion for the test case."""
        self.tempdir = TemporaryDirectory()
        config.THEMES_PATH = self.tempdir.name

        self.themes_config = {
            'alpha': (
                'path: {path}\n'
                '{subthemes}:\n'
                '    a: a/a.yaml\n'
                '    b: b.yaml\n'
                '{parameters}:\n'
                '    param1: test1\n'
                '    param2: test2\n'
                '{description}: is alpha theme for the test\n'
                '{root_file}: alpha.tex\n'
                '{tex}:\n'
                '    option1: val1\n'
                '    option2: 25\n'
                '    option3: [1, 2, 3]\n'
                '{include_files}:\n'
                '    file1.tex: template_file1.tex\n'
                '    file2.tex: template_file2.tex\n'
                '{readme}: readme.txt\n'
                '{example}: examples/alpha\n'
                '{jinja2_config}:\n'
                '    autoescape: true\n'
                '    line_comment_prefix:' r' "%%##"' '\n'
                ''.format(**config.SECTION_NAMES_CONFIG,
                          path=path.join(self.tempdir.name, 'alpha',
                                         'config.yaml'))
            ),
            'a': (
                '{subthemes}:\n'
                '    a1: 1.yaml\n'
                '{parameters}:\n'
                '    param1: test1a\n'
                '    param2: test2a\n'
                '    param3: newtestA\n'
                '{description}: is `a` theme of the alpha subtheme\n'
                '{root_file}: a.tex\n'
                '{tex}:\n'
                '    option1: val1a\n'
                '    option2: AA\n'
                '    option3: [4, 5, 6]\n'
                '{include_files}:\n'
                '    file1.tex: template_file1a.tex\n'
                '    file2.tex: template_file2a.tex\n'
                '    file3.tex: template_file3a.tex\n'
                '{readme}: readmeA.txt\n'
                '{example}: examples/a\n'
                ''.format(**config.SECTION_NAMES_CONFIG)
            ),
            'alpha:a': (
                'path: {path}\n'
                '{subthemes}:\n'
                '    a1: 1.yaml\n'
                '{parameters}:\n'
                '    param1: test1a\n'
                '    param2: test2a\n'
                '    param3: newtestA\n'
                '{description}: is `a` theme of the alpha subtheme\n'
                '{root_file}: a.tex\n'
                '{tex}:\n'
                '    option1: val1a\n'
                '    option2: AA\n'
                '    option3: [4, 5, 6]\n'
                '{include_files}:\n'
                '    file1.tex: template_file1a.tex\n'
                '    file2.tex: template_file2a.tex\n'
                '    file3.tex: template_file3a.tex\n'
                '{readme}: readmeA.txt\n'
                '{example}: examples/a\n'
                '{jinja2_config}:\n'
                '    autoescape: true\n'
                '    line_comment_prefix:' r' "%%##"' '\n'
                ''.format(**config.SECTION_NAMES_CONFIG,
                          path=path.join(self.tempdir.name, 'alpha',
                                         'a', 'a.yaml'))
            ),
            'a1': (
                '{parameters}:\n'
                '    param3: newtest111\n'
                '{root_file}: 1.tex\n'
                '{tex}:\n'
                '    option1: val1111\n'
                '    option4: 11111\n'
                '{jinja2_config}: {{}}\n'
                ''.format(**config.SECTION_NAMES_CONFIG)
            ),
            'alpha:a:a1': (
                'path: {path}\n'
                '{subthemes}: {{}}\n'
                '{parameters}:\n'
                '    param1: test1a\n'
                '    param2: test2a\n'
                '    param3: newtest111\n'
                '{description}: ""\n'
                '{root_file}: 1.tex\n'
                '{tex}:\n'
                '    option1: val1111\n'
                '    option2: AA\n'
                '    option3: [4, 5, 6]\n'
                '    option4: 11111\n'
                '{include_files}:\n'
                '    file1.tex: template_file1a.tex\n'
                '    file2.tex: template_file2a.tex\n'
                '    file3.tex: template_file3a.tex\n'
                '{readme}: ""\n'
                '{example}: ""\n'
                '{jinja2_config}:\n'
                '    autoescape: true\n'
                '    line_comment_prefix:' r' "%%##"' '\n'
                ''.format(**config.SECTION_NAMES_CONFIG,
                          path=path.join(self.tempdir.name, 'alpha',
                                         'a', '1.yaml'))
            )
        }
        self.themes = {
            'alpha': safe_load(StringIO(self.themes_config['alpha'])),
            'alpha:a': safe_load(StringIO(self.themes_config['alpha:a'])),
            'alpha:a:a1': safe_load(StringIO(self.themes_config['alpha:a:a1']))
        }
        self.make_diretory_tree()

    def make_diretory_tree(self):
        """Make the directories tree."""
        for name, theme in self.themes.items():
            makedirs(path.dirname(theme['path']), exist_ok=True)
            with open(theme['path'], 'w') as file:
                file.write(self.themes_config[name])

    def tearDown(self):
        """Clean the system after tests."""
        self.tempdir.cleanup()

    def test_load_root_theme(self):
        """Test load the root theme."""
        theme = load_theme('alpha')
        self.assertEqual(theme.items(), self.themes['alpha'].items())

    def test_load_subtheme(self):
        """Test load the subtheme."""
        theme = load_theme('alpha{sep}a'.format(sep=config.THEME_NAME_SEP))
        self.assertEqual(theme.items(), self.themes['alpha:a'].items())

    def test_load_subsubtheme(self):
        """Test load the subsubtheme."""
        theme = load_theme(
            'alpha{sep}a{sep}a1'.format(sep=config.THEME_NAME_SEP))
        self.assertEqual(theme.items(), self.themes['alpha:a:a1'].items())

    def test_theme_not_exits(self):
        """Test load the subsubtheme."""
        theme = load_theme('beta')
        self.assertEqual(theme.items(), {}.items())

    def test_subtheme_not_exits(self):
        """Test load the subsubtheme."""
        theme = load_theme('alpha{sep}beta'.format(sep=config.THEME_NAME_SEP))
        self.assertEqual(theme.items(), self.themes['alpha'].items())

    def test_subtheme_config_not_exits(self):
        """Test load the subsubtheme."""
        theme = load_theme('alpha{sep}b'.format(sep=config.THEME_NAME_SEP))
        self.assertEqual(theme.items(), self.themes['alpha'].items())


class ThemeIteratorTestCase(unittest.TestCase):
    """Test Case for iteration over themes."""

    def setUp(self):
        """Prepartion for the test case."""
        self.tempdir = TemporaryDirectory()
        self.themes_config = {
            'a': (
                'path: {path}\n'
                '{subthemes}:\n'
                '    a1: a1.yaml\n'
                '    a2: a2.yaml\n'
                '    a3: a3.yaml\n'
                ''.format(**config.SECTION_NAMES_CONFIG,
                          path=path.join(self.tempdir.name,
                                         'a', 'config.yaml'))
            ),
            'a1': (
                'path: {path}\n'
                '{subthemes}:\n'
                '    a11: a11.yaml\n'
                '    a12: a12.yaml\n'
                ''.format(**config.SECTION_NAMES_CONFIG,
                          path=path.join(self.tempdir.name,
                                         'a', 'a1.yaml'))
            ),
            'a11': (
                'path: {path}\n'
                ''.format(path=path.join(self.tempdir.name,
                                         'a', 'a11.yaml'))
            ),
            'a12': (
                'path: {path}\n'
                ''.format(path=path.join(self.tempdir.name,
                                         'a', 'a12.yaml'))
            ),
            'a2': (
                'path: {path}\n'
                ''.format(path=path.join(self.tempdir.name,
                                         'a', 'a2.yaml'))
            ),
            'a3': (
                'path: {path}\n'
                ''.format(path=path.join(self.tempdir.name,
                                         'a', 'a3.yaml'))
            ),
            'b': (
                'path: {path}\n'
                '{subthemes}:\n'
                '    b1: b1.yaml\n'
                ''.format(**config.SECTION_NAMES_CONFIG,
                          path=path.join(self.tempdir.name,
                                         'b', 'config.yaml'))
            ),
            'b1': (
                'path: {path}\n'
                ''.format(path=path.join(self.tempdir.name,
                                         'b', 'b1.yaml'))
            ),
            'c': (
                'path: {path}\n'
                ''.format(path=path.join(self.tempdir.name,
                                         'c', 'config.yaml'))
            ),
        }
        self.themes = {}
        config.THEMES_PATH = self.tempdir.name
        self.make_files()

    def tearDown(self):
        """Clean after test."""
        self.tempdir.cleanup()

    def make_files(self):
        """Make directory tree."""
        for (name, conf_str) in self.themes_config.items():
            self.themes[name] = safe_load(StringIO(conf_str))
            makedirs(path.dirname(self.themes[name]['path']), exist_ok=True)
            with open(self.themes[name]['path'], 'w') as file:
                file.write('\n'.join(conf_str.split('\n')[1:]))

    def test_iteration_all(self):
        """Test iteration over all themes."""
        check_themes = {name: load_theme(name)
                        for name in ['a', 'b', 'c']}
        themes = dict(themes_iter())
        for name, theme_conf in check_themes.items():
            self.assertIn(name, themes)
            self.assertEqual(theme_conf.items(), themes[name].items())

    def test_iteration_theme(self):
        """Test iteration over subthemes."""
        check_themes = {'a{sep}{name}'.format(sep=config.THEME_NAME_SEP,
                                              name=name):
                        load_theme('a{sep}{name}'.format(
                            sep=config.THEME_NAME_SEP,
                            name=name))
                        for name in ['a1', 'a2', 'a3']}
        themes = dict(themes_iter('a'))
        for name, theme_conf in check_themes.items():
            self.assertIn(name, themes)
            self.assertEqual(theme_conf.items(), themes[name].items())

    def test_iteration_not_theme(self):
        """Test iteration over all themes if a theme does not exist."""
        check_themes = {name: load_theme(name)
                        for name in ['a', 'b', 'c']}
        makedirs(path.join(self.tempdir.name, 'notheme'))
        themes = dict(themes_iter())
        for name, theme_conf in check_themes.items():
            self.assertIn(name, themes)
            self.assertEqual(theme_conf.items(), themes[name].items())


if __name__ == '__main__':
    unittest.main(verbosity=0)
