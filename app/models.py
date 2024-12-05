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

    def get_displayname(self):
        return self.display_name

    def get_avatar_small(self):
        return self.url_avatar_small

    def get_avatar_medium(self):
        return self.url_avatar_medium

    def get_avatar_full(self):
        return self.url_avatar_full

    def get_profile(self):
        return self.url_profile

    def get_friendlist(self):
        return self.friend_list
