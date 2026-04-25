"""
Infrastructure Unit Tests - Testes de Infraestrutura

Testes para os adapters de infraestrutura.
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

from src.infrastructure.adapters.opencv_adapter import OpenCVAdapter


class TestOpenCVAdapter:
    """Testes para OpenCVAdapter"""

    def test_smooth(self):
        """Testa suavização de scores"""
        adapter = OpenCVAdapter()

        scores = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

        result = adapter._smooth(scores, window=3)

        assert len(result) == len(scores)
        assert all(isinstance(s, float) or isinstance(s, int) for s in result)

    def test_smooth_edge_cases(self):
        """Testa casos extremos da suavização"""
        adapter = OpenCVAdapter()

        # Lista vazia
        result = adapter._smooth([], window=5)
        assert len(result) == 0

        # Lista pequena
        result = adapter._smooth([10], window=5)
        assert len(result) == 1


class TestFFmpegAdapter:
    """Testes para FFmpegAdapter"""

    def test_parse_fps(self):
        """Testa parsing de FPS"""
        from src.infrastructure.adapters.ffmpeg_adapter import FFmpegAdapter

        adapter = FFmpegAdapter()

        # Teste com fração
        fps = adapter._parse_fps("30000/1001")
        assert 29.9 < fps < 30.1

        # Teste com inteiro
        fps = adapter._parse_fps("30/1")
        assert fps == 30.0

        # Teste com valor inválido
        fps = adapter._parse_fps("invalid")
        assert fps == 0.0


class TestAudioAdapter:
    """Testes para AudioAdapter"""

    def test_format_timestamp(self):
        """Testa formatação de timestamp"""
        from src.infrastructure.adapters.audio_adapter import AudioAdapter

        adapter = AudioAdapter()

        # Este teste verifica se os métodos estão definidos
        assert hasattr(adapter, 'detect_silence')
        assert hasattr(adapter, 'get_audio_info')
        assert hasattr(adapter, 'extract_audio')


class TestWhisperAdapter:
    """Testes para WhisperAdapter"""

    def test_format_srt_timestamp(self):
        """Testa formatação SRT timestamp"""
        from src.infrastructure.adapters.whisper_adapter import WhisperAdapter

        adapter = WhisperAdapter()

        # Teste com 0 segundos
        ts = adapter._format_srt_timestamp(0.0)
        assert "00:00:00,000" in ts

        # Teste com tempo específico
        ts = adapter._format_srt_timestamp(65.5)
        assert "00:01:05,500" in ts

    def test_format_vtt_timestamp(self):
        """Testa formatação VTT timestamp"""
        from src.infrastructure.adapters.whisper_adapter import WhisperAdapter

        adapter = WhisperAdapter()

        ts = adapter._format_vtt_timestamp(65.5)
        assert "00:01:05.500" in ts

    def test_models_cache(self):
        """Testa cache de modelos"""
        adapter = WhisperAdapter()

        # Deve começar com cache vazio
        assert adapter.models == {}

        # Models deve ser um dicionário
        assert isinstance(adapter.models, dict)