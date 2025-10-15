import puppeteer from 'puppeteer';
import { readFileSync } from 'fs';
import { writeFileSync } from 'fs';

(async () => {
    const browser = await puppeteer.launch({
        headless: false,
        // args: ['--use-gl=egl', '--disable-gpu=false']
    });

    const page = await browser.newPage();

    // Load the scene.html from disk
    const html = readFileSync('./scene.html', 'utf8');
    await page.setContent(html, { waitUntil: 'load' });

    // Wait for render to finish
    await page.waitForFunction('window.renderDone === true');

    // Capture screenshot
    const buffer = await page.screenshot({ type: 'png' });
    writeFileSync('output.png', buffer);
    console.log('✅ Rendered output.png');

    await browser.close();
})();
