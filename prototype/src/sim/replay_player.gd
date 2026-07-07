class_name ReplayPlayer
extends RefCounted
## Relit un replay (seed + inputs) : reconstruit l'input exact de chaque tick.
## Le format est celui d'InputRecorder : frames = [[tick, qx, qy, flags], …],
## une frame n'existe que quand l'input CHANGE — entre deux frames, l'input
## courant persiste. Les flags encodent les impulsions comme dans main.gd :
## bit 0 = esquive, bit 1 = interaction, bits 2+ = choix de draft + 1.

var run_seed: int = 0
var tick_rate: int = SimClock.TICK_RATE
var frames: Array = []

var _cursor: int = 0
var _qx: int = 0
var _qy: int = 0
var _flags: int = 0


static func from_dict(data: Dictionary) -> ReplayPlayer:
	var player := ReplayPlayer.new()
	player.run_seed = int(data.get("seed", 0))
	player.tick_rate = int(data.get("tick_rate", SimClock.TICK_RATE))
	player.frames = data.get("frames", [])
	return player


static func load_from_file(path: String) -> ReplayPlayer:
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		return null
	var parsed: Variant = JSON.parse_string(file.get_as_text())
	file.close()
	if not (parsed is Dictionary):
		return null
	return from_dict(parsed)


func rewind() -> void:
	_cursor = 0
	_qx = 0
	_qy = 0
	_flags = 0


## Dernier tick pour lequel le replay contient une information.
func last_tick() -> int:
	if frames.is_empty():
		return 0
	return int(frames[frames.size() - 1][0])


## L'input du tick demandé, au format attendu par SimWorld.step().
## Les ticks doivent être demandés en ordre croissant (lecture séquentielle).
func input_for_tick(tick: int) -> Dictionary:
	while _cursor < frames.size() and int(frames[_cursor][0]) <= tick:
		var frame: Array = frames[_cursor]
		_qx = int(frame[1])
		_qy = int(frame[2])
		_flags = int(frame[3])
		_cursor += 1
	return {
		"move": Vector2(float(_qx) / InputRecorder.QUANT, float(_qy) / InputRecorder.QUANT),
		"dodge": (_flags & 1) != 0,
		"interact": (_flags & 2) != 0,
		"draft_pick": (_flags >> 2) - 1,
	}
