const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.setViewport({ width: 1400, height: 900 });

    const getScale = async (file) => {
        await page.goto('file:///Users/charlie/Desktop/Apps/Ops Suite/prototype/' + file);
        const rect = await page.evaluate(() => {
            const frame = document.querySelector('.device-frame');
            return frame ? frame.getBoundingClientRect() : null;
        });
        const containerRect = await page.evaluate(() => {
            const container = document.getElementById('main-view');
            return container ? container.getBoundingClientRect() : null;
        });
        const scale = await page.evaluate(() => {
            const frame = document.querySelector('.device-frame');
            return frame.style.transform;
        });
        console.log(`${file}: scale: ${scale}, frame width: ${rect.width}, height: ${rect.height}, container width: ${containerRect.width}, height: ${containerRect.height}`);
    };

    await getScale('index.html');
    await getScale('home.html');
    await getScale('flightlog.html');

    await browser.close();
})();
