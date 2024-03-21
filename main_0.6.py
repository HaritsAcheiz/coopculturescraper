import sys
from datetime import date, timedelta, datetime
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
        sb.driver.uc_open_with_reconnect(self.target_url, reconnect_time=3)
        sb.click(f'div[data-date="{self.reserve_date}"]')

        found = False

        for page in range(2, 6):
            sb.wait_for_element_present('div.content > div')
            selectors = len(sb.find_elements('div.content > div'))
            for selector in range(1, selectors + 1):
                if self.hour in sb.get_text(f'div.content > div:nth-of-type({str(selector)})'):
                    found = True
                    break
            if found:
                sb.click(f'div.content > div:nth-of-type({str(selector)}) > div:nth-of-type(2) > button')
                break
            sb.click(f'a[href="#page-{page}"]')

        if found:
            for i in range(self.tickets):
                sb.click('span.input-group-addon.quantity.glyphicon.glyphicon-plus')
            sb.scroll_to_bottom()
            sb.driver.uc_click('button.btn.btn-primary.addtocart')
        else:
            print('Failed...ticket not found')

    def re_purchase(self, sb):
        sb.click('a.delcart', timeout=10)
        print('click del cart')
        sb.wait_for_element_clickable('button.btn.btn-red')
        sb.click('button.btn.btn-red')
        print('red button clicked!!!')
        sb.wait_for_element_clickable('div.row.ja-masthead.wrap')
        sb.go_back()
        sb.click(f'div[data-date="{self.reserve_date}"]')
        print('back to main page succesfully!!!')

        found = False
        for page in range(2, 6):
            sb.wait_for_element_present('div.content > div')
            selectors = len(sb.find_elements('div.content > div'))
            for selector in range(1, selectors + 1):
                if self.hour in sb.get_text(f'div.content > div:nth-of-type({str(selector)})'):
                    found = True
                    break
            if found:
                sb.click(f'div.content > div:nth-of-type({str(selector)}) > div:nth-of-type(2) > button')
                break
            sb.click(f'a[href="#page-{page}"]')

        if found:
            for i in range(self.tickets):
                sb.click('span.input-group-addon.quantity.glyphicon.glyphicon-plus')
            sb.scroll_to_bottom()
            sb.driver.uc_click('button.btn.btn-primary.addtocart')
        else:
            print('Failed...ticket not found')

    def remove_from_cart(self, sb):
        print(f'{6 * "="} press delcart {6 * "="}')
        sb.click('a.delcart')
        print(f'{6 * "="} click red button {6 * "="}')
        sb.sleep(0.2)
        sb.click('button.btn.btn-red')
        sb.is_element_present('div.row.ja-masthead.wrap')

    def click_turnstile_and_verify(self, sb):
        try:
            sb.wait_for_element_present('iframe[title="Widget containing a Cloudflare security challenge"]')
            sb.driver.uc_switch_to_frame('iframe[title="Widget containing a Cloudflare security challenge"]')
            sb.driver.uc_click("label.ctp-checkbox-label > span.mark")
        except:
            pass

    def crawl3(self, proxy):
        with SB(uc=True, proxy=proxy, multi_proxy=True, headless2=True) as sb:
            try:
                start = time.time()
                self.open_the_form_turnstile_page(sb)
                self.click_turnstile_and_verify(sb)
                try:
                    sb.wait_for_element_clickable('a.delcart', timeout=8)
                except Exception as e:
                    print(e)
                    self.open_the_form_turnstile_page(sb)
                    self.click_turnstile_and_verify(sb)
                processing_time = time.time() - start
                print(f'Processing time: {processing_time} second(s) using {proxy}')

                while datetime.today() <= datetime.strptime(self.reserve_date, "%d/%m/%Y"):
                    print(f'current date: {datetime.today()}',
                          f'reserve date: {datetime.strptime(self.reserve_date, "%d/%m/%Y")}')
                    print(f'{6 * "="} repurchase {6 * "="}')
                    start = time.time()
                    sb.sleep(840)
                    self.re_purchase(sb)
                    self.click_turnstile_and_verify(sb)
                    try:
                        sb.wait_for_element_clickable('a.delcart', timeout=8)
                    except Exception as e:
                        print(e)
                        self.open_the_form_turnstile_page(sb)
                        self.click_turnstile_and_verify(sb)
                    processing_time = time.time() - start
                    print(f'Processing time: {processing_time} second(s) using {proxy}')
            except Exception as e:
                print(e)

if __name__ == '__main__':
    sys.argv.append("-n")
    # target_url = "https://www.coopculture.it/it/prodotti/biglietto-colosseo-foro-romano-palatino_24h/"
    target_url = "https://ecm.coopculture.it/index.php?option=com_snapp&view=event&id=3793660E-5E3F-9172-2F89-016CB3FAD609&catalogid=B79E95CA-090E-FDA8-2364-017448FF0FA0&lang=it"
    reserve_date = '28/03/2024'
    # reserve_date = date.strftime(date.today() + timedelta(days=7), '%d/%m/%Y')
    hour = '16:10'
    tickets = 8
    print(f'Ticket date: {reserve_date}')
    print(f'Ticket hour: {hour}')
    print(f'Ticket qty: {tickets}')

    proxies = [
        # 'natlbogh:r0zualc0deql@192.46.200.121:5791',
        # 'natlbogh:r0zualc0deql@193.160.82.127:6099',
        # 'natlbogh:r0zualc0deql@130.180.234.80:7303',
        'natlbogh:r0zualc0deql@192.53.67.116:5665',
        'natlbogh:r0zualc0deql@192.53.66.161:6267',
        'natlbogh:r0zualc0deql@45.115.60.116:5845',
        # 'natlbogh:r0zualc0deql@179.61.172.25:6576'
    ]

    scraper = CCScraper(target_url=target_url, reserve_date=reserve_date, hour=hour, tickets=tickets)
    with ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(scraper.crawl3, proxies)


