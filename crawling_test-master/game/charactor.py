from web import crawling
from common.job import meas_run_time, mult_run


class Charactor:
    def __init__(self, name='', raiders=[], selenium=False):
        self.name = name
        self.raiders = []
        self.soup = None
        self.class_name = None
        self.level_item = None
        self.source = crawling.get_source(f"https://lostark.game.onstove.com/Profile/Character/{self.name}",
                                          selenium=selenium)
        self.soup = None
        # self.soup = crawling.get_soup(f"https://lostark.game.onstove.com/Profile/Character/{self.name}")
        # self.get_data()

    def __str__(self):
        return f"{self.name}: {self.class_name}, {self.level_item}"

    # @meas_run_time
    def get_data(self):
        self.soup = crawling.get_soup(self.source)
        # self.soup = crawling.get_soup(f"https://lostark.game.onstove.com/Profile/Character/{self.name}")
        self.class_name = self.soup.select_one("#lostark-wrapper > div > main > div > div.profile-character-info > img")['alt']
        level_item = self.soup.select_one("#lostark-wrapper > div > main > div > div.profile-ingame > div.profile-info > div.level-info2 > div.level-info2__item > span:nth-child(2)")
        self.level_item = float(str(level_item.get_text()).replace('Lv.', '').replace(',', ''))
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

@meas_run_time
def get_all_raiders(main_charactor_name):
    main_charactor = Charactor(main_charactor_name)
    main_charactor.get_data()
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

