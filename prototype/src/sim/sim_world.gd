class_name SimWorld
extends RefCounted
## Le cœur de simulation, pur et déterministe : pas fixe, aucun accès à la scène,
## à l'horloge murale ni au RNG global. La présentation (src/view, src/ui) LIT cet
## état et l'interpole ; elle n'écrit jamais dedans (roadmap technique §2).
## NOTE : ce squelette calcule en flottants — suffisant sur une machine unique.
## La bascule en virgule fixe 32.32 est la première tâche du Jalon 0 (roadmap §1.3).

# --- Unités et étalons -------------------------------------------------------
const M: float = 32.0                      # pixels par mètre (portées de l'annexe §4)
const SPEED_SCALE: float = 1.6             # px/s par point de VIT (VIT 100 → 160 px/s)
const ARENA: Rect2 = Rect2(-1200, -700, 2400, 1400)

# --- Le Conteur (GDD §4.3 : trois entrées, pas une de plus) ------------------
const CONTEUR_VIT: float = 100.0
const DODGE_TICKS: int = 6                 # 0,2 s d'élan
const DODGE_SPEED_MULT: float = 3.0
const DODGE_COOLDOWN_TICKS: int = 60       # 2 s

# --- Le cortège --------------------------------------------------------------
const FIGURE_CAP: int = 24                 # plafond dur (annexe systèmes §2.2)
const OVERFLOW_FERVEUR: int = 30           # tout récit excédentaire se convertit
const FOLLOW_DISTANCE: float = 34.0
const SEPARATION_RADIUS: float = 26.0
const SEPARATION_PUSH: float = 70.0        # px/s
const CATCH_UP_MULT: float = 1.25

# --- Économie in-run (annexe équilibrage §6) ---------------------------------
const CHEST_BASE_COST: int = 60
const CHEST_COST_STEP: int = 20            # +20 par Volume déjà ouvert dans la manche
const CHEST_INTERACT_RADIUS: float = 56.0
const PICKUP_RADIUS: float = 40.0
const GISEMENT_AMOUNT: int = 10
const START_FERVEUR: int = 30

# --- La courbe adverse (annexe équilibrage §5.1, en Silences-équivalents) ----
const WAVE_INTERVAL_TICKS: int = 600       # une « manche » du jouet : 20 s
const WAVE_BUDGET_BASE: int = 8
const WAVE_BUDGET_STEP: int = 5
const WAVE_BUDGET_CAP: int = 60
const SPAWN_EVERY_TICKS: int = 6
const SPAWN_RING_MIN: float = 640.0
const SPAWN_RING_MAX: float = 840.0

# --- Kits implémentés (le reste des 16 kits : voir README, prochaines étapes) -
const TAUNT_RADIUS_M: float = 4.0          # Héraclès : provocation passive r 4 m
const JEANNE_AURA_M: float = 5.0           # Jeanne : régén. 1,5 % PV max/s r 5 m
const JEANNE_HEAL_RATE: float = 0.015

var tick: int = 0
var game_over: bool = false
var ferveur: int = START_FERVEUR
var conteur_pos: Vector2 = Vector2.ZERO
var conteur_prev_pos: Vector2 = Vector2.ZERO
var dodge_ticks_left: int = 0
var dodge_cooldown: int = 0
var figures: Array[SimFigure] = []
var enemies: Array[SimEnemy] = []
var gisements: Array[Dictionary] = []      # {uid, pos, amount}
var chests: Array[Dictionary] = []         # {uid, pos}
var wave_index: int = 0
var wave_timer: int = 0
var spawn_queue: int = 0
var chests_opened_this_wave: int = 0
var pending_offer: Array[String] = []      # draft en attente (vide = aucun)
var events: Array[Dictionary] = []         # consommés par la présentation à chaque tick

var _data_by_id: Dictionary = {}
var _draft: SimDraft
var _rng_draft: RandomNumberGenerator
var _rng_spawns: RandomNumberGenerator
var _rng_degats: RandomNumberGenerator     # réservé (critiques, variance) — encore inutilisé
var _next_pickup_uid: int = 0


func _init(
	figures_data: Array,
	roster_ids: Array,
	start_ids: Array,
	rng_draft: RandomNumberGenerator,
	rng_spawns: RandomNumberGenerator,
	rng_degats: RandomNumberGenerator
) -> void:
	for entry: Variant in figures_data:
		var data: Dictionary = entry
		_data_by_id[data["id"]] = data
	_draft = SimDraft.new(roster_ids)
	_rng_draft = rng_draft
	_rng_spawns = rng_spawns
	_rng_degats = rng_degats
	var offset := 0
	for figure_id: Variant in start_ids:
		var figure := SimFigure.from_data(_data_by_id[figure_id], Vector2(-40.0 - 30.0 * offset, 0.0))
		figures.append(figure)
		offset += 1


