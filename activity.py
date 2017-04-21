from olpcgames import activity
from gettext import gettext as _

class Activity(activity.PyGameActivity):
    """Your Sugar activity"""
    
    game_name = 'tetrismat:main'
    game_title = _('Tetris Mat')
    game_size = (1200,900)

