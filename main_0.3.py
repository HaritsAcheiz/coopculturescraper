from random import uniform
from typing import List
from seleniumbase import SB
from seleniumbase.common.exceptions import NoSuchElementException, TextNotVisibleException
from dataclasses import dataclass, field
import time

@dataclass
class CCScraper:
    target_url: str
    reserve_date: str
    hours: List[str] = field(default_factory=lambda: [])

    def open_the_form_turnstile_page(self, sb, hour):
        sb.maximize_window()
        sb.driver.uc_open_with_reconnect(self.target_url, reconnect_time=2.7)
        sb.click('div.col-xl-3.d-none.d-lg-block')
        sb.click(f'div[data-date="{self.reserve_date}"]')
        found = False
        selector = 1
        page = 2
        while not found:
            try:
                sb.assert_text(hour, f'div.content > div:nth-of-type({selector})', timeout=0.5)
                found = True
                selector = 1
                page = 2
            except TextNotVisibleException:
                selector += 1
                continue
            except NoSuchElementException as e:
                print(e)
                sb.click(f'a[href="#page-{page}"]')
                page += 1

        sb.click(f'div.content > div:nth-of-type({selector}) > div:nth-of-type(2)')

        for i in range(10):
            sb.click('span.input-group-addon.quantity.glyphicon.glyphicon-plus')
            sb.sleep(uniform(1, 2))
        sb.scroll_to_bottom()
        sb.click('button.btn.btn-primary.addtocart')
        time.sleep(3)
        # sb.switch_to_frame("iframe[title='Widget containing a Cloudflare security challenge']")
        # sb.click("label.ctp-checkbox-label > span.mark")
        # sb.driver.uc_click("label.ctp-checkbox-label > span.mark")
        # time.sleep(3)

    def click_turnstile_and_verify(self, sb):
        sb.driver.uc_switch_to_frame("iframe[title='Widget containing a Cloudflare security challenge']")
        sb.driver.uc_click("label.ctp-checkbox-label > span.mark")
        # sb.highlight("img#captcha-success", timeout=3.33)

    def crawl3(self):
        with SB(uc=True) as sb:
            for hour in self.hours:
                print(hour)
                self.open_the_form_turnstile_page(sb, hour=hour)
                self.click_turnstile_and_verify(sb)
            sb.sleep(100)

if __name__ == '__main__':
    target_url = "https://www.coopculture.it/it/prodotti/audiovideoguida-del-colosseo-con-biglietto-colosseo-foro-romano-palatino_h24/"
    reserve_date = '6/03/2024'
    hours = ['12:30', '13:30']
    scraper = CCScraper(target_url=target_url, reserve_date=reserve_date)
    scraper.hours = hours
    scraper.crawl3()