## Avance la simulation d'un tick. `frame` vient de main.gd, déjà quantifié et journalisé :
## {"move": Vector2, "dodge": bool, "interact": bool, "draft_pick": int (-1 = aucun)}
func step(frame: Dictionary) -> void:
	events.clear()
	if game_over:
		return
	tick += 1
	_snapshot_prev()
	if not pending_offer.is_empty():
		# Le temps s'arrête pendant le draft — choix assumé du jouet, à requestionner
		# dès la première itération jouable (roadmap : risque du sprint 3).
		var pick := int(frame.get("draft_pick", -1))
		if pick >= 0 and pick < pending_offer.size():
			_resolve_draft(pick)
		return
	_step_conteur(frame)
	_step_cortege()
	_step_waves()
	_step_enemies()
	_step_figures_combat()
	_step_pickups()
	if bool(frame.get("interact", false)):
		_try_open_chest()
	_check_game_over()


func t1_eq_total() -> int:
	var total := 0
	for figure: SimFigure in figures:
		total += figure.t1_equivalents()
	return total


func owned_count(figure_id: String, tier: int) -> int:
	var count := 0
	for figure: SimFigure in figures:
		if figure.id == figure_id and figure.tier == tier:
			count += 1
	return count


func figure_data(figure_id: String) -> Dictionary:
	return _data_by_id.get(figure_id, {})


func current_chest_cost() -> int:
	return CHEST_BASE_COST + CHEST_COST_STEP * chests_opened_this_wave


func nearest_chest_distance() -> float:
	var best := INF
	for chest: Dictionary in chests:
		best = minf(best, conteur_pos.distance_to(chest["pos"]))
	return best


# --- Systèmes internes -------------------------------------------------------

func _snapshot_prev() -> void:
	conteur_prev_pos = conteur_pos
	for figure: SimFigure in figures:
		figure.prev_pos = figure.pos
	for enemy: SimEnemy in enemies:
		enemy.prev_pos = enemy.pos


func _step_conteur(frame: Dictionary) -> void:
	if dodge_cooldown > 0:
		dodge_cooldown -= 1
	if dodge_ticks_left > 0:
		dodge_ticks_left -= 1
	if bool(frame.get("dodge", false)) and dodge_cooldown == 0:
		dodge_ticks_left = DODGE_TICKS
		dodge_cooldown = DODGE_COOLDOWN_TICKS
		events.append({"type": "dodge", "pos": conteur_pos})
	var move: Vector2 = frame.get("move", Vector2.ZERO)
	var speed := CONTEUR_VIT * SPEED_SCALE
	if dodge_ticks_left > 0:
		speed *= DODGE_SPEED_MULT
	conteur_pos += move * speed * SimClock.TICK_DT
	conteur_pos = conteur_pos.clamp(ARENA.position, ARENA.end)


func _step_cortege() -> void:
	# Suivi en chaîne : la figure 0 suit le Conteur, chaque figure suit la précédente.
	# Une figure au contact d'un ennemi tient sa position : le déplacement du cortège
	# EST le verbe de combat (annexe systèmes §1.1).
	var leader := conteur_pos
	for figure: SimFigure in figures:
		var engaged := _nearest_enemy_in_range(figure) != null
		if not engaged:
			var to_leader := leader - figure.pos
			if to_leader.length() > FOLLOW_DISTANCE:
				var speed := figure.vit * SPEED_SCALE * CATCH_UP_MULT
				figure.pos += to_leader.normalized() * speed * SimClock.TICK_DT
		leader = figure.pos
	# Séparation : le cortège est un banc de poissons, pas une file indienne.
	for i: int in range(figures.size()):
		for j: int in range(i + 1, figures.size()):
			var between := figures[j].pos - figures[i].pos
			var dist := between.length()
			if dist < SEPARATION_RADIUS and dist > 0.001:
				var push := between.normalized() * SEPARATION_PUSH * SimClock.TICK_DT
				figures[i].pos -= push
				figures[j].pos += push
	for figure: SimFigure in figures:
		figure.pos = figure.pos.clamp(ARENA.position, ARENA.end)


