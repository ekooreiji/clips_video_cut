"""
Integration Tests - Testes de Integração
"""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock


class TestPipelineIntegration:
    """Testes de integração do pipeline"""

    def test_pipeline_initialization(self):
        """Testa inicialização do pipeline"""
        from src.application.pipeline import VideoPipeline
        from src.domain.values.config import ProcessingConfig

        config = ProcessingConfig()
        pipeline = VideoPipeline(config=config)

        assert pipeline.config == config
        assert pipeline.scene_detector is not None
        assert pipeline.silence_detector is not None

    def test_pipeline_with_custom_config(self):
        """Testa pipeline com config customizada"""
        from src.application.pipeline import VideoPipeline
        from src.domain.values.config import ProcessingConfig, SilenceConfig

        config = ProcessingConfig()
        config.silence.enabled = True
        config.silence.db_threshold = -50

        pipeline = VideoPipeline(config=config)

        assert pipeline.config.silence.enabled is True
        assert pipeline.config.silence.db_threshold == -50


class TestBatchProcessorIntegration:
    """Testes de integração do batch processor"""

    def test_batch_processor_initialization(self):
        """Testa inicialização do batch processor"""
        from src.application.batch_processor import BatchProcessor
        from src.domain.values.config import ProcessingConfig

        config = ProcessingConfig()
        processor = BatchProcessor(config=config)

        assert processor.config == config
        assert processor.max_workers == 3

    def test_batch_processor_max_workers(self):
        """Testa limite de workers"""
        from src.application.batch_processor import BatchProcessor
        from src.domain.values.config import ProcessingConfig

        config = ProcessingConfig()
        config.output.max_workers = 5

        processor = BatchProcessor(config=config)

        assert processor.max_workers == 5


class TestSceneDetectorIntegration:
    """Testes de integração do scene detector"""

    def test_scene_detector_initialization(self):
        """Testa inicialização do scene detector"""
        from src.domain.use_cases.detect_scene import SceneDetector

        detector = SceneDetector()

        assert detector.min_clip_length == 10
        assert detector.opencv is not None


class TestSilenceDetectorIntegration:
    """Testes de integração do silence detector"""

    def test_silence_detector_initialization(self):
        """Testa inicialização do silence detector"""
        from src.domain.use_cases.detect_silence import SilenceDetector

        detector = SilenceDetector()

        assert detector.audio_adapter is not None


class TestExporterIntegration:
    """Testes de integração dos exporters"""

    def test_json_exporter(self, tmp_path):
        """Testa exportador JSON"""
        from src.infrastructure.exporters.json_exporter import JSONExporter

        exporter = JSONExporter()

        data = {
            "video": "test.mp4",
            "clips": [
                {"id": 1, "start": 0, "end": 10}
            ]
        }

        output_file = tmp_path / "output.json"
        exporter.export(data, output_file)

        assert output_file.exists()

        # Verificar conteúdo
        loaded = exporter.load(output_file)
        assert loaded["video"] == "test.mp4"
        assert len(loaded["clips"]) == 1


class TestUseCases:
    """Testes de integração dos use cases"""

    def test_sensitivity_levels(self):
        """Testa níveis de sensibilidade"""
        from src.domain.values.config import Sensitivity

        assert Sensitivity.LOW.value == 0.3
        assert Sensitivity.MEDIUM.value == 1.0
        assert Sensitivity.HIGH.value == 2.0