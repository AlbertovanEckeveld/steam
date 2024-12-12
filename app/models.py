from dataclasses import dataclass
from typing import List, Optional

@dataclass
class UserProfile:
    steam_id: str
    display_name: str
    url_avatar_small: str
    url_avatar_medium: str
    url_avatar_full: str
    url_profile: str
    friend_list: Optional[List] = None
    game_list: Optional[List] = None

    def __str__(self):
        return self.steam_id

    def get_displayname(self) -> str:
        return self.display_name

    def get_avatar_small(self) -> str:
        return self.url_avatar_small

    def get_avatar_medium(self) -> str:
        return self.url_avatar_medium

    def get_avatar_full(self) -> str:
        return self.url_avatar_full

    def get_profile(self) -> str:
        return self.url_profile

    def get_friendlist(self) -> List:
        return self.friend_list

    def get_gamelist(self) -> List:
        return self.game_list
