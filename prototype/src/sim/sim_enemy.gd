class_name SimEnemy
extends RefCounted
## Un Oubli, côté simulation. Le prototype ne connaît que l'ennemi-étalon :
## le Silence — 30 PV, 4 DPS, VIT 85 (annexe équilibrage §1).

const SILENCE_PV: float = 30.0
const SILENCE_DPS: float = 4.0
const SILENCE_VIT: float = 85.0
const FERVEUR_DROP: int = 3

static var _next_uid: int = 0

var uid: int = 0
var pv: float = SILENCE_PV
var dps: float = SILENCE_DPS
var vit: float = SILENCE_VIT
var pos: Vector2 = Vector2.ZERO
var prev_pos: Vector2 = Vector2.ZERO


static func spawn_at(at_pos: Vector2) -> SimEnemy:
	var enemy := SimEnemy.new()
	_next_uid += 1
	enemy.uid = _next_uid
	enemy.pos = at_pos
	enemy.prev_pos = at_pos
	return enemy


func is_alive() -> bool:
	return pv > 0.0
