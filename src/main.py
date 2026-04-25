import click
from pathlib import Path

@click.command()
@click.argument("path_video", required=True, type=click.Path(exists=True))
@click.option("--output_video", default="./output_clip/", type=click.Path(), help="Caminho para salvar o vídeo editado")
@click.option("--remove-silence", is_flag=True, help="Remove o silencio do vídeo")
@click.option("--remove-audio", is_flag=True, help="Remove o audio do vídeo")
@click.option("--remove-background-noise", is_flag=True, help="Remove background noise from the video")
def init_informations(path_video, output_video, remove_silence, remove_audio, remove_background_noise):
    # Converte para Path manualmente
    path_video = Path(path_video)
    output_video = Path(output_video)
    return [path_video, output_video, remove_silence, remove_audio, remove_background_noise]


if __name__ == "__main__":
    valor = init_informations(standalone_mode=False)
    print(valor)
