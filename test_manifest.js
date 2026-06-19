const puppeteer = require('puppeteer');
(async () => {
    const browser = await puppeteer.launch({headless: true});
    const page = await browser.newPage();
    
    // Set localStorage BEFORE navigating
    await page.goto('file:///Users/charlie/Desktop/Apps/Ops Suite/prototype/manifest.html');
    await page.evaluate(() => {
        localStorage.setItem('ops_suite_flight_sent', 'true');
        localStorage.setItem('ops_suite_sim_route', JSON.stringify([{id:'RWI',lat:0,lon:0},{id:'ECU',lat:1,lon:1}]));
    });
    // Reload so scripts run with localStorage set
    await page.reload();
    
    // Wait for a bit
    await page.waitForTimeout(1000);
    
    // Check if the container has children
    const html = await page.evaluate(() => {
        const c = document.getElementById('dynamic-manifest-container');
        return c ? c.innerHTML : 'No container found';
    });
    
    console.log("HTML inside container:");
    console.log(html);
    
    await browser.close();
})();
