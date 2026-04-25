"""
Testes Unitários de Entidades

Testes para as entidades do domínio.
"""

import pytest
from pathlib import Path

from src.domain.entities.video import VideoDocument, VideoMetadata
from src.domain.entities.clip import ClipSegment, ClipReason


class TestVideoMetadata:
    """Testes para VideoMetadata"""

    def test_create_metadata(self):
        """Testa criação de metadata"""
        metadata = VideoMetadata(
            width=1920,
            height=1080,
            fps=30.0,
            codec="h264",
            duration=120.5,
            has_audio=True,
            audio_codec="aac",
            audio_channels=2,
            audio_sample_rate=48000
        )

        assert metadata.width == 1920
        assert metadata.height == 1080
        assert metadata.fps == 30.0
        assert metadata.codec == "h264"

    def test_metadata_defaults(self):
        """Testa valores padrão"""
        metadata = VideoMetadata(
            width=1920,
            height=1080,
            fps=30.0,
            codec="h264"
        )

        assert metadata.bitrate is None
        assert metadata.duration == 0.0
        assert metadata.has_audio is True


class TestVideoDocument:
    """Testes para VideoDocument"""

    def test_create_document(self, tmp_path):
        """Testa criação de documento"""
        video_path = tmp_path / "test.mp4"
        video_path.touch()

        doc = VideoDocument(path=video_path)

        assert doc.path == video_path
        assert doc.name == "test"
        assert doc.extension == ".mp4"

    def test_is_valid_format(self, tmp_path):
        """Testa validação de formato"""
        video_path = tmp_path / "test.mp4"
        video_path.touch()

        doc = VideoDocument(path=video_path)

        assert doc.is_valid_format() is True

    def test_invalid_format(self, tmp_path):
        """Testa formato inválido"""
        video_path = tmp_path / "test.txt"
        video_path.touch()

        doc = VideoDocument(path=video_path)

        assert doc.is_valid_format() is False

    def test_output_directory(self, tmp_path):
        """Testa diretório de saída"""
        video_path = tmp_path / "test.mp4"
        video_path.touch()

        doc = VideoDocument(path=video_path)

        expected = tmp_path / "clips"
        assert doc.output_directory == expected


class TestClipSegment:
    """Testes para ClipSegment"""

    def test_create_clip(self):
        """Testa criação de clip"""
        clip = ClipSegment(
            id=1,
            start_time=0.0,
            end_time=10.5
        )

        assert clip.id == 1
        assert clip.start_time == 0.0
        assert clip.end_time == 10.5

    def test_duration(self):
        """Testa duração"""
        clip = ClipSegment(
            id=1,
            start_time=5.0,
            end_time=15.0
        )

        assert clip.duration == 10.0

    def test_reason_default(self):
        """Testa razão padrão"""
        clip = ClipSegment(
            id=1,
            start_time=0.0,
            end_time=10.0
        )

        assert clip.reason == ClipReason.SCENE_CHANGE

    def test_to_dict(self):
        """Testa conversão para dict"""
        clip = ClipSegment(
            id=1,
            start_time=5.0,
            end_time=15.0,
            reason=ClipReason.SCENE_CHANGE,
            scene_score=125.5
        )

        data = clip.to_dict()

        assert data["id"] == 1
        assert data["start_time"] == 5.0
        assert data["duration"] == 10.0
        assert data["reason"] == "scene_change"