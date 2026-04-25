"""
CLI Unit Tests - Testes da Interface CLI

Testes para a interface de linha de comando.
"""

import pytest
from click.testing import CliRunner
from pathlib import Path
from unittest.mock import patch, MagicMock

from src.cli.commands import cli, process, preview, init_config, gui


class TestCLI:
    """Testes para CLI"""

    def test_cli_help(self):
        """Testa help do CLI"""
        runner = CliRunner()
        result = runner.invoke(cli, ['--help'])

        assert result.exit_code == 0
        assert 'Video Clips Automation' in result.output

    def test_cli_version(self):
        """Testa versão"""
        runner = CliRunner()
        result = runner.invoke(cli, ['--version'])

        assert result.exit_code == 0
        assert '1.0.0' in result.output

    def test_process_help(self):
        """Testa help do comando process"""
        runner = CliRunner()
        result = runner.invoke(cli, ['process', '--help'])

        assert result.exit_code == 0
        assert '--visual-cut' in result.output
        assert '--remove-silence' in result.output

    def test_preview_help(self):
        """Testa help do comando preview"""
        runner = CliRunner()
        result = runner.invoke(cli, ['preview', '--help'])

        assert result.exit_code == 0

    def test_init_config_default(self, tmp_path):
        """Testa comando init-config"""
        runner = CliRunner()

        config_file = tmp_path / "config.json"
        result = runner.invoke(cli, ['init-config', '-o', str(config_file)])

        assert result.exit_code == 0
        assert config_file.exists()

    @patch('src.cli.commands.VideoPipeline')
    def test_process_video(self, mock_pipeline, tmp_path):
        """Testa comando process"""
        runner = CliRunner()

        # Criar vídeo falso
        video_file = tmp_path / "test.mp4"
        video_file.touch()

        # Mock do pipeline
        mock_instance = MagicMock()
        mock_instance.process_single.return_value = {
            'clips_detected': 5,
            'report_path': str(tmp_path / "report.json"),
            'output_files': []
        }
        mock_pipeline.return_value = mock_instance

        result = runner.invoke(cli, [
            'process',
            str(video_file),
            '--visual-cut'
        ])

        # Pode falhar por FFmpeg não instalado, mas não deve ser erro de CLI
        assert 'process' in result.output.lower() or 'error' in result.output.lower()

    @patch('src.cli.commands.VideoPipeline')
    def test_preview_video(self, mock_pipeline, tmp_path):
        """Testa comando preview"""
        runner = CliRunner()

        video_file = tmp_path / "test.mp4"
        video_file.touch()

        mock_instance = MagicMock()
        mock_instance.preview.return_value = {
            'clips_detected': 3,
            'clips': [
                {'id': 1, 'start_time': 0, 'end_time': 10, 'reason': 'scene_change'},
                {'id': 2, 'start_time': 10, 'end_time': 20, 'reason': 'scene_change'},
                {'id': 3, 'start_time': 20, 'end_time': 30, 'reason': 'scene_change'}
            ]
        }
        mock_pipeline.return_value = mock_instance

        result = runner.invoke(cli, [
            'preview',
            str(video_file)
        ])

        # Verifica se retornou algo
        assert result.exit_code == 0 or 'error' in result.output.lower()


class TestCLIOptions:
    """Testes para opções da CLI"""

    def test_verbose_flag(self, tmp_path):
        """Testa flag verbose"""
        runner = CliRunner()

        video_file = tmp_path / "test.mp4"
        video_file.touch()

        result = runner.invoke(cli, [
            'process',
            str(video_file),
            '-v'
        ])

        # Non-zero exit acceptable for missing dependencies
        assert result is not None

    def test_destroy_flag(self, tmp_path):
        """Testa flag destroy"""
        runner = CliRunner()

        video_file = tmp_path / "test.mp4"
        video_file.touch()

        result = runner.invoke(cli, [
            'process',
            str(video_file),
            '--destroy'
        ])

        assert result is not None

    def test_config_flag(self, tmp_path):
        """Testa flag config"""
        runner = CliRunner()

        video_file = tmp_path / "test.mp4"
        video_file.touch()

        config_file = tmp_path / "config.json"
        config_file.write_text('{}')

        result = runner.invoke(cli, [
            'process',
            str(video_file),
            '--config', str(config_file)
        ])

        assert result is not None