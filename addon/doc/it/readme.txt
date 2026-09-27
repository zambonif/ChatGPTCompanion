# ChatGPT Companion

Di Fernando de Paula Zamboni. Versione 0.1.3 (beta).

Componente aggiuntivo NVDA per leggere nuovi messaggi nel sito e nell’app Windows di ChatGPT. Può leggere automaticamente le risposte, leggere o confermare i messaggi inviati e annunciare aggiornamenti accessibili sullo stato senza spostare il focus.

## Obiettivo

Seguire la conversazione senza tornare continuamente dal campo di scrittura all’ultima risposta. Continui a usare account e interfaccia abituali, senza un altro client, chiavi API o pagamenti API aggiuntivi. Voce e braille seguono le impostazioni di NVDA.

Altri componenti possono offrire funzioni simili. Questo progetto si concentra sugli annunci automatici nell’interfaccia esistente, con controlli indipendenti per messaggi inviati, risposte e stato. È un aiuto facoltativo, non sostituisce i miglioramenti di accessibilità di ChatGPT stesso.

## Installazione e utilizzo

Scarica ChatGPTCompanion-0.1.3.nvda-addon, aprilo con NVDA attivo, conferma l’installazione e riavvia NVDA. Richiede NVDA 2026.2 o successivo; la versione API dichiarata come testata è 2026.2. Versioni future possono richiedere una verifica di compatibilità.

Download: https://github.com/zambonif/ChatGPTCompanion/releases

Codice sorgente e segnalazioni: https://github.com/zambonif/ChatGPTCompanion

Apri una conversazione in Chrome o nell’app Windows, attendi un momento e invia una domanda. L’autore ha confermato la lettura in entrambi gli ambienti con versioni precedenti. Le correzioni di 0.1.3 richiedono ancora prove reali. Edge, Firefox e Brave sono ulteriori obiettivi sperimentali.

La cronologia non viene annunciata all’apertura. Si monitora solo la conversazione attiva. Si ricordano fino a otto contesti durante la sessione NVDA: tornando a una conversazione riconosciuta, una risposta arrivata durante l’assenza può essere annunciata. Non c’è lettura in background. Riavviare NVDA o alternare il monitoraggio con il relativo comando cancella questa memoria.

## Impostazioni

Menu NVDA, Preferenze, Impostazioni, ChatGPT Companion. Gli aggiornamenti conservano le preferenze. Salva la configurazione se il salvataggio automatico è disattivato.

- Attiva la lettura automatica: attiva o disattiva il monitoraggio.
- Leggi i messaggi inviati: legge il contenuto dopo la sua comparsa.
- Conferma l’invio: dice solo “Messaggio inviato” se la lettura dei messaggi inviati è disattivata. Disattiva entrambe le opzioni per un invio silenzioso.
- Leggi le risposte e Leggi gli aggiornamenti sullo stato: opzioni indipendenti.
- Ignora avvisi e testi dell’interfaccia: attivo per impostazione predefinita; filtra i blocchi finali riconosciuti. Disattivalo se rimuove un esempio letterale del piè di pagina alla fine della risposta.
- Risposta completa: attende un controllo di completamento riconosciuto e testo stabile. Nuovi paragrafi è un’alternativa sperimentale durante la generazione.
- Attesa dopo il completamento: da 1 a 10 secondi; predefinito 2.
- Alternativa dopo il silenzio: da 0 a 60 secondi; predefinito 3 nelle nuove installazioni. Usata quando il controllo di generazione non viene riconosciuto. Una pausa lunga può sembrare la fine; aumenta il valore se la lettura inizia troppo presto. 0 disattiva l’alternativa.

## Comandi

NVDA significa Insert o Bloc Maiusc secondo la configurazione. Riassegna i comandi in Gesti e tasti di immissione, ChatGPT Companion.

- NVDA+Control+Shift+G: attiva o disattiva la lettura automatica.
- NVDA+Control+Shift+R: legge l’ultima risposta disponibile, eventualmente parziale. Se una domanda nuova attende risposta, la precedente non viene usata al suo posto.
- NVDA+Control+Shift+P: legge l’ultimo aggiornamento accessibile sullo stato.
- NVDA+Control+Shift+D: aggiorna la diagnostica dei messaggi recenti e del controllo di generazione.
- Control: interrompe la voce attuale. Usa G per impedire gli annunci automatici successivi.

## Problemi e limiti

Se non legge, controlla Leggi le risposte, prova R e D e verifica l’alternativa dopo il silenzio. La diagnostica conta il tratto recente, non tutta la cronologia. Prova la modalità navigazione con NVDA+Spazio se la conversazione non viene riconosciuta.

Dipende dal testo e dalle intestazioni degli autori esposti a NVDA. Se la risposta attuale non è disponibile, lo comunica invece di usare deliberatamente una risposta precedente memorizzata. Modifiche dell’interfaccia possono influire sul riconoscimento. Non interpreta in modo speciale immagini, allegati o formule. Lo stato indica avvisi accessibili, non il ragionamento interno.

0.1.3 cerca dalla fine e non esclude più cronologie oltre 250.000 caratteri. Risposte singole enormi o fornitori senza navigazione per intestazioni possono ancora causare lentezza o lettura incompleta. La ricerca alternativa copre fino a 2.560 righe dalla fine.

Gli annunci nativi possono duplicare la voce; disattiva la lettura dello stato se necessario. Segnala versioni di NVDA e browser/app, lingua, diagnostica e passi per riprodurre il problema. Non serve condividere conversazioni private.

## Novità e privacy

0.1.3 migliora conversazioni lunghe e cronologie con campi modificabili, aggiorna il testo da ripetere e mantiene lo stato durante cambi temporanei di focus. La documentazione utente è stata riorganizzata e il manifesto punta al progetto con NVDA 2026.2 come minimo.

Non effettua connessioni di rete né accede a password, cookie o appunti. Il testo accessibile rimane temporaneamente in memoria, senza essere salvato o inviato. NVDA conserva le preferenze. Le schermate protette sono escluse.

GNU GPL versione 2 o successiva, senza garanzia. Progetto indipendente, non affiliato a OpenAI o NV Access. Interfaccia e aiuto in inglese, portoghese brasiliano, spagnolo, francese e italiano.
