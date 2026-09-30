import unittest, tempfile
from pathlib import Path
from hermes_learn.install import install, uninstall

class InstallTests(unittest.TestCase):

    def test_fingerprint_uses_portable_paths_on_windows(self):
        from pathlib import PureWindowsPath
        from unittest.mock import Mock, patch
        from hermes_learn.install import fingerprint
        import hashlib

        file = Mock()
        file.is_symlink.return_value = False
        file.is_file.return_value = True
        file.parent.name = 'nested'
        file.relative_to.return_value = PureWindowsPath('nested/helper.py')
        file.read_bytes.return_value = b'original content'
        root = Mock()
        root.is_symlink.return_value = False
        root.rglob.return_value = [file]
        with patch('hermes_learn.install.Path', return_value=root):
            self.assertEqual(fingerprint('source'), {
                'nested/helper.py': hashlib.sha256(b'original content').hexdigest(),
            })

    def test_isolated_install_roundtrip(self):
        with tempfile.TemporaryDirectory() as d:
            h = Path(d).resolve()
            install(h, dry_run=True)
            self.assertFalse((h / 'plugins').exists())
            install(h)
            self.assertTrue((h / 'plugins/hermes-learn/plugin.yaml').exists())
            uninstall(h)
            self.assertFalse((h / 'plugins/hermes-learn').exists())

    def test_conflict_preserved(self):
        with tempfile.TemporaryDirectory() as d:
            h = Path(d).resolve()
            p = h / 'skills/teach'
            p.mkdir(parents=True)
            (p / 'mine').write_text('personal')
            with self.assertRaises(FileExistsError):
                install(h)
            self.assertEqual((p / 'mine').read_text(), 'personal')
            self.assertFalse((h / 'plugins').exists())

    def test_non_cache_files_in_pycache_prevent_uninstall(self):
        for name in ('personal-notes.md', 'personal.pyc'):
            with self.subTest(name=name), tempfile.TemporaryDirectory() as d:
                h = Path(d).resolve()
                install(h)
                cache = h / 'plugins/hermes-learn/runtime/__pycache__'
                cache.mkdir(exist_ok=True)
                note = cache / name
                note.write_text('personal')
                (cache / 'core.cpython-314.pyc').write_bytes(b'disposable')
                with self.assertRaises(ValueError):
                    uninstall(h)
                self.assertEqual(note.read_text(), 'personal')
                self.assertTrue((h / '.hermes-learn-install.json').exists())

    def test_partial_copy_failure_rolls_back_new_destinations(self):
        from unittest.mock import patch
        import shutil
        real_copytree = shutil.copytree
        for failing_target in ('skills/teach', 'skills/visualize', 'plugins/hermes-learn'):
            with self.subTest(target=failing_target), tempfile.TemporaryDirectory() as d:
                h = Path(d).resolve()
                survivor = h / 'skills/personal'
                survivor.mkdir(parents=True)
                (survivor / 'notes.md').write_text('keep')
                def partial_copy(src, dst, *args, **kwargs):
                    if Path(dst) == h / failing_target:
                        Path(dst).mkdir(exist_ok=True)
                        (Path(dst) / 'partial').write_text('partial')
                        raise OSError('injected partial copy failure')
                    return real_copytree(src, dst, *args, **kwargs)
                with patch('hermes_learn.install.shutil.copytree', side_effect=partial_copy):
                    with self.assertRaisesRegex(OSError, 'injected partial copy failure'):
                        install(h)
                for target in ('skills/teach', 'skills/visualize', 'plugins/hermes-learn'):
                    self.assertFalse((h / target).exists())
                self.assertFalse((h / '.hermes-learn-install.json').exists())
                self.assertEqual((survivor / 'notes.md').read_text(), 'keep')

    def test_source_non_cache_files_are_installed_and_owned(self):
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as d:
            root = Path(d).resolve() / 'source'
            for rel in ('skills/teach', 'skills/visualize', 'plugin', 'hermes_learn'):
                (root / rel).mkdir(parents=True)
            cache = root / 'hermes_learn/__pycache__'
            cache.mkdir()
            (cache / 'personal-notes.md').write_text('source note')
            (cache / 'core.cpython-314.pyc').write_bytes(b'disposable')
            h = Path(d).resolve() / 'profile'
            with patch('hermes_learn.install.ROOT', root):
                install(h)
            installed = h / 'plugins/hermes-learn/runtime/__pycache__'
            self.assertTrue((installed / 'personal-notes.md').exists())
            self.assertFalse((installed / 'core.cpython-314.pyc').exists())
            (installed / 'core.cpython-314.opt-1.pyc').write_bytes(b'disposable')
            uninstall(h)
            self.assertFalse((h / 'plugins/hermes-learn').exists())

    def test_modified_install_not_removed(self):
        with tempfile.TemporaryDirectory() as d:
            h = Path(d).resolve()
            install(h)
            p = h / 'skills/teach/SKILL.md'
            p.write_text('edited')
            with self.assertRaises(ValueError):
                uninstall(h)
            self.assertEqual(p.read_text(), 'edited')
