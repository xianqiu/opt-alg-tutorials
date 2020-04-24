import os
from pathlib import Path
import json
import time

from selenium import webdriver
from PIL import Image


class GifResult(object):
    """
    计算过程可视化. 结果保存为gif图片.
    """

    def __init__(self, tours, locations):
        """
        :param tours: list, e.g. [(1, 2), (2, 3), (3, 4) ...]
        :param locations: list, e.g. [(x0, y0), (x1, y1), (x2, y2), ... ]
        """
        self._tours = tours
        self._locations = locations
        self._index = 0
        self._url = "file://" + os.path.abspath('./web/tsp.html')
        self._browser = None
        self._pic_folder = Path('temp')
        self._pic_names = []

    def _init(self):
        if not self._pic_folder.exists():
            self._pic_folder.mkdir()
        # 请自行下载对应操作系统的chrome driver, 然后放到项目文件夹
        # https://chromedriver.storage.googleapis.com/index.html?path=81.0.4044.69/
        self._browser = webdriver.Chrome(executable_path='./chromedriver')
        self._browser.set_window_size(800, 600)
        self._browser.get(self._url)

    def _clean_folder(self):
        for pic_name in self._pic_names:
            filepath = self._pic_folder / pic_name
            if filepath.exists():
                os.remove(filepath)
        self._pic_folder.rmdir()

    def _update_tour_view(self, tour):
        """ 把tour保存成js文件.
        :param tour: e.g. [(1, 2), (2, 3), (3, 4), ....]
        """
        data_js = [{'line': ["%.6f,%.6f" % (self._locations[pair[0]][0], self._locations[pair[0]][1]),
                             "%.6f,%.6f" % (self._locations[pair[1]][0], self._locations[pair[1]][1])]}
                   for pair in tour]
        path = Path('web') / 'data_tour.js'
        var_name = 'S.data.tour'
        with open(path, 'w', encoding='utf-8') as f:
            f.write('%s = %s;' % (var_name, json.dumps(data_js)))

    def _capture(self):
        """ 截图并保存.
        """
        self._browser.refresh()
        pic_name = '%d.png' % self._index
        self._browser.save_screenshot('%s/%s' % (self._pic_folder, pic_name))
        self._pic_names.append(pic_name)
        self._index += 1

    def _done(self):
        self._to_gif()
        self._browser.quit()
        self._clean_folder()

    def _to_gif(self):
        frames = [Image.open(self._pic_folder / pic_name)
                  .convert('RGB')
                  .convert('P', palette=Image.ADAPTIVE)
                  for pic_name in self._pic_names]
        frames += [frames[-1]] * 10
        frames[0].save('tour.gif',
                       format='GIF',
                       append_images=frames[1:],
                       save_all=True,
                       duration=300,
                       loop=0)

    def format(self, sleep=2):
        self._init()
        for tour in self._tours:
            self._update_tour_view(tour)
            time.sleep(sleep)
            self._capture()
        self._done()
