from seleniumbase import SB
from seleniumbase.common.exceptions import NoSuchElementException
from dataclasses import dataclass
import time

@dataclass
class CCScraper:
    target_url: str
    reserve_date: str
    hour: str
    tickets: int

    def open_the_form_turnstile_page(self, sb):
        sb.maximize_window()
        sb.driver.uc_open_with_reconnect(self.target_url, reconnect_time=2.7)
        sb.click('div.col-xl-3.d-none.d-lg-block')
        sb.click(f'div[data-date="{self.reserve_date}"]')
        found = False
        selector = 1
        page = 2
        while not found:
            try:
                if self.hour in sb.get_text(f'div.content > div:nth-of-type({str(selector)})'):
                    found = True
                else:
                    selector += 1
                    continue
            except NoSuchElementException as e:
                print('Move to next page...')
                sb.click(f'a[href="#page-{page}"]')
                selector = 1
                page += 1

        sb.click(f'div.content > div:nth-of-type({selector}) > div:nth-of-type(2) > button')

        for i in range(self.tickets):
            sb.click('span.input-group-addon.quantity.glyphicon.glyphicon-plus')
            # sb.sleep(uniform(1, 2))
        sb.scroll_to_bottom()
        sb.driver.uc_click('button.btn.btn-primary.addtocart')
        # time.sleep(3)


    def click_turnstile_and_verify(self, sb):
        sb.driver.uc_switch_to_frame("iframe[title='Widget containing a Cloudflare security challenge']")
        try:
            sb.driver.uc_click("label.ctp-checkbox-label > span.mark")
        except NoSuchElementException:
            pass
        processing_time = time.time() - start
        print(f'Processing time: {processing_time} second(s)')
        sb.sleep(50)
        # time.sleep(3)
        # sb.highlight("img#captcha-success", timeout=3.33)

    def crawl3(self):
        with SB(uc=True) as sb:
            self.open_the_form_turnstile_page(sb)
            self.click_turnstile_and_verify(sb)


if __name__ == '__main__':
    start = time.time()
    target_url = "https://www.coopculture.it/it/prodotti/audiovideoguida-del-colosseo-con-biglietto-colosseo-foro-romano-palatino_h24/"
    reserve_date = '12/03/2024'
    hour = '11:30'
    tickets = 10
    scraper = CCScraper(target_url=target_url, reserve_date=reserve_date, hour=hour, tickets=tickets)
    scraper.crawl3()
