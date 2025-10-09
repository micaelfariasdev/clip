import subprocess
import platform

def is_wsl() -> bool:
    """Verifica se o script está rodando dentro do WSL."""
    # O kernel do WSL contém 'microsoft' ou 'WSL' no nome da sua versão.
    uname_release = platform.uname().release.lower()
    return 'microsoft' in uname_release or 'wsl' in uname_release

def notify(title='Aviso', msg='Teste'):
    """
    Envia uma notificação de desktop nativa para Linux, Windows, ou WSL.
    """
    system = platform.system()

    try:
        if system == 'Windows':
            # 🪟 Rodando diretamente no Windows
            command = f'powershell -Command "New-BurntToastNotification -Text \'{title}\', \'{msg}\'"'
            subprocess.run(command, shell=True, check=True)

        elif system == 'Linux':
            if is_wsl():
                # 🐧+🪟 Rodando dentro do WSL
                # Chamamos o .exe do PowerShell do Windows a partir do Linux
                command = f'powershell.exe -Command "New-BurntToastNotification -Text \'{title}\', \'{msg}\'"'
                subprocess.run(command, shell=True, check=True)
            else:
                # 🐧 Rodando em um Linux nativo (com interface gráfica)
                subprocess.run(['notify-send', title, msg], check=True)
        else:
            print(f"Notificações não suportadas para o sistema: {system}")

    except (FileNotFoundError, subprocess.CalledProcessError) as e:
        print(f"Erro ao enviar notificação: {e}")
        if system == 'Windows' or is_wsl():
            print("-> Dica: Verifique se o módulo 'BurntToast' está instalado no PowerShell do seu Windows.")
        elif system == 'Linux':
            print("-> Dica: Verifique se o 'notify-send' (pacote libnotify-bin) está instalado no seu Linux.")


if __name__ == '__main__':
    print("Enviando notificação a partir do ambiente atual...")
    notify('Script Concluído', f'Executado com sucesso no {platform.system()}!')
    print("Script terminou.")