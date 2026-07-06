class_name SimFigure
extends RefCounted
## Une figure du cortège, côté simulation pure. Aucune dépendance à la scène.
## Stats T1 issues de data/figures.json (annexe équilibrage §4) ; la fusion
## applique les multiplicateurs de l'annexe §2 (PV/dégâts ×3, rayons ×1,25).

const FUSION_PV_DEGATS: float = 3.0
const FUSION_RAYONS: float = 1.25

static var _next_uid: int = 0

var uid: int = 0
var id: String = ""
var display_name: String = ""
var role: String = ""
var tier: int = 1
var pv: float = 0.0
var pv_max: float = 0.0
var dps: float = 0.0
var range_m: float = 1.5
var vit: float = 100.0
var kit: String = ""
var pos: Vector2 = Vector2.ZERO
var prev_pos: Vector2 = Vector2.ZERO


static func from_data(data: Dictionary, at_pos: Vector2) -> SimFigure:
	var figure := SimFigure.new()
	_next_uid += 1
	figure.uid = _next_uid
	figure.id = data.get("id", "")
	figure.display_name = data.get("nom", "?")
	figure.role = data.get("role", "?")
	figure.tier = 1
	figure.pv_max = float(data.get("pv", 100))
	figure.pv = figure.pv_max
	figure.dps = float(data.get("dps", 10))
	figure.range_m = float(data.get("portee_m", 1.5))
	figure.vit = float(data.get("vit", 100))
	figure.kit = data.get("kit", "")
	figure.pos = at_pos
	figure.prev_pos = at_pos
	return figure


## Fusion : trois récits de la même figure convergent (bible §3).
## Conservation stricte : le T2 vaut 3 T1-eq, le T3 en vaut 9.
static func fuse(base: SimFigure) -> SimFigure:
	var fused := SimFigure.new()
	_next_uid += 1
	fused.uid = _next_uid
	fused.id = base.id
	fused.display_name = base.display_name
	fused.role = base.role
	fused.tier = base.tier + 1
	fused.pv_max = base.pv_max * FUSION_PV_DEGATS
	fused.pv = fused.pv_max
	fused.dps = base.dps * FUSION_PV_DEGATS
	fused.range_m = base.range_m * FUSION_RAYONS
	fused.vit = base.vit
	fused.kit = base.kit
	fused.pos = base.pos
	fused.prev_pos = base.pos
	return fused


func t1_equivalents() -> int:
	return int(pow(3.0, float(tier - 1)))


## Multiplicateur des rayons d'effet selon le tier (×1,25 par fusion, annexe §2).
func radius_scale() -> float:
	return pow(FUSION_RAYONS, float(tier - 1))


func is_alive() -> bool:
	return pv > 0.0
