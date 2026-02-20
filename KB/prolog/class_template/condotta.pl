/* Classe condotta
 * * Contiene i seguenti attributi:
 * - nome: identificativo della tubazione
 * - nodi: lista dei punti/campi collegati dalla condotta
 * - portata_max: litri al secondo massimi trasportabili
 * - materiale: tipologia di tubo (es. PVC, Polietilene)
 */

/* Sottoclassi di condotta */
prop(condotta_principale, subClassOf, condotta).
prop(condotta_secondaria, subClassOf, condotta).

/* Classe nodo (Base per campi e serbatoi) */
prop(nodo, id, _).
prop(nodo, latitudine, _).
prop(nodo, longitudine, _).