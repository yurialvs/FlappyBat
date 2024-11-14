import os

def salvar_recorde(pontuacao, nome):
    # Função para salvar o recorde do jogador no arquivo 'recordes.txt'
    try:
        # Verifica se a pasta de 'recorde' existe, caso contrário, cria
        if not os.path.exists("recorde"):
            os.makedirs("recorde")
        
        # Caminho do arquivo de recordes
        caminho_arquivo = os.path.join("recorde", "records.txt")
        
        # Verifica se o arquivo de recorde já existe
        if os.path.exists(caminho_arquivo):
            with open(caminho_arquivo, "r") as f:
                conteudo = f.read().strip()
                if conteudo:
                    partes = conteudo.split(":")
                    if len(partes) == 2:
                        recorde = int(partes[0])
                        recorde_nome = partes[1]
                    else:
                        recorde = 0
                        recorde_nome = ""
                else:
                    recorde = 0
                    recorde_nome = ""
        else:
            recorde = 0
            recorde_nome = ""
        
        # Se a pontuação do jogador for maior que o recorde, salva o novo recorde
        if pontuacao > recorde:
            with open(caminho_arquivo, "w") as f:
                f.write(f"{pontuacao}:{nome}")
            return pontuacao, nome
        
        return recorde, recorde_nome
    
    except Exception as e:
        print(f"Erro ao salvar o recorde: {e}")
        return 0, ""
