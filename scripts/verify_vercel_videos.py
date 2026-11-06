import asyncio
from playwright.async_api import async_playwright

async def verify():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        print("Navigating to https://capivara-club-hot.vercel.app/painel...")
        await page.goto("https://capivara-club-hot.vercel.app/painel", timeout=60000, wait_until="networkidle")

        # Check if login modal or bypass is needed or if already logged in / localStorage master session
        # Let's set the master user auth in localStorage if needed:
        await page.evaluate('''() => {
            const user = { email: "diseguro20@gmail.com", name: "Diego Segura", role: "admin", access: "full" };
            localStorage.setItem("capivara_user", JSON.stringify(user));
            localStorage.setItem("capivara_logged_in", "true");
        }''')

        # Navigate or switch tab to tutoriais
        print("Clicking tutoriais tab...")
        await page.evaluate('''() => {
            if (typeof window.openPage === "function") {
                window.openPage("tutoriais");
            } else if (typeof window.switchTab === "function") {
                window.switchTab("tutoriais");
            }
        }''')
        await asyncio.sleep(3)

        # Inspect video elements
        videos_info = await page.evaluate('''() => {
            const vids = Array.from(document.querySelectorAll("video"));
            return vids.map((v, i) => {
                const sources = Array.from(v.querySelectorAll("source")).map(s => s.src);
                return {
                    index: i + 1,
                    currentSrc: v.currentSrc || v.src,
                    sources: sources,
                    readyState: v.readyState,
                    networkState: v.networkState,
                    error: v.error ? v.error.message || v.error.code : null,
                    paused: v.paused
                };
            });
        }''')

        print(f"Found {len(videos_info)} video elements:")
        for v in videos_info:
            print(f"Video #{v['index']}: currentSrc={v['currentSrc']} readyState={v['readyState']} sources={v['sources']} error={v['error']}")

        # Attempt to play first video to ensure stream buffers
        play_result = await page.evaluate('''async () => {
            const v = document.querySelector("video");
            if (!v) return { ok: false, error: "no video found" };
            try {
                // muted playback so browser won't block autoplay
                v.muted = true;
                await v.play();
                await new Promise(r => setTimeout(r, 2000));
                return {
                    ok: true,
                    currentTime: v.currentTime,
                    duration: v.duration,
                    paused: v.paused,
                    currentSrc: v.currentSrc
                };
            } catch(e) {
                return { ok: false, error: e.toString() };
            }
        }''')
        print(f"Playback test on video #1: {play_result}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(verify())
