% Importazione delle classi
:- include('class_value/condotta.pl').
:- include('class_value/punto_irrigazione.pl').

% Regola per la gerarchia delle classi (Ereditarietà)
prop(X, type, C) :- prop(S, subClassOf, C), prop(X, type, S).

% Utility: Estrae vicini e gestisce liste (Invariate per compatibilità)
suddividi_prefisso_suffisso(X, L, Prefix1, Suffix) :-
    select(X, Prefix, Suffix, L),
    delete(X, Prefix, Prefix1).

select(Elem, Prefix, Suffix, List) :-
    member(Elem, List),
    position(Elem, List, Position),
    split_at(Position, List, Prefix, Suffix).

position(Elem, [Elem|_], 1).
position(Elem, [_|Tail], Position) :- position(Elem, Tail, Position1), Position is Position1 + 1.

split_at(1, [Elem|Tail], [Elem], Tail).
split_at(Position, [Head|Tail], [Head|Prefix], Suffix) :-
    Position1 is Position - 1,
    split_at(Position1, Tail, Prefix, Suffix).

delete(_, [], []) :- !.
delete(Elem, [Elem|Tail], Result) :- !, delete(Elem, Tail, Result).
delete(Elem, [Head|Tail], [Head|Result]) :- \+ (Elem = Head), delete(Elem, Tail, Result).

% Identifica se un nodo è un campo irriguo
primo_campo(Nodo) :- prop(Nodo, type, campo).
find_first(List, First) :- findall(Elem, (member(Elem, List), primo_campo(Elem)), [First|_]), !.
find_first(_, []).