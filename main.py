import io

import MusicManager
import os
from dotenv import load_dotenv, find_dotenv
import pygame

from scripts.PlayButton import PlayButton
from scripts.PlaybackController import PlaybackController


def main():
    load_dotenv(find_dotenv())
    api_key = os.getenv("API_KEY")

    song = MusicManager.get_top_songs("s3nse1_snorlax", api_key)[0]
    song_audio = MusicManager.download_song(song)
    album_cover = MusicManager.get_image(song)
    song.cover = io.BytesIO(album_cover)

    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True

    white = (245, 240, 223)
    red = (204, 55, 40)
    blue = (14, 66, 95)

    album_cover = pygame.image.load(song.cover).convert()
    album_cover = pygame.transform.scale(album_cover, (280, 280))

    playback_controller = PlaybackController(song_audio)
    playback_controller.load()
    play_button = PlayButton(pygame.rect.Rect(500, 300, 75, 100), playback_controller)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        play_button.update()

        # Begin Rendering
        screen.fill(white)

        # Red Background Separator
        pygame.draw.polygon(screen, red, ((650, 0), (1280, 0), (1280, 720), (890, 720)))
        pygame.draw.aaline(screen, red, (649, 0), (889, 720))

        # Who Listens to this Song?
        pygame.draw.rect(screen, blue, (118, 35, 1065, 80))
        pygame.draw.rect(screen, blue, (108, 25, 1065, 80))
        pygame.draw.rect(screen, white, (111, 28, 1059, 74))
        courier_prime_60 = pygame.font.Font("./assets/CourierPrime-Bold.ttf", 60)
        screen.blit(courier_prime_60.render("WHO LISTENS TO THIS SONG?", True, blue), (180, 35))

        # Progress Bar
        pygame.draw.rect(screen, blue, (45, 666, 1210, 35))
        pygame.draw.rect(screen, blue, (35, 656, 1210, 35))

        # Album Cover
        pygame.draw.rect(screen, blue, (70, 180, 300, 300))
        pygame.draw.rect(screen, blue, (80, 190, 300, 300))

        screen.blit(album_cover, (80, 190, 100, 100))

        # Song Information
        space_mono_35 = pygame.font.Font("./assets/SpaceMono-Regular.ttf", 35)
        screen.blit(space_mono_35.render(song.title, True, blue), (70, 500))
        space_mono_25 = pygame.font.Font("./assets/SpaceMono-Regular.ttf", 25)
        screen.blit(space_mono_25.render(song.artist, True, blue), (70, 545))
        space_mono_15 = pygame.font.Font("./assets/SpaceMono-Regular.ttf", 20)
        screen.blit(space_mono_15.render(f"Plays: {song.total_plays}", True, blue), (73, 580))

        # Play Button
        play_button.render(screen)


        pygame.display.flip()
        clock.tick(60)

    playback_controller.unload()

    pygame.font.quit()
    pygame.quit()


if __name__ == '__main__':
    main()