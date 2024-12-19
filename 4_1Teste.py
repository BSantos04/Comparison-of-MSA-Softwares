import sys

nucleotideos = set(["A", "T", "G", "C", "U", "R", "Y", "S", "W", "K", "M", "B", "D", "H", "V", "N", "-"])

aminoacidos = set(["A", "R", "N", "D", "C", "E", "Q", "G","H", "I", "L", "K", "M", "F", "P", "S", "T", "W", "Y", "V", "-"])


def verificar_sequencia(ficheiro):
    try:
        with open(ficheiro, 'r') as f:
            conteudo = f.read().strip().upper()

        conteudo = "".join(linha.strip() for linha in conteudo.splitlines() if not linha.startswith('>')).upper()

        caracteres_ficheiro = set(conteudo)

        nao_nucleotideos = caracteres_ficheiro - nucleotideos

        if not nao_nucleotideos:
            print("O ficheiro contém sequências de aminoácidosa.")
        else:
            nao_aminoacidos = caracteres_ficheiro - aminoacidos
            if not nao_aminoacidos:
                print("O ficheiro contém sequências de proteínas.")
            else:
                if nao_aminoacidos and nao_nucleotideos:
                    print("O ficheiro não contém sequências de aminoácidos nem proteínas.")

    except FileNotFoundError:
        print("Erro: Ficheiro não encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    if len(sys.argv)!=2:
        print("Usage: python3 {path/to/script.py} {path/to/file.fasta}")
    else:
        ficheiro = sys.argv[1]
        verificar_sequencia(ficheiro)

