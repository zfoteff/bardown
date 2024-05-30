from stats.models.dao.game_statistics import GameStatistics as GameStatisticsDAO
from stats.models.dto.statistics import GameStatistics as GameStatisticsDTO


def foo():
    bar = GameStatisticsDAO()
    baz = GameStatisticsDTO()
    return bar, baz
