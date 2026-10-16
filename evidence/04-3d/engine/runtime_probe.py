from playwright.sync_api import sync_playwright
import json, time, os
from pathlib import Path

URL = 'https://screen.sessionhd.com/screen/index.html?preview=browser&type=default#/3d'
OUT = Path('evidence/04-3d/engine')
OUT.mkdir(parents=True, exist_ok=True)

requests = []
console = []
errors = []

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
        args=[
            '--use-gl=angle',
            '--use-angle=swiftshader',
            '--enable-webgl',
            '--ignore-gpu-blocklist',
            '--no-first-run',
            '--no-default-browser-check',
        ],
    )
    context = browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        device_scale_factor=1,
        locale='zh-CN',
    )
    page = context.new_page()

    def on_request(req):
        if len(requests) < 500:
            requests.append({
                'method': req.method,
                'url': req.url,
                'resource_type': req.resource_type,
                'is_navigation': req.is_navigation_request(),
            })

    def on_console(msg):
        if len(console) < 300:
            console.append({'type': msg.type, 'text': msg.text[:1000]})

    def on_pageerror(exc):
        if len(errors) < 100:
            errors.append(str(exc)[:2000])

    page.on('request', on_request)
    page.on('console', on_console)
    page.on('pageerror', on_pageerror)

    nav = None
    try:
        nav = page.goto(URL, wait_until='domcontentloaded', timeout=90000)
    except Exception as e:
        errors.append('goto: ' + str(e)[:2000])
    try:
        page.wait_for_timeout(12000)
    except Exception:
        pass

    probe = {}
    try:
        probe = page.evaluate('''() => {
          const canvases = [...document.querySelectorAll('canvas')].map(c => ({
            id: c.id, className: c.className, width: c.width, height: c.height,
            clientWidth: c.clientWidth, clientHeight: c.clientHeight,
            display: getComputedStyle(c).display, visible: !!(c.offsetWidth || c.offsetHeight || c.getClientRects().length)
          }));
          let gl = null, vendor = null, renderer = null, version = null, shading = null, extensions = [];
          const c = document.querySelector('canvas');
          if (c) {
            try {
              gl = c.getContext('webgl2') || c.getContext('webgl') || c.getContext('experimental-webgl');
              if (gl) {
                vendor = gl.getParameter(gl.VENDOR);
                renderer = gl.getParameter(gl.RENDERER);
                version = gl.getParameter(gl.VERSION);
                shading = gl.getParameter(gl.SHADING_LANGUAGE_VERSION);
                extensions = gl.getSupportedExtensions() || [];
              }
            } catch (e) { renderer = 'error: ' + e; }
          }
          const scripts = [...document.scripts].map(s => s.src).filter(Boolean);
          const links = [...document.querySelectorAll('link[rel="stylesheet"]')].map(l => l.href);
          return {
            title: document.title,
            href: location.href,
            readyState: document.readyState,
            canvases,
            gl: {vendor, renderer, version, shading, extensionCount: extensions.length},
            scripts, links,
            appHTML: (document.querySelector('#app') || {}).innerHTML ? document.querySelector('#app').innerHTML.slice(0, 4000) : null,
            bodyText: document.body ? document.body.innerText.slice(0, 3000) : null,
            globals: {
              THREE: typeof window.THREE,
              Vue: typeof window.Vue,
              $signin3d: typeof window.$signin3d,
              webpackJsonp: typeof window.webpackJsonp,
            }
          };
        }''')
    except Exception as e:
        errors.append('evaluate: ' + str(e)[:2000])

    screenshot = OUT / 'runtime-3d.png'
    try:
        page.screenshot(path=str(screenshot), full_page=False, timeout=30000)
    except Exception as e:
        errors.append('screenshot: ' + str(e)[:2000])

    context.close()
    browser.close()

result = {
    'url': URL,
    'probed_at': time.strftime('%Y-%m-%dT%H:%M:%S%z'),
    'navigation': {'status': nav.status if nav else None, 'url': nav.url if nav else None},
    'probe': probe,
    'requests': requests,
    'console': console,
    'errors': errors,
    'screenshot': str(screenshot),
}
(OUT/'runtime-probe.json').write_text(json.dumps(result, ensure_ascii=False, indent=2))
print(json.dumps({
    'navigation': result['navigation'],
    'title': probe.get('title'),
    'canvases': probe.get('canvases'),
    'gl': probe.get('gl'),
    'globals': probe.get('globals'),
    'request_count': len(requests),
    'console_count': len(console),
    'errors': errors,
}, ensure_ascii=False, indent=2))
