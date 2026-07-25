import asyncio
from threading import Thread

from winrt.windows.media.control import (
    GlobalSystemMediaTransportControlsSessionManager
)


class SpotifyListener:
    def __init__(self, callback):
        self.callback = callback

        self.spotify_open = False
        self.spotify_session = None

        self.thread = None
        self.loop = None


    def start(self):
        self.thread = Thread(
            target=self.run,
            daemon=True
        )
        self.thread.start()


    def run(self):
        asyncio.run(self.main())


    def get_spotify_session(self, manager):
        for session in manager.get_sessions():
            if "spotify" in session.source_app_user_model_id.lower():
                return session

        return None


    async def on_song_changed(self, session, args):
        info = await session.try_get_media_properties_async()

        if self.callback:
            self.callback(info)


    def add_song_listener(self, session):
        session.add_media_properties_changed(
            lambda sender, args:
            asyncio.run_coroutine_threadsafe(
                self.on_song_changed(sender, args),
                self.loop
            )
        )


    async def on_sessions_changed(self, manager, args):
        session = self.get_spotify_session(manager)

        is_open = session is not None

        if is_open != self.spotify_open:
            self.spotify_open = is_open

            if session:
                self.spotify_session = session

                if self.callback:
                    self.callback("OPEN", session)

                self.add_song_listener(session)

            else:
                self.spotify_session = None

                if self.callback:
                    self.callback("CLOSE", None)


    def sessions_changed_handler(self, sender, args):
        asyncio.run_coroutine_threadsafe(
            self.on_sessions_changed(sender, args),
            self.loop
        )


    # ==============================
    # CONTROLES DE SPOTIFY
    # ==============================

    def run_command(self, coroutine):
        """
        Ejecuta comandos desde cualquier hilo
        """
        if self.loop:
            asyncio.run_coroutine_threadsafe(
                coroutine,
                self.loop
            )


    async def play_pause(self):
        """
        Pausa o reproduce Spotify
        """
        if self.spotify_session:
            await self.spotify_session.try_toggle_play_pause_async()


    async def next_song(self):
        """
        Canción siguiente
        """
        if self.spotify_session:
            await self.spotify_session.try_skip_next_async()


    async def previous_song(self):
        """
        Canción anterior
        """
        if self.spotify_session:
            await self.spotify_session.try_skip_previous_async()


    # Métodos públicos para llamar fácilmente

    def toggle_play_pause(self):
        self.run_command(
            self.play_pause()
        )


    def next(self):
        self.run_command(
            self.next_song()
        )


    def previous(self):
        self.run_command(
            self.previous_song()
        )


    async def main(self):
        self.loop = asyncio.get_running_loop()

        manager = await GlobalSystemMediaTransportControlsSessionManager.request_async()

        session = self.get_spotify_session(manager)

        self.spotify_open = session is not None

        if session:
            self.spotify_session = session
            self.add_song_listener(session)


        manager.add_sessions_changed(
            self.sessions_changed_handler
        )

        while True:
            await asyncio.sleep(3600)
