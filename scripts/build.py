#!/usr/bin/env python3
"""Genera index.html (app instal·lable) a partir de src/rolada.html.

src/rolada.html és la font única: una pàgina sense <html>/<head>, la mateixa
que es publica com a artefacte. Aquest script l'embolcalla amb el head de
l'app (manifest, icones, service worker) i escriu index.html a l'arrel.
"""
import pathlib, re, hashlib

root = pathlib.Path(__file__).resolve().parent.parent
body = (root / 'src' / 'rolada.html').read_text(encoding='utf-8')
version = hashlib.sha1(body.encode()).hexdigest()[:8]

head = f'''<!doctype html>
<html lang="ca">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#0c1a22">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Rolada">
<meta name="description" content="Simulador de tàctica de cenyida en Optimist.">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
<link rel="icon" href="icons/icon-192.png">
<style>:root{{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}</style>
</head>
<body>
'''
tail = f'''
<script>if('serviceWorker' in navigator){{addEventListener('load',()=>navigator.serviceWorker.register('sw.js?v={version}').catch(()=>{{}}))}}</script>
</body>
</html>
'''
(root / 'index.html').write_text(head + body + tail, encoding='utf-8')
sw = (root / 'scripts' / 'sw.template.js').read_text(encoding='utf-8').replace('__VERSION__', version)
(root / 'sw.js').write_text(sw, encoding='utf-8')
print('index.html i sw.js generats, versió', version)
