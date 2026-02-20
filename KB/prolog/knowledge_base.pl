% Importazione del setup
:- include('setup.pl').
:- dynamic prop/3.
:- multifile prop/3.
:- discontiguous prop/3.

/**
 * REGOLE PER A* (Path Finding Idrico)
 */

% Calcola la distanza (euristica) tra due punti della rete
distanza_nodi(X, Y, S) :- 
    prop(X, latitudine, L1), prop(Y, latitudine, L2), 
    prop(X, longitudine, G1), prop(Y, longitudine, G2), 
    S is sqrt((L1 - L2)^2 + (G1 - G2)^2).

% Trova i campi vicini collegati dalla stessa condotta
vicini_campo(Campo, Vicini) :- 
    prop(Campo, type, campo), 
    prop(Campo, condotte, Condotte), 
    vicini_condotte_campo(Campo, Condotte, Vicini).

vicini_condotte_campo(_, [], []).
vicini_condotte_campo(Campo, [C1|C2], Vicini) :- 
    prop(C1, nodi, Nodi),
    suddividi_prefisso_suffisso(Campo, Nodi, P, S),
    reverse(P, P1),
    find_first(P1, V1),
    find_first(S, V2),
    vicini_condotte_campo(Campo, C2, ViciniResto),
    append(ViciniResto, [V1, V2], Vicini).

/**
 * REGOLE PER CSP (Ottimizzazione Irrigazione)
 */

% Inizializza il problema CSP: definisce i campi e i litri d'acqua possibili
% Chiamato da: self.prolog.init_IrrigationCSP()
init_IrrigationCSP(Dati) :-
    findall(C, prop(C, type, campo), ListaCampi),
    % Per ogni campo, definiamo un dominio di litri (es: 0, 10, 20, 30)
    map_campi_domini(ListaCampi, Dati).

map_campi_domini([], []).
map_campi_domini([C|Resto], [C-[0, 10, 20, 30] | DatiResto]) :- 
    map_campi_domini(Resto, DatiResto).

% Valuta quanto è 'buona' una distribuzione d'acqua
% Chiamato da: self.prolog.valutazione_benessere_piante(Assegnamento)
valutazione_benessere_piante(Assegnamento, Score) :-
    % Logica semplificata: più acqua diamo (fino a un limite), più lo score è alto
    findall(V, member(_-V, Assegnamento), Valori),
    sum_list(Valori, Score).

/**
 * DATI DI ESEMPIO (Fatti della Base di Conoscenza)
 */

% Definizione Condotte
prop(tubo_principale_1, type, condotta_principale).
prop(tubo_principale_1, nodi, [serbatoio, campo_nord, campo_sud]).
prop(tubo_principale_1, portata_max, 100).

% Definizione Campi
prop(campo_nord, type, campo).
prop(campo_nord, condotte, [tubo_principale_1]).
prop(campo_nord, latitudine, 10).
prop(campo_nord, longitudine, 20).

prop(campo_sud, type, campo).
prop(campo_sud, condotte, [tubo_principale_1]).
prop(campo_sud, latitudine, 50).
prop(campo_sud, longitudine, 60).