class_name InputRecorder
extends RefCounted
## Journal d'inputs : le format replay (seed + inputs par tick) existe dès le premier
## jour, même si la relecture n'est pas encore implémentée (roadmap technique §2).
## Le vecteur de déplacement est quantifié AVANT d'entrer dans la simulation :
## la valeur enregistrée est exactement la valeur simulée.

const FORMAT_VERSION: int = 0
const QUANT: float = 256.0

var run_seed: int = 0
var frames: Array = []
var _last_packed: Array = [0, 0, 0]


static func quantize_move(raw: Vector2) -> Vector2:
	var clamped := raw.limit_length(1.0)
	return Vector2(
		round(clamped.x * QUANT) / QUANT,
		round(clamped.y * QUANT) / QUANT
	)


func start_run(p_seed: int) -> void:
	run_seed = p_seed
	frames.clear()
	_last_packed = [0, 0, 0]


## Enregistre l'input d'un tick. N'écrit une frame que si l'input change :
## un replay d'une run de 25 min pèse quelques dizaines de Ko, pas des Mo.
func record(tick: int, move: Vector2, flags: int) -> void:
	var packed: Array = [int(move.x * QUANT), int(move.y * QUANT), flags]
	if packed == _last_packed and not frames.is_empty():
		return
	_last_packed = packed
	frames.append([tick, packed[0], packed[1], flags])


func to_dict() -> Dictionary:
	return {
		"version": FORMAT_VERSION,
		"tick_rate": SimClock.TICK_RATE,
		"seed": run_seed,
		"frames": frames,
	}


func save_to_file(path: String) -> void:
	var file := FileAccess.open(path, FileAccess.WRITE)
	if file == null:
		push_warning("InputRecorder : impossible d'écrire " + path)
		return
	file.store_string(JSON.stringify(to_dict()))
	file.close()
