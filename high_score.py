from menu import Points


class HighScoreScreen:
    """Displays all the high scores recorded from past game play"""
    def __init__(self, settings, screen, game_stats):
        # Score text is a list of titles representing text to display
        self.score_text = []
        self.score_text.append(Points(settings.bg_color, screen, 'High Scores'))
        for num, value in enumerate(game_stats.top_high_scores, 1):
            self.score_text.append(Points(settings.bg_color, screen, '(' + str(num) + ')  ' + str(value),
                                         text_color=(255, 255, 0)))

        # Place each line of text down the screen, in the center
        y_offset = settings.screen_height * 0.15
        for text in self.score_text:
            text.prep_image()
            text.image_rect.centerx = settings.screen_width / 2
            text.image_rect.centery = y_offset
            y_offset += settings.screen_height * 0.15

    def show_scores(self):
        """Blit all the high score related text to the screen"""
        for text in self.score_text:
            text.draw()
