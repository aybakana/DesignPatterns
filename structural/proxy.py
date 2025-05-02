"""
Proxy Design Pattern

This pattern provides a surrogate or placeholder for another object to control access to it.
Example demonstrates a video streaming service with access control and caching.
"""
from abc import ABC, abstractmethod
from time import sleep
from typing import Dict, Optional


class Video:
    """Resource class"""
    def __init__(self, id: str, title: str):
        self.id = id
        self.title = title
        self.content = f"Content for {title}"


class VideoDownloader(ABC):
    """Subject interface"""
    @abstractmethod
    def get_video(self, id: str) -> Optional[Video]:
        pass


class RealVideoDownloader(VideoDownloader):
    """Real Subject"""
    def __init__(self):
        self.videos = {
            "1": Video("1", "Introduction to Python"),
            "2": Video("2", "Design Patterns"),
            "3": Video("3", "Advanced Python Topics")
        }

    def get_video(self, id: str) -> Optional[Video]:
        video = self.videos.get(id)
        if video:
            print(f"\nDownloading video: {video.title}")
            # Simulate network delay
            sleep(2)
            return video
        return None


class VideoDownloaderProxy(VideoDownloader):
    """Proxy"""
    def __init__(self, downloader: RealVideoDownloader):
        self._downloader = downloader
        self._cache: Dict[str, Video] = {}
        self._access_rights = {
            "user": ["1", "2"],      # Regular user can access videos 1 and 2
            "admin": ["1", "2", "3"]  # Admin can access all videos
        }

    def check_access(self, user_role: str, video_id: str) -> bool:
        """Check if user has access to the video"""
        allowed_videos = self._access_rights.get(user_role, [])
        return video_id in allowed_videos

    def get_video(self, id: str, user_role: str = "user") -> Optional[Video]:
        # Check access rights
        if not self.check_access(user_role, id):
            print(f"\nAccess denied for video {id}. Required role: admin")
            return None

        # Check cache
        if id in self._cache:
            print(f"\nRetrieving video from cache: {self._cache[id].title}")
            return self._cache[id]

        # Download video
        video = self._downloader.get_video(id)
        if video:
            # Cache for future requests
            self._cache[id] = video
            return video
        return None


def main():
    # Create a proxy
    real_downloader = RealVideoDownloader()
    proxy = VideoDownloaderProxy(real_downloader)

    # Regular user access
    print("=== Regular User Access ===")
    
    # First access - should download
    print("\nFirst request for Video 1:")
    proxy.get_video("1", "user")
    
    # Second access - should use cache
    print("\nSecond request for Video 1:")
    proxy.get_video("1", "user")
    
    # Try to access restricted video
    print("\nTrying to access restricted Video 3:")
    proxy.get_video("3", "user")

    # Admin access
    print("\n=== Admin Access ===")
    
    # Admin can access all videos
    print("\nAdmin requesting Video 3:")
    proxy.get_video("3", "admin")


if __name__ == "__main__":
    main()