func _step_waves() -> void:
	wave_timer -= 1
	if wave_timer <= 0:
		wave_index += 1
		wave_timer = WAVE_INTERVAL_TICKS
		spawn_queue = mini(WAVE_BUDGET_BASE + WAVE_BUDGET_STEP * (wave_index - 1), WAVE_BUDGET_CAP)
		chests_opened_this_wave = 0
		var gisement_count := _rng_spawns.randi_range(4, 6)
		for i: int in range(gisement_count):
			_spawn_pickup(_random_arena_point(), GISEMENT_AMOUNT)
		for i: int in range(2):
			_next_pickup_uid += 1
			chests.append({"uid": _next_pickup_uid, "pos": _random_arena_point()})
		events.append({"type": "wave_started", "wave": wave_index, "budget": spawn_queue})
	if spawn_queue > 0 and tick % SPAWN_EVERY_TICKS == 0:
		spawn_queue -= 1
		var angle := _rng_spawns.randf_range(0.0, TAU)
		var radius := _rng_spawns.randf_range(SPAWN_RING_MIN, SPAWN_RING_MAX)
		var at := (conteur_pos + Vector2.from_angle(angle) * radius).clamp(ARENA.position, ARENA.end)
		enemies.append(SimEnemy.spawn_at(at))


func _step_enemies() -> void:
	var contact_sq := 1.5 * M * 1.5 * M
	for enemy: SimEnemy in enemies:
		var target := _pick_enemy_target(enemy)
		if target == null:
			continue
		var to_target := target.pos - enemy.pos
		if to_target.length_squared() > contact_sq:
			enemy.pos += to_target.normalized() * enemy.vit * SPEED_SCALE * SimClock.TICK_DT
			enemy.pos = enemy.pos.clamp(ARENA.position, ARENA.end)
		else:
			target.pv -= enemy.dps * SimClock.TICK_DT


## Provocation (Héraclès, annexe §4.1) : un Cogneur provocateur à portée capte
## l'attention ; sinon, l'Oubli vise la figure la plus proche.
## Boucle chaude (ennemis × figures) : distances au carré, jamais de racine.
func _pick_enemy_target(enemy: SimEnemy) -> SimFigure:
	var taunt_range := TAUNT_RADIUS_M * M
	var best_taunt: SimFigure = null
	var best_taunt_dist_sq := INF
	var best_any: SimFigure = null
	var best_any_dist_sq := INF
	for figure: SimFigure in figures:
		var dist_sq := enemy.pos.distance_squared_to(figure.pos)
		if figure.id == "heracles" and dist_sq < best_taunt_dist_sq:
			var reach := taunt_range * figure.radius_scale()
			if dist_sq < reach * reach:
				best_taunt = figure
				best_taunt_dist_sq = dist_sq
		if dist_sq < best_any_dist_sq:
			best_any = figure
			best_any_dist_sq = dist_sq
	if best_taunt != null:
		return best_taunt
	return best_any


func _step_figures_combat() -> void:
	for figure: SimFigure in figures:
		var enemy := _nearest_enemy_in_range(figure)
		if enemy != null:
			enemy.pv -= figure.dps * SimClock.TICK_DT
	# Aura de Jeanne : chaque alliée dans le rayon régénère 1,5 % de SES PV max/s.
	for healer: SimFigure in figures:
		if healer.id != "jeanne_darc":
			continue
		var aura := JEANNE_AURA_M * M * healer.radius_scale()
		for ally: SimFigure in figures:
			if ally.pos.distance_to(healer.pos) <= aura:
				ally.pv = minf(ally.pv_max, ally.pv + ally.pv_max * JEANNE_HEAL_RATE * SimClock.TICK_DT)
	# Récolte des morts — les Oublis rendent un peu de Ferveur en gisement.
	var survivors: Array[SimEnemy] = []
	for enemy: SimEnemy in enemies:
		if enemy.is_alive():
			survivors.append(enemy)
		else:
			events.append({"type": "enemy_died", "pos": enemy.pos})
			_spawn_pickup(enemy.pos, SimEnemy.FERVEUR_DROP)
	enemies = survivors
	var alive: Array[SimFigure] = []
	for figure: SimFigure in figures:
		if figure.is_alive():
			alive.append(figure)
		else:
			events.append({"type": "figure_died", "name": figure.display_name, "pos": figure.pos})
	figures = alive


## Boucle chaude (figures × ennemis) : distances au carré, jamais de racine.
func _nearest_enemy_in_range(figure: SimFigure) -> SimEnemy:
	var reach := figure.range_m * M
	var reach_sq := reach * reach
	var best: SimEnemy = null
	var best_dist_sq := INF
	for enemy: SimEnemy in enemies:
		var dist_sq := figure.pos.distance_squared_to(enemy.pos)
		if dist_sq <= reach_sq and dist_sq < best_dist_sq:
			best = enemy
			best_dist_sq = dist_sq
	return best


