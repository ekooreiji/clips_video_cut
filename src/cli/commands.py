"""
CLI Commands - Definição de comandos CLI

Sistema CLI para automação de cortes em vídeos usando Click.
"""

import click
import sys
from pathlib import Path
from typing import Optional

from src.application.pipeline import VideoPipeline
from src.domain.values.config import ProcessingConfig
from src.common.exceptions import (
    VideoNotFoundError,
    VideoCorruptedError,
    FFmpegNotFoundError,
)
from src.common.utils.logger import setup_logger, get_logger

logger = get_logger(__name__)


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """Video Clips Automation - Sistema CLI para cortes automáticos de vídeo"""
    pass


@cli.command()
@click.argument("video_path", type=click.Path(exists=True))
@click.option(
    "--output-dir",
    "-o",
    type=click.Path(),
    help="Diretório de saída para os clips"
)
@click.option(
    "--visual-cut/--no-visual-cut",
    default=True,
    help="Ativar detecção de mudança de cena"
)
@click.option(
    "--sensitivity",
    type=click.Choice(["low", "medium", "high"], case_sensitive=False),
    default="medium",
    help="Sensibilidade para detecção de cena"
)
@click.option(
    "--remove-silence",
    is_flag=True,
    help="Remover trechos de silêncio do áudio"
)
@click.option(
    "--silence-db",
    type=int,
    default=-40,
    help="Threshold de dB para detecção de silêncio"
)
@click.option(
    "--silence-duration",
    type=float,
    default=0.5,
    help="Duração mínima do silêncio em segundos"
)
@click.option(
    "--normalize-audio",
    is_flag=True,
    help="Normalizar volume do áudio"
)
@click.option(
    "--generate-subtitles",
    is_flag=True,
    help="Gerar legendas automáticas com Whisper"
)
@click.option(
    "--export-subtitles",
    type=click.Choice(["srt", "vtt"], case_sensitive=False),
    help="Exportar legendas em formato SRT ou VTT"
)
@click.option(
    "--burn-subtitles",
    is_flag=True,
    help="Inserir legendas no vídeo"
)
@click.option(
    "--no-audio",
    is_flag=True,
    help="Indicar que o vídeo não tem áudio"
)
@click.option(
    "--destroy",
    is_flag=True,
    help="Excluir arquivo original após processamento"
)
@click.option(
    "--config",
    "-c",
    type=click.Path(exists=True),
    help="Arquivo de configuração JSON"
)
@click.option(
    "--batch",
    "-b",
    type=click.Path(exists=True, file_okay=False),
    help="Processar todos os vídeos da pasta"
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Ativar logging verboso"
)
def process(
    video_path: str,
    output_dir: Optional[str],
    visual_cut: bool,
    sensitivity: str,
    remove_silence: bool,
    silence_db: int,
    silence_duration: float,
    normalize_audio: bool,
    generate_subtitles: bool,
    export_subtitles: Optional[str],
    burn_subtitles: bool,
    no_audio: bool,
    destroy: bool,
    config: Optional[str],
    batch: Optional[str],
    verbose: bool,
):
    """Processar vídeo para gerar clips automáticos"""
    
    # Setup logging
    level = "DEBUG" if verbose else "INFO"
    setup_logger(level=level)
    
    # Carregar configuração
    if config:
        processing_config = ProcessingConfig.from_json(Path(config))
    else:
        processing_config = ProcessingConfig()
        
        # Debug
        logger.info(f"CLI visual_cut flag: {visual_cut}")
        
        # Aplicar opções da CLI
        processing_config.visual_cut.enabled = visual_cut
        processing_config.visual_cut.sensitivity = {
            "low": 0.3, "medium": 1.0, "high": 2.0
        }[sensitivity]
        
        processing_config.silence.enabled = remove_silence
        processing_config.silence.db_threshold = silence_db
        processing_config.silence.min_duration = silence_duration
        
        processing_config.normalization.enabled = normalize_audio
        processing_config.subtitles.enabled = generate_subtitles
        processing_config.subtitles.burn = burn_subtitles
        
        if export_subtitles:
            processing_config.subtitles.format = export_subtitles
        
        processing_config.output.keep_original = not destroy
    
    # Criar pipeline
    pipeline = VideoPipeline(config=processing_config)
    
    try:
        if batch:
            # Processamento em lote
            videos = list(Path(batch).glob("*.mp4"))
            videos.extend(Path(batch).glob("*.mkv"))
            videos.extend(Path(batch).glob("*.avi"))
            videos.extend(Path(batch).glob("*.mov"))
            videos.extend(Path(batch).glob("*.webm"))
            
            click.echo(f"Processando {len(videos)} vídeos...")
            
            for video in videos:
                try:
                    result = pipeline.process_single(video, output_dir)
                    click.echo(f"✓ {video.name}: {result['clips_detected']} clips")
                except Exception as e:
                    click.echo(f"✗ {video.name}: {str(e)}", err=True)
        
        else:
            # Processamento único
            video_path_obj = Path(video_path)
            
            # Validar entrada
            if not video_path_obj.exists():
                click.echo(f"Erro: Arquivo não encontrado: {video_path}", err=True)
                sys.exit(1)
            
            if not video_path_obj.is_file():
                click.echo(f"Erro: Caminho inválido: {video_path}", err=True)
                sys.exit(1)
            
            valid_extensions = {'.mp4', '.mkv', '.avi', '.webm', '.mov'}
            if video_path_obj.suffix.lower() not in valid_extensions:
                click.echo(f"Erro: Formato não suportado: {video_path_obj.suffix}", err=True)
                click.echo(f"Formatos suportados: {', '.join(valid_extensions)}", err=True)
                sys.exit(1)
            
            # Validar tamanho do arquivo (máximo 10GB)
            max_size_bytes = 10 * 1024 * 1024 * 1024  # 10GB
            file_size = video_path_obj.stat().st_size
            if file_size > max_size_bytes:
                size_gb = file_size / (1024 ** 3)
                click.echo(f"Erro: Arquivo muito grande: {size_gb:.2f}GB", err=True)
                click.echo(f"Tamanho máximo permitido: 10GB", err=True)
                sys.exit(1)
            
            # Log do tamanho do arquivo
            size_mb = file_size / (1024 ** 2)
            logger.info(f"Processando arquivo: {video_path_obj.name} ({size_mb:.1f}MB)")
            
            result = pipeline.process_single(video_path_obj, output_dir)
            
            click.echo(f"Video: {video_path}")
            click.echo(f"Clips detectados: {result['clips_detected']}")
            click.echo(f"Arquivo de relatório: {result['report_path']}")
            
            if destroy:
                click.echo("Arquivo original excluído.")
    
    except VideoNotFoundError as e:
        click.echo(f"Erro: {e}", err=True)
        sys.exit(1)
    except VideoCorruptedError as e:
        click.echo(f"Erro: {e}", err=True)
        sys.exit(1)
    except FFmpegNotFoundError as e:
        click.echo(f"Erro: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        logger.exception("Erro inesperado")
        click.echo(f"Erro: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("video_path", type=click.Path(exists=True))
@click.option(
    "--output-dir",
    "-o",
    type=click.Path(),
    help="Diretório de saída"
)
@click.option(
    "--json",
    "json_output",
    type=click.Path(),
    help="Salvar resultado em arquivo JSON"
)
def preview(
    video_path: str,
    output_dir: Optional[str],
    json_output: Optional[str],
):
    """Pré-visualizar pontos de corte sem processar"""
    
    setup_logger(level="INFO")
    
    pipeline = VideoPipeline()
    
    try:
        result = pipeline.preview(Path(video_path), output_dir)
        
        click.echo(f"Pontos de corte detectados:")
        
        for clip in result["clips"]:
            click.echo(
                f"  {clip['id']}: {clip['start_time']:.2f}s - "
                f"{clip['end_time']:.2f}s ({clip['reason']})"
            )
        
        click.echo(f"Total: {result['clips_detected']} clips")
        
        if json_output:
            import json
            with open(json_output, 'w') as f:
                json.dump(result, f, indent=2)
            click.echo(f"Resultado salvo em: {json_output}")
    
    except Exception as e:
        click.echo(f"Erro: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    help="Criar arquivo de exemplo"
)
def init_config(output: Optional[str]):
    """Criar arquivo de configuração de exemplo"""
    
    config = ProcessingConfig()
    
    if output:
        config.save_json(Path(output))
        click.echo(f"Configuração salva em: {output}")
    else:
        config.save_json(Path("config.example.json"))
        click.echo("Configuração salva em: config.example.json")


@cli.command()
def gui():
    """Abrir interface gráfica (GUI)"""
    
    try:
        from src.gui.main_window import main
        main()
    except ImportError:
        click.echo("Erro: PyQt6 não está instalado", err=True)
        click.echo("Instale com: pip install PyQt6", err=True)
        sys.exit(1)


if __name__ == "__main__":
    cli()