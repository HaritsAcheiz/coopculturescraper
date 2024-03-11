from datetime import date, timedelta
from concurrent.futures import ThreadPoolExecutor
from seleniumbase import SB
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
        # sb.sleep(0.5)
        # selector = 1
        # page = 2
        # while not found:
        #     try:
        #         if self.hour in sb.get_text(f'div.content > div:nth-of-type({str(selector)})'):
        #             found = True
        #         else:
        #             selector += 1
        #             continue
        #     except NoSuchElementException as e:
        #         print('Move to next page...')
        #         sb.click(f'a[href="#page-{page}"]')
        #         selector = 1
        #         page += 1

        # sb.click(f'div.content > div:nth-of-type({selector}) > div:nth-of-type(2) > button')

        for page in range(2, 4):
            sb.wait_for_element_present('div.content > div')
            selectors = len(sb.find_elements('div.content > div'))
            for selector in range(1, selectors + 1):
                if self.hour in sb.get_text(f'div.content > div:nth-of-type({str(selector)})'):
                    found = True
                    break
            if found:
                sb.click(f'div.content > div:nth-of-type({str(selector)}) > div:nth-of-type(2) > button')
                break
            print('Move to next page...')
            sb.click(f'a[href="#page-{page}"]')

        if found:
            for i in range(self.tickets):
                sb.click('span.input-group-addon.quantity.glyphicon.glyphicon-plus')
            sb.scroll_to_bottom()
            sb.driver.uc_click('button.btn.btn-primary.addtocart')
        else:
            input('Failed...need to check')

        # for i in range(self.tickets):
        #     sb.click('span.input-group-addon.quantity.glyphicon.glyphicon-plus')
        #     # sb.sleep(uniform(1, 2))
        # sb.scroll_to_bottom()
        # sb.driver.uc_click('button.btn.btn-primary.addtocart')
        # time.sleep(3)

    def re_purchase(self, sb):
        print(f'{6 * "="} press delcart {6 * "="}')
        sb.click('a.delcart')
        print(f'{6 * "="} click red button {6 * "="}')
        sb.sleep(0.2)
        sb.click('button.btn.btn-red')
        sb.is_element_present('div.row.ja-masthead.wrap')
        sb.sleep(1)
        sb.go_back()
        sb.click(f'div[data-date="{self.reserve_date}"]')
        found = False
        # sb.sleep(0.5)
        for page in range(2, 4):
            sb.wait_for_element_present('div.content > div')
            selectors = len(sb.find_elements('div.content > div'))
            print(selectors)
            for selector in range(1, selectors + 1):
                print(sb.get_text(f'div.content > div:nth-of-type({str(selector)})'))
                print(self.hour in sb.get_text(f'div.content > div:nth-of-type({str(selector)})'))
                if self.hour in sb.get_text(f'div.content > div:nth-of-type({str(selector)})'):
                    found = True
                    break
            if found:
                sb.click(f'div.content > div:nth-of-type({str(selector)}) > div:nth-of-type(2) > button')
                break
            print('Move to next page...')
            sb.click(f'a[href="#page-{page}"]')

        if found:
            for i in range(self.tickets):
                sb.click('span.input-group-addon.quantity.glyphicon.glyphicon-plus')
            sb.scroll_to_bottom()
            sb.driver.uc_click('button.btn.btn-primary.addtocart')
        else:
            input('Failed...need to check')


    def click_turnstile_and_verify(self, sb):
        try:
            sb.driver.uc_switch_to_frame("iframe[title='Widget containing a Cloudflare security challenge']")
            sb.driver.uc_click("label.ctp-checkbox-label > span.mark")
        except Exception:
            pass
        # time.sleep(3)
        # sb.highlight("img#captcha-success", timeout=3.33)

    def crawl3(self, proxy):
        with SB(uc=True, proxy=proxy, multi_proxy=True) as sb:
            start = time.time()
            self.open_the_form_turnstile_page(sb)
            self.click_turnstile_and_verify(sb)
            processing_time = time.time() - start
            print(f'Processing time: {processing_time} second(s)')
            for _ in range(2):
                print(f'{6 * "="} sleep {6 * "="}')
                sb.sleep(20)
                print(f'{6 * "="} repurchase {6 * "="}')
                start = time.time()
                self.re_purchase(sb)
                self.click_turnstile_and_verify(sb)
                processing_time = time.time() - start
                print(f'Processing time: {processing_time} second(s)')

if __name__ == '__main__':
    target_url = "https://www.coopculture.it/it/prodotti/biglietto-colosseo-foro-romano-palatino_24h/"
    # reserve_date = '8/03/2024'
    reserve_date = date.strftime(date.today() + timedelta(days=7), '%d/%m/%Y')
    hour = '12:30'
    tickets = 10
    print(f'Ticket date: {reserve_date}')
    print(f'Ticket hour: {hour}')
    print(f'Ticket qty: {tickets}')

    proxies = ['natlbogh:r0zualc0deql@130.180.236.213:6218', 'natlbogh:r0zualc0deql@154.194.24.67:5677']
    scraper = CCScraper(target_url=target_url, reserve_date=reserve_date, hour=hour, tickets=tickets)
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.map(scraper.crawl3, proxies)

    # scraper.crawl3()


