"""Navigation mobile, partage local et isolation du cache de Papiers Sans Galère."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
import unittest
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]


class Quiet(SimpleHTTPRequestHandler):
    def log_message(self, *_): pass
    def copyfile(self, source, output):
        try: super().copyfile(source, output)
        except (BrokenPipeError, ConnectionResetError): pass


class AuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), partial(Quiet, directory=str(ROOT.parent)))
        Thread(target=cls.server.serve_forever, daemon=True).start()
        cls.base = f'http://127.0.0.1:{cls.server.server_port}/Papiers-sans-galere/'
        cls.p = sync_playwright().start()
        cls.browser = cls.p.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])

    @classmethod
    def tearDownClass(cls):
        cls.browser.close(); cls.p.stop(); cls.server.shutdown(); cls.server.server_close()

    def context(self, width=390, workers='block'):
        context = self.browser.new_context(viewport={'width': width, 'height': 900}, service_workers=workers)
        context.route('**/*', lambda route: route.continue_() if route.request.url.startswith(self.base) else route.abort())
        return context

    def test_mobile_desktop_and_private_sharing(self):
        for width in [320, 390, 1440]:
            context = self.context(width); page = context.new_page(); requests = []; errors = []
            page.on('request', lambda r: requests.append(r.url))
            page.on('pageerror', lambda e: errors.append(str(e)))
            for path in ['', 'outils.html', 'accompagnement.html']:
                with self.subTest(width=width, path=path):
                    page.goto(self.base + path, wait_until='networkidle')
                    self.assertLessEqual(page.evaluate('document.documentElement.scrollWidth'), width + 1)
                    self.assertEqual(page.locator('.vmbar .vmb-logo').get_attribute('href'), 'https://vmunivers.fr/')
                    page.locator('#vmFab').click()
                    page.wait_for_selector('#vmShQ canvas', state='attached')
                    self.assertEqual(errors, [])
                    self.assertFalse(any('countapi.' in u or 'vm-stats-' in u or 'qrserver.com' in u or 'cdnjs.' in u for u in requests))
            context.close()

    def test_worker_preserves_other_apps_and_offline_page(self):
        context = self.context(workers='allow'); page = context.new_page()
        page.goto(self.base, wait_until='networkidle')
        page.evaluate("async()=>{await navigator.serviceWorker.ready;await caches.open('other-app-cache');await caches.open('pp-app-v1')}")
        page.evaluate("async()=>{const r=await navigator.serviceWorker.ready;r.active.postMessage('test');return navigator.serviceWorker.register('sw.js?migration=1')}")
        page.wait_for_function("async()=>{let k=await caches.keys();return k.includes('pp-app-v3')&&!k.includes('pp-app-v1')}")
        self.assertIn('other-app-cache', page.evaluate('caches.keys()'))
        context.set_offline(True)
        page.reload(wait_until='domcontentloaded')
        self.assertGreater(page.locator('h1').count(), 0)
        context.close()


if __name__ == '__main__': unittest.main(verbosity=2)
