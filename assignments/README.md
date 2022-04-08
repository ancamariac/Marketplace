Nume: Ciuciu Anca-Maria
Grupă: 333 AA

# Tema 1

Organizare
-
1. Explicație pentru soluția aleasă:

Problema rezolvata de aceasta tema este una de tip Multi Producers - Multi Consumers, continand fisierele consumer.py, producer.py si marketplace.py. 
Cele doua tipuri de produse ce se regasesc in marketplace sunt Tea si Coffee - urmand sa fie vandute de catre producatori, consumatorilor. Pentru a 
rezerva produsele ce urmeaza a fi cumparate, fiecare cumparator detine cate un cos de cumparaturi din care poate adauga sau elimina obiecte. 
Consider aceasta tema utila deoarece am invatat cum se folosesc elementele de sincronizare in python. Consider ca aceasta problema ar fi putut fi implementata
mai eficient acoperind mai multe edge cases.

Implementare
-
Intregul enunt al problemei a fost implementat. 

Clasa Producer - in aceasta clasa se va genera lista de produse pe care o are un producator. Un obiect din aceasta lista este caracterizat de un produs (product[0]),
cantitatea (product[1]) si timpul de asteptare (product[2]). Astfel, se va publica fiecare produs ca fiind disponibil in marketplace, dupa aceasta operatie urmand un apel
de sleep ce reprezinta timpul de asteptare. Totodata, se tine cont de faptul ca producatorul sa nu depaseasca limita de produse din marketplace, acest caz fiind tratat de
timpul de asteptare republish_wait_time.

Clasa Consumer - functionalitatea clasei consta in asignarea unui ID pentru cosul de cumparaturi, adaugarea sau eliminarea obiectelor din cos si plasarea unei comenzi. Consumatorul
analizeaza lista de comenzi, urmarind tipurile acestora (add/remove) si obtine produsul si cantitatea. Fiecare produs va fi adaugat pe rand in cosul de cumparaturi, analizandu-se totodata
si cazul in care produsul inca nu a fost publicat, apelandu-se sleep cu retry_wait_time. Stergerea unui element din cos presupune intrarea acestuia din nou in marketplace,
pentru a fi disponibil pentru alti consumatori. In cele din urma, se executa comanda cu place_order si se afiseaza produsele cumparate. 

Clasa Marketplace - are rolul de a asigna cate un ID pentru un producator (len(self.producers)) cat si pentru un cart (len(self.consumers)) prin intermediul metodelor 
register_producer() si new_cart(), urmand ca la final, dimensiunea listelor sa se incrementeze prin append. Pentru cele doua metode s-a folosit Lock pentru a evita problemele
ce tin de concurenta. Adaugarea produsului in cos este posibila datorita metodei add_to_cart care efectueaza si stergerea acestuia din lista producatorului, returnandu-se True. 
Daca produsul solicitat nu exista se va returna False. Problema ce tine de o posibila solicitare de adaugare a aceluiasi obiect a doua thread-uri a fost rezolvata cu un alt Lock.
Eliminarea produsului din cart si actualizarea acestuia ca fiind disponil s-a realizat cu metoda remove_from_cart care presupune folosirea unui alt lock, din acelasi motiv. 
Prin intermediul metodei place_order se va obtine lista de produse din cosul consumatorului. 

Resurse utilizate
-
https://ocw.cs.pub.ro/courses/asc/laboratoare

Git
-
1. Link către repo-ul de git
https://github.com/ancamariac/Arhitectura-Sistemelor-de-Calcul/tree/main/assignments/1-marketplace