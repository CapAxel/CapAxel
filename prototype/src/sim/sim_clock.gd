extends Node
## SimClock — autoload. Constantes de temps de la simulation et tick courant.
## La simulation avance à pas fixe (30 Hz) ; la présentation interpole entre deux ticks.
## Personne d'autre que main.gd n'écrit current_tick.

const TICK_RATE: int = 30
const TICK_DT: float = 1.0 / float(TICK_RATE)

var current_tick: int = 0


static func seconds_to_ticks(seconds: float) -> int:
	return int(round(seconds * float(TICK_RATE)))


static func ticks_to_seconds(ticks: int) -> float:
	return float(ticks) * TICK_DT