func _step_pickups() -> void:
	var remaining: Array[Dictionary] = []
	for gisement: Dictionary in gisements:
		var collected := conteur_pos.distance_to(gisement["pos"]) <= PICKUP_RADIUS
		if not collected:
			for figure: SimFigure in figures:
				if figure.pos.distance_to(gisement["pos"]) <= PICKUP_RADIUS:
					collected = true
					break
		if collected:
			ferveur += int(gisement["amount"])
			events.append({"type": "pickup", "amount": gisement["amount"], "pos": gisement["pos"]})
		else:
			remaining.append(gisement)
	gisements = remaining


func _try_open_chest() -> void:
	var best_index := -1
	var best_dist := CHEST_INTERACT_RADIUS
	for i: int in range(chests.size()):
		var dist: float = conteur_pos.distance_to(chests[i]["pos"])
		if dist <= best_dist:
			best_index = i
			best_dist = dist
	if best_index < 0:
		return
	var cost := current_chest_cost()
	if ferveur < cost:
		events.append({"type": "chest_refused", "cost": cost, "pos": chests[best_index]["pos"]})
		return
	ferveur -= cost
	chests_opened_this_wave += 1
	var at: Vector2 = chests[best_index]["pos"]
	chests.remove_at(best_index)
	pending_offer = _draft.draw_three(_rng_draft)
	events.append({"type": "draft_offered", "pos": at})


func _resolve_draft(pick: int) -> void:
	var chosen_id := pending_offer[pick]
	pending_offer = []
	if figures.size() >= FIGURE_CAP:
		# Plafond du chaos lisible : tout récit excédentaire devient de la Ferveur.
		ferveur += OVERFLOW_FERVEUR
		events.append({"type": "overflow", "amount": OVERFLOW_FERVEUR, "pos": conteur_pos})
		return
	var figure := SimFigure.from_data(_data_by_id[chosen_id], conteur_pos + Vector2(0.0, 40.0))
	figures.append(figure)
	events.append({"type": "figure_added", "name": figure.display_name, "pos": figure.pos})
	_check_fusions(chosen_id)


## Trois récits identiques convergent : le mythe grandit (bible §3). En cascade :
## trois T1 → un T2, et si trois T2 existent, un T3 naît dans la foulée.
func _check_fusions(figure_id: String) -> void:
	var fused_something := true
	while fused_something:
		fused_something = false
		for tier: int in [1, 2]:
			var indices: Array[int] = []
			for i: int in range(figures.size()):
				if figures[i].id == figure_id and figures[i].tier == tier:
					indices.append(i)
			if indices.size() >= 3:
				var base := figures[indices[0]]
				var fused := SimFigure.fuse(base)
				for k: int in range(2, -1, -1):
					figures.remove_at(indices[k])
				figures.append(fused)
				events.append({
					"type": "fusion",
					"name": fused.display_name,
					"tier": fused.tier,
					"pos": fused.pos,
				})
				fused_something = true
				break


func _spawn_pickup(at: Vector2, amount: int) -> void:
	_next_pickup_uid += 1
	gisements.append({"uid": _next_pickup_uid, "pos": at, "amount": amount})


## Harnais de mesure UNIQUEMENT (RunHarness.bench) : complète la sim jusqu'à la
## charge demandée, en réutilisant le flux « spawns ». Jamais appelé en jeu.
func debug_populate(target_figures: int, target_enemies: int) -> void:
	var ids: Array = _data_by_id.keys()
	ids.sort()
	var i := figures.size()
	while figures.size() < mini(target_figures, FIGURE_CAP):
		var data: Dictionary = _data_by_id[ids[i % ids.size()]]
		var at := conteur_pos + Vector2.from_angle(TAU * float(i) / float(FIGURE_CAP)) * 120.0
		figures.append(SimFigure.from_data(data, at.clamp(ARENA.position, ARENA.end)))
		i += 1
	while enemies.size() < target_enemies:
		var angle := _rng_spawns.randf_range(0.0, TAU)
		var radius := _rng_spawns.randf_range(SPAWN_RING_MIN, SPAWN_RING_MAX)
		var at := (conteur_pos + Vector2.from_angle(angle) * radius).clamp(ARENA.position, ARENA.end)
		enemies.append(SimEnemy.spawn_at(at))


func _random_arena_point() -> Vector2:
	var margin := 80.0
	return Vector2(
		_rng_spawns.randf_range(ARENA.position.x + margin, ARENA.end.x - margin),
		_rng_spawns.randf_range(ARENA.position.y + margin, ARENA.end.y - margin)
	)


func _check_game_over() -> void:
	if figures.is_empty() and tick > SimClock.TICK_RATE:
		game_over = true
		events.append({"type": "game_over", "tick": tick})
