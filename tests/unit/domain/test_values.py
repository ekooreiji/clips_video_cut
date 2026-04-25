"""
Testes de Valores - Value Objects

Testes para os value objects do domínio.
"""

import pytest

from src.domain.values.timestamp import Timestamp
from src.domain.values.config import (
    ProcessingConfig,
    VisualCutConfig,
    SilenceConfig,
    Sensitivity,
)


class TestTimestamp:
    """Testes para Timestamp"""

    def test_create_timestamp(self):
        """Testa criação de timestamp"""
        ts = Timestamp(seconds=125.5)

        assert ts.seconds == 125.5
        assert ts.milliseconds == 125500

    def test_formatted(self):
        """Testa formatação HH:MM:SS.mmm"""
        ts = Timestamp(seconds=3725.5)  # 1h 2m 5.5s

        assert "01:02:05.500" in ts.formatted

    def test_srt_format(self):
        """Testa formatação SRT"""
        ts = Timestamp(seconds=3725.5)

        assert "01:02:05,500" in ts.srt_format

    def test_from_frame(self):
        """Testa criação a partir de frame"""
        ts = Timestamp.from_frame(150, 30.0)

        assert ts.seconds == 5.0

    def test_add(self):
        """Testa soma de timestamps"""
        ts1 = Timestamp(seconds=10.0)
        ts2 = Timestamp(seconds=5.0)

        result = ts1 + ts2

        assert result.seconds == 15.0

    def test_sub(self):
        """Testa subtração de timestamps"""
        ts1 = Timestamp(seconds=10.0)
        ts2 = Timestamp(seconds=5.0)

        result = ts1 - ts2

        assert result.seconds == 5.0

    def test_eq(self):
        """Testa igualdade"""
        ts1 = Timestamp(seconds=10.0)
        ts2 = Timestamp(seconds=10.001)

        assert ts1 == ts2

    def test_lt(self):
        """Testa comparação menor que"""
        ts1 = Timestamp(seconds=10.0)
        ts2 = Timestamp(seconds=15.0)

        assert ts1 < ts2


class TestProcessingConfig:
    """Testes para ProcessingConfig"""

    def test_default_config(self):
        """Testa configuração padrão"""
        config = ProcessingConfig()

        # Visual Cut
        assert config.visual_cut.enabled is True
        assert config.visual_cut.sensitivity == 1.0

        # Silence
        assert config.silence.enabled is False
        assert config.silence.db_threshold == -40

        # Subtitles
        assert config.subtitles.enabled is False
        assert config.subtitles.format == "srt"

        # Output
        assert config.output.keep_original is True
        assert config.output.max_workers == 3

    def test_change_sensitivity(self):
        """Testa mudança de sensibilidade"""
        config = ProcessingConfig()

        config.visual_cut.sensitivity = 2.0

        assert config.visual_cut.sensitivity == 2.0

    def test_enable_silence(self):
        """Testa habilitação de silêncio"""
        config = ProcessingConfig()

        config.silence.enabled = True
        config.silence.db_threshold = -50
        config.silence.min_duration = 1.0

        assert config.silence.enabled is True
        assert config.silence.db_threshold == -50
        assert config.silence.min_duration == 1.0

    def test_to_dict(self):
        """Testa conversão para dicionário"""
        config = ProcessingConfig()

        data = config.to_dict()

        assert "processing" in data
        assert "output" in data

    def test_from_json(self, tmp_path):
        """Testa carregamento de JSON"""
        import json

        config_data = {
            "processing": {
                "visual_cut": {
                    "enabled": True,
                    "sensitivity": 2.0,
                    "sample_rate": 3
                },
                "silence_removal": {
                    "enabled": True,
                    "db_threshold": -50,
                    "min_duration": 1.0
                },
                "normalization": {
                    "enabled": True
                }
            },
            "subtitles": {
                "enabled": True,
                "format": "vtt",
                "burn": True,
                "whisper_model": "small"
            },
            "output": {
                "format": "mp4",
                "quality": "high",
                "keep_original": False,
                "max_workers": 5
            },
            "logging": {
                "level": "DEBUG",
                "file": "debug.log"
            }
        }

        config_file = tmp_path / "config.json"
        with open(config_file, "w") as f:
            json.dump(config_data, f)

        config = ProcessingConfig.from_json(config_file)

        assert config.visual_cut.sensitivity == 2.0
        assert config.silence.enabled is True
        assert config.subtitles.format == "vtt"
        assert config.output.max_workers == 5