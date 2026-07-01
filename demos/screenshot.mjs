// Screenshot carousel slides via CDP (navigate to local server)
import { readFileSync, mkdirSync, writeFileSync } from 'fs';

const CDP_PORT = 18800;
const SITE = `http://127.0.0.1:${CDP_PORT}`;
const HTTP_HOST = 'http://127.0.0.1:8765';

const carousels = [
  { name: 'carousel-1-student', slides: 6, file: 'carousel-1-student.html' },
  { name: 'carousel-2-relation', slides: 7, file: 'carousel-2-relation.html' },
  { name: 'carousel-3-child', slides: 5, file: 'carousel-3-child.html' },
];

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

function connectWS(url) {
  return new Promise((resolve, reject) => {
    const ws = new WebSocket(url);
    ws.addEventListener('open', () => resolve(ws));
    ws.addEventListener('error', () => reject(new Error('WS failed: ' + url)));
    setTimeout(() => reject(new Error('WS timeout: ' + url)), 8000);
  });
}

function makeSender(ws) {
  return (msg, timeoutMs = 30000) => new Promise((resolve, reject) => {
    const id = Math.floor(Math.random() * 1000000);
    ws.send(JSON.stringify({ id, ...msg }));
    const handler = (event) => {
      try {
        const resp = JSON.parse(event.data.toString());
        if (resp.id === id) resolve(resp);
      } catch (e) {}
    };
    ws.addEventListener('message', handler);
    setTimeout(() => {
      ws.removeEventListener('message', handler);
      reject(new Error(`CDP timeout: ${msg.method}`));
    }, timeoutMs);
  });
}

async function main() {
  const ver = await (await fetch(`${SITE}/json/version`)).json();
  console.log('Chrome:', ver.Browser);

  const bws = await connectWS(ver.webSocketDebuggerUrl);
  const bsend = makeSender(bws);
  console.log('CDP connected\n');

  mkdirSync('output', { recursive: true });

  for (const c of carousels) {
    console.log(`═══ ${c.name} (${c.slides} slides) ═══`);

    // Create tab → navigate to local HTML
    const { result: { targetId } } = await bsend({
      method: 'Target.createTarget',
      params: { url: `${HTTP_HOST}/${c.file}` }
    });

    // Connect to page CDP
    const pws = await connectWS(`ws://127.0.0.1:${CDP_PORT}/devtools/page/${targetId}`);
    const ps = makeSender(pws);

    // Wait for load + fonts
    await sleep(2000);

    // Enable Page events (won't catch load at this point but that's OK)
    await ps({ method: 'Page.enable' });
    await sleep(500);

    // Set viewport for crisp 2x output
    await ps({
      method: 'Emulation.setDeviceMetricsOverride',
      params: { width: 1080, height: 1080, deviceScaleFactor: 2, mobile: false }
    });
    await sleep(300);

    // Check font loading
    const f = await ps({
      method: 'Runtime.evaluate',
      params: { expression: `document.fonts.ready.then(() => document.fonts.size + ' fonts loaded')`, awaitPromise: true }
    });
    console.log(`  ${f.result.result.value}`);

    // Take screenshots
    for (let i = 0; i < c.slides; i++) {
      await ps({
        method: 'Runtime.evaluate',
        params: { expression: `window.scrollTo(0, ${i * 1080})` }
      });

      // Wait for rendering
      await ps({
        method: 'Runtime.evaluate',
        params: { expression: `new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)))`, awaitPromise: true }
      });

      const { result: { data } } = await ps({
        method: 'Page.captureScreenshot',
        params: { format: 'png', fromSurface: true }
      });

      const outPath = `output/${c.name}-slide-${String(i + 1).padStart(2, '0')}.png`;
      writeFileSync(outPath, Buffer.from(data, 'base64'));
      console.log(`  ✓ Slide ${i + 1}/${c.slides}`);
    }

    pws.close();
    await bsend({ method: 'Target.closeTarget', params: { targetId } });
    console.log(`  Done: ${c.name}\n`);
  }

  bws.close();
  console.log('All carousels rendered!');
}

main().catch((err) => {
  console.error('FATAL:', err);
  process.exit(1);
});
