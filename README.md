# acronym-helper
Un piccolo script Python per la ricerca e la visualizzazione rapida di acronimi assieme alla loro versione estesa, utile durante lo studio per reperire velocemente alcuni significati utili. Esempio:
```
$ python3 ah.py --file filename.csv
```

https://user-images.githubusercontent.com/61554895/168433599-795ccbc0-6536-4561-98a4-fe2a6853403f.mp4


Per motivi di convenienza si può anche usare un alias come `alias ah='python3 /path/to/ah.py --file /path/to/file.csv'` da inserire dentro `.bashrc`. Per cancellare il testo basta usare `backspace` per eliminare l'ultimo carattere o `canc` per eliminare tutto.

Per gli acronimi segnati con il simbolo `(!)` è anche disponibile una descrizione; per visualizzarla basta premere il tasto `invio`.

Gli argomenti sono:

`--show <num>`: Quanti suggerimenti di acronimi simili vengono mostrati; di default è 5

`--col <color>`: Il colore del primo match, quello più simile al testo digitato

`--noscroll`: Il terminale viene completamente pulito invece di scorrere un tot

L'unica dipendenza esterna è [click](https://github.com/pallets/click), per l'uso di `click.getchar()`. Per installarla è sufficiente fare: `python3 -m pip install click`.

Nella repo è anche incluso un file di acronimi relativi ad un esame di telecomunicazioni che sto svolgendo, `acronimi.csv`, si può testare anche con quello.
