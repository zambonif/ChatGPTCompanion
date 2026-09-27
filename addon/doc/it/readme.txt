# ChatGPT Companion 0.1.2 — versione sperimentale

Di Fernando de Paula Zamboni. https://www.blog.fernandozamboni.com

Legge messaggi inviati, risposte e aggiornamenti accessibili sullo stato nella conversazione attiva di ChatGPT, senza spostare il focus. Usa voce e braille di NVDA. Interfaccia e documentazione in portoghese brasiliano, inglese, spagnolo, francese e italiano.

## Modifiche nella versione 0.1.2

Ignora avvisi e testi dell’interfaccia è attivo per impostazione predefinita. Rimuove il blocco finale noto sugli errori possibili seguito da “Risposta più recente”, dalla lettura automatica e dal comando di ripetizione. Non effettua sostituzioni globali: conserva frasi isolate, esempi tra virgolette e riferimenti all’interno della risposta. Il riconoscimento è testuale; se una risposta termina letteralmente con l’intero blocco, disattiva l’opzione per ascoltarlo. Altri piè di pagina non riconosciuti possono rimanere.

Una risposta precedente non viene più rimessa in coda quando compare un nuovo invio o quando una risposta già annunciata scompare e ricompare nell’albero di accessibilità. Le nuove installazioni usano un’alternativa dopo il silenzio di 3 secondi; le impostazioni esistenti vengono conservate. L’utente ha confermato la lettura automatica con questa alternativa in Chrome e nell’app Windows con la versione 0.1.1. Questo aggiornamento richiede ancora prove in entrambi gli ambienti prima della pubblicazione.

## Modifica nella versione 0.1.1

Corretta la ripetizione del messaggio inviato durante gli aggiornamenti della pagina. Ogni nuovo invio viene annunciato una volta; modifiche dello stesso testo o scomparse temporanee non generano un altro annuncio. Un nuovo invio con testo identico viene ancora riconosciuto. Per un invio silenzioso, disattiva Leggi i messaggi inviati e Conferma l’invio. Modificare un messaggio esistente senza aggiungerne un altro non provoca una nuova lettura automatica dell’invio.

## Installazione e prima prova
Apri fzChatGPTCompanion-0.1.2.nvda-addon, conferma l’installazione e riavvia NVDA quando richiesto. Compatibilità dichiarata: NVDA da 2025.1 a 2026.2; sono ancora necessarie prove reali su Windows. lastTestedNVDAVersion indica l’obiettivo di compatibilità del pacchetto sperimentale, non un test di esecuzione effettuato.

Inizia con una conversazione breve in Chrome su https://chatgpt.com. Attendi circa due secondi e invia una domanda semplice. Dovrebbero essere letti il tuo messaggio, gli avvisi riconosciuti e la risposta completata. La cronologia esistente non viene annunciata. Cambiare scheda, conversazione o applicazione stabilisce un nuovo riferimento; gli aggiornamenti ricevuti durante l’assenza non vengono annunciati al ritorno. Mantieni attiva la conversazione durante la prova.

Edge, Firefox, Brave e l’app ChatGPT per Windows sono obiettivi sperimentali. L’app deve esporre un documento con testo accessibile strutturato. Ogni ambiente richiede verifica. Non serve una chiave API di ChatGPT né un pagamento aggiuntivo per l’API.

## Impostazioni
Apri il menu NVDA, Preferenze, Impostazioni, ChatGPT Companion. Usa Tab, Spazio e le frecce, poi OK. Salva la configurazione di NVDA se il salvataggio all’uscita è disattivato.

- Attiva la lettura automatica: attiva o disattiva il monitoraggio.
- Leggi i messaggi inviati: legge il contenuto dopo la sua comparsa nella conversazione, non semplicemente dopo Invio.
- Conferma l’invio: se la lettura dei messaggi inviati è disattivata, annuncia solo “Messaggio inviato”. Disattiva entrambe le opzioni per un invio silenzioso.
- Leggi le risposte e Leggi gli aggiornamenti sullo stato: opzioni indipendenti.
- Risposta completa: predefinita; attende un controllo di invio riconosciuto e due secondi senza modifiche al testo.
- Nuovi paragrafi: sperimentale; legge paragrafi completi durante la generazione. Le revisioni del sito possono causare ripetizioni. Senza separazioni tra paragrafi può attendere la fine.
- Attesa dopo il completamento: da 1 a 10 secondi; predefinito 2.
- Alternativa dopo il silenzio: da 0 a 60 secondi; 0 la disattiva e il valore predefinito per le nuove installazioni è 3. Senza un controllo di generazione riconosciuto, un valore come 8 deduce la fine dopo il silenzio. Una pausa può provocare una lettura anticipata; non garantisce il completamento.

## Comandi
NVDA corrisponde a Insert o Bloc Maiusc secondo la configurazione. Modifica i comandi in Preferenze, Gesti e tasti di immissione, ChatGPT Companion.

- NVDA+Control+Shift+G: attiva o disattiva la lettura automatica.
- NVDA+Control+Shift+R: legge l’ultima risposta disponibile, anche parziale. Funziona con la lettura automatica disattivata.
- NVDA+Control+Shift+P: legge l’ultimo aggiornamento sullo stato disponibile.
- NVDA+Control+Shift+D: annuncia il numero di messaggi riconosciuti e lo stato del controllo di generazione.
- Control: interrompe la voce attuale secondo il normale comportamento di NVDA. Usa il comando G per impedire gli annunci successivi.

## Limiti e risoluzione dei problemi
“Pensiero” indica soltanto uno stato o un riepilogo esposto dall’interfaccia. Non recupera ragionamento interno, testo nascosto o contenuti non accessibili a NVDA. Riconosce intestazioni degli autori e controlli in cinque lingue; modifiche dell’interfaccia possono richiedere aggiornamenti. Immagini, allegati e formule non ricevono un’interpretazione speciale.

Se la diagnostica indica zero messaggi, verifica di averne inviato uno e prova la modalità navigazione con NVDA+Spazio; se necessario, prova Chrome o Edge. Se riconosce i messaggi ma non il controllo di generazione, usa la lettura manuale o l’alternativa dopo il silenzio. Le conversazioni oltre 250.000 caratteri vengono ignorate per limitare l’elaborazione; altre conversazioni lunghe possono comunque rallentare il lettore.

Gli annunci nativi delle regioni dinamiche di NVDA o del sito possono duplicare la voce. Se necessario, disattiva la lettura degli aggiornamenti del componente. Non sopprime globalmente gli annunci nativi. Per segnalare problemi, indica versione del browser o dell’app, versione di NVDA, lingua dell’interfaccia e diagnostica; non serve condividere la conversazione. Prima della pubblicazione prova cambio scheda, installazione, rimozione, salvataggio delle impostazioni e i quattro comandi.

## Privacy, licenza e distribuzione
Non accede a rete, cookie, password, appunti o file delle conversazioni. Elabora il testo accessibile in memoria mentre la conversazione è attiva, senza salvarlo né inviarlo. Sono escluse le schermate protette di Windows. NVDA conserva le impostazioni.

GNU GPL versione 2 o successiva, senza garanzia; vedi COPYING.txt. Progetto indipendente, non affiliato a OpenAI o NV Access. Il manifest.ini nella radice è in inglese; le traduzioni sono in locale. Prima dell’invio allo Store, verifica Windows e la compatibilità dichiarata e pubblica codice sorgente e un collegamento HTTPS diretto al pacchetto. La struttura del pacchetto non garantisce l’approvazione.
