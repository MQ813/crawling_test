from web import crawling
from common.job import meas_run_time, mult_run

reput_db = {}

class Charactor:
    def __init__(self, name='', raiders=[], selenium=False):
        self.name = name
        self.raiders = raiders
        self.soup = None
        self.class_name = None
        self.level_item = None
        self.server = None
        self.source = crawling.get_source(f"https://lostark.game.onstove.com/Profile/Character/{self.name}",
                                          selenium=selenium)
        self.soup = None
        self.get_data()
        self.get_reput()

        # self.soup = crawling.get_soup(f"https://lostark.game.onstove.com/Profile/Character/{self.name}")
        # self.get_data()

    def __str__(self):
        return f"""
{self.name}<br>
서버      : {self.server}<br>
클래스    : {self.class_name}<br>
아이템레벨 : {self.level_item}<br>
like     : {self.get_reput()}<br>
"""

    # @meas_run_time
    def get_data(self):
        self.soup = crawling.get_soup(self.source)
        level_item = self.soup.select_one(
            "#lostark-wrapper > div > main > div > div.profile-ingame > div.profile-info > div.level-info2 > div.level-info2__item > span:nth-child(2)")
        if not level_item:
            return 0
        self.class_name = self.soup.select_one("#lostark-wrapper > div > main > div > div.profile-character-info > img")['alt']
        self.level_item = float(str(level_item.get_text()).replace('Lv.', '').replace(',', ''))
        self.server = self.soup.select_one("#lostark-wrapper > div > main > div > div.profile-character-info > span.profile-character-info__server").get_text()
        self.get_raiders_names()

    def get_raiders_names(self):
        n_raider = 1
        raiders = []
        while 1:
            raider = self.soup.select_one(f"#expand-character-list > ul > li:nth-child({n_raider}) > span > button > span")
            if raider is None:
                break
            raiders.append(str(raider.get_text()))
            n_raider += 1
        self.raiders = raiders

    def get_reput(self):
        global reput_db
        for raider in self.raiders:
            if raider in reput_db:
                return reput_db[raider]['reput']
        else:
            reput_db[self.name] = {'reput': 0, 'ip': set([])}
            return 0

        # try:
        #     return reput_db[self.name]['reput']
        # except KeyError:
        #     reput_db[self.name] = {'reput': 0, 'ip': set([])}
        #     return 0

    def add_reput(self, added_reput, ip):
        for raider in self.raiders:
            if raider in reput_db:
                if ip not in reput_db[raider]['ip']:
                    if added_reput == 'like':
                        added_num = 1
                    elif added_reput == 'hate':
                        added_num = -1
                    reput_db[raider]['reput'] += added_num
                    reput_db[raider]['ip'].add(ip)
                    return ''
                else:
                    return ' 한 IP에서 한번만 가능합니다. '


@meas_run_time
def get_all_raiders(main_charactor_name):
    main_charactor = Charactor(main_charactor_name)
    # main_charactor.get_data()
    print('* 대표캐릭터 *')
    print(main_charactor)
    raider = main_charactor.raiders
    print('* 원정대캐릭터 *')
    raider.remove(main_charactor_name)
    raider = raider
    raiders = mult_run(Charactor, raider)
    for charac in raiders:
        charac.get_data()
        print(charac)

