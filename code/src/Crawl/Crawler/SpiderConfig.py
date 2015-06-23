__author__ = 'hanxuan'


class SpiderConfig(object):
    def __init__(self):
        self._domain_fetch_time_span = 1000  # in ms
        self._max_tasks = 20000
        self._max_threads = 1000
        self._seeds_path = ''

    @property
    def domain_fetch_time_span(self):
        return self._domain_fetch_time_span

    @property
    def max_tasks(self):
        return self._max_tasks

    @property
    def max_threads(self):
        return self._max_threads

    @property
    def seeds_path(self):
        return self._seeds_path

    @domain_fetch_time_span.setter
    def domain_fetch_time_span(self, value):
        self._domain_fetch_time_span = value

    @max_tasks.setter
    def max_tasks(self, value):
        self._max_tasks = value

    @max_threads.setter
    def max_threads(self, value):
        self._max_threads = value

    @seeds_path.setter
    def seeds_path(self, value):
        self._seeds_path = value

if __name__ == '__main__':
    SpiderConfig()