class_name StateHash
extends RefCounted
## Empreinte de l'état complet de la simulation, pour comparer deux exécutions
## (enregistrement contre relecture, deux machines, deux versions du code).
## S'appuie sur hash() de Godot : stable pour un même binaire — suffisant pour
## le test de déterminisme mono-binaire de la CI. L'empreinte multiplateforme
## sérieuse arrive avec la virgule fixe 32.32 (roadmap technique §1.3).

static func of_world(sim: SimWorld) -> int:
	var acc: Array = [
		sim.tick,
		sim.game_over,
		sim.ferveur,
		sim.conteur_pos.x, sim.conteur_pos.y,
		sim.dodge_ticks_left,
		sim.dodge_cooldown,
		sim.wave_index,
		sim.wave_timer,
		sim.spawn_queue,
		sim.chests_opened_this_wave,
		sim.pending_offer,
	]
	for figure: SimFigure in sim.figures:
		acc.append([figure.uid, figure.id, figure.tier, figure.pv, figure.pos.x, figure.pos.y])
	for enemy: SimEnemy in sim.enemies:
		acc.append([enemy.uid, enemy.pv, enemy.pos.x, enemy.pos.y])
	for gisement: Dictionary in sim.gisements:
		var g_pos: Vector2 = gisement["pos"]
		acc.append([int(gisement["uid"]), g_pos.x, g_pos.y, int(gisement["amount"])])
	for chest: Dictionary in sim.chests:
		var c_pos: Vector2 = chest["pos"]
		acc.append([int(chest["uid"]), c_pos.x, c_pos.y])
	return hash(acc)
