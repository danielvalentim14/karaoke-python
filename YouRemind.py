import pygame
import time
import re

def parse_lrc(file_path):
    lyrics = []
    # Expressão regular para encontrar o tempo no formato [mm:ss.xx]
    pattern = re.compile(r'\[(\d+):(\d+\.\d+)\](.*)')
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            match = pattern.match(line)
            if match:
                minutes = int(match.group(1))
                seconds = float(match.group(2))
                text = match.group(3).strip()
                
                # Converte tudo para segundos totais
                total_seconds = minutes * 60 + seconds
                lyrics.append((total_seconds, text))
    
    # Garante que as letras estejam em ordem cronológica
    return sorted(lyrics, key=lambda x: x[0])

def play_karaoke(music_file, lrc_file):
    # Inicializa o mixer do pygame
    pygame.mixer.init()
    pygame.mixer.music.load(music_file)
    
    lyrics = parse_lrc(lrc_file)
    
    print(f"Tocando: {music_file}...\n")
    pygame.mixer.music.play()
    
    start_time = time.time()
    
    for timestamp, text in lyrics:
        # Calcula quanto tempo falta para a próxima frase
        while True:
            elapsed_time = time.time() - start_time
            if elapsed_time >= timestamp:
                print(f">>> {text}")
                break
            time.sleep(0.01) # Pequena pausa para não sobrecarregar a CPU

    # Mantém o programa rodando até a música acabar
    while pygame.mixer.music.get_busy():
        time.sleep(1)

# --- CONFIGURAÇÃO ---
# Certifique-se de que os arquivos estão na mesma pasta do script
MUSICA = "- (000)nickelback - This Is How You Remind Me..mp3"
LETRA = "HowYou.lrc"

if __name__ == "__main__":
    try:
        play_karaoke(MUSICA, LETRA)
    except FileNotFoundError:
        print("Erro: Verifique se os nomes dos arquivos MP3 e LRC estão corretos.")
    except KeyboardInterrupt:
        pygame.mixer.music.stop()
        print("\nInterrompido pelo usuário.")
