class_name RunHarness
extends RefCounted
## Harnais headless : construit des runs hors présentation et exécute les
## vérifications de la roadmap technique (§2, §3 — jalon 0) :
##   --selftest  le test de déterminisme : une run pilotée est journalisée,
##               puis REJOUÉE depuis seed + inputs ; les empreintes d'état
##               doivent coïncider tick à tick. C'est le test « qui casse »
##               destiné à la CI (annexe systèmes §3.6).
##   --replay    relit un fichier replay et imprime l'empreinte finale.
##   --bench     mesure le coût du tick à charge nominale (budget 4 ms).
## Le pilote synthétique est une fonction PURE du tick et de l'état lu : aucune
## source de hasard hors des flux seedés — c'est ce qui rend le test rejouable.

const HASH_SAMPLE_EVERY: int = 100
const BENCH_WARMUP_TICKS: int = 30
const BENCH_MEASURE_TICKS: int = 600
const BENCH_FIGURES: int = 24
const BENCH_ENEMIES: int = 300
const BENCH_BUDGET_MS: float = 4.0


## Construit une sim prête à jouer pour une seed donnée. Réinitialise les flux
## RNG et les compteurs d'UID : même seed = même monde, à chaque fois.
static func build_sim(figures_data: Array, roster_ids: Array, start_ids: Array, p_seed: int) -> SimWorld:
	RngService.init_run(p_seed)
	SimFigure.reset_uids()
	SimEnemy.reset_uids()
	return SimWorld.new(
		figures_data,
		roster_ids,
		start_ids,
		RngService.stream("draft"),
		RngService.stream("spawns"),
		RngService.stream("degats")
	)


## Passe 1 : le pilote joue et tout est journalisé. Passe 2 : la relecture
## reconstruit la run entière depuis seed + inputs. Retourne true si chaque
## empreinte échantillonnée ET l'empreinte finale coïncident.
static func selftest(figures_data: Array, roster_ids: Array, start_ids: Array, p_seed: int, total_ticks: int) -> bool:
	var recorder := InputRecorder.new()
	recorder.start_run(p_seed)
	var sim_a := build_sim(figures_data, roster_ids, start_ids, p_seed)
	var hashes_a: Array[int] = []
	var drafts := 0
	var fusions := 0
	for t: int in range(total_ticks):
		var frame := _bot_frame(sim_a, t)
		recorder.record(sim_a.tick + 1, frame["move"], _frame_flags(frame))
		sim_a.step(frame)
		for event: Dictionary in sim_a.events:
			match event["type"]:
				"draft_offered":
					drafts += 1
				"fusion":
					fusions += 1
		if sim_a.tick % HASH_SAMPLE_EVERY == 0:
			hashes_a.append(StateHash.of_world(sim_a))
	var final_a := StateHash.of_world(sim_a)

	var player := ReplayPlayer.from_dict(recorder.to_dict())
	var sim_b := build_sim(figures_data, roster_ids, start_ids, player.run_seed)
	var hashes_b: Array[int] = []
	for t: int in range(total_ticks):
		sim_b.step(player.input_for_tick(sim_b.tick + 1))
		if sim_b.tick % HASH_SAMPLE_EVERY == 0:
			hashes_b.append(StateHash.of_world(sim_b))
	var final_b := StateHash.of_world(sim_b)

	print("[selftest] seed=%d ticks=%d (%.1f s de sim)" % [p_seed, total_ticks, SimClock.ticks_to_seconds(total_ticks)])
	print("[selftest] couverture : %d manches, %d drafts, %d fusions, game_over=%s" % [sim_a.wave_index, drafts, fusions, str(sim_a.game_over)])
	print("[selftest] run A : tick final=%d, %d figures, %d ennemis, empreinte=%d" % [sim_a.tick, sim_a.figures.size(), sim_a.enemies.size(), final_a])
	print("[selftest] run B : tick final=%d, %d figures, %d ennemis, empreinte=%d" % [sim_b.tick, sim_b.figures.size(), sim_b.enemies.size(), final_b])
	if hashes_a != hashes_b:
		for i: int in range(mini(hashes_a.size(), hashes_b.size())):
			if hashes_a[i] != hashes_b[i]:
				printerr("[selftest] ÉCHEC : divergence au plus tard au tick %d (%d ≠ %d)" % [(i + 1) * HASH_SAMPLE_EVERY, hashes_a[i], hashes_b[i]])
				return false
		printerr("[selftest] ÉCHEC : nombres d'échantillons différents (%d ≠ %d)" % [hashes_a.size(), hashes_b.size()])
		return false
	if final_a != final_b:
		printerr("[selftest] ÉCHEC : empreintes finales différentes (%d ≠ %d)" % [final_a, final_b])
		return false
	print("[selftest] OK : la relecture reproduit la run à l'identique (%d empreintes comparées)" % (hashes_a.size() + 1))
	return true


## Relit un fichier replay (format InputRecorder) et imprime l'empreinte finale —
## la brique des « golden replays » de la CI et de la re-simulation serveur.
static func replay_file(figures_data: Array, roster_ids: Array, start_ids: Array, path: String) -> bool:
	var player := ReplayPlayer.load_from_file(path)
	if player == null:
		printerr("[replay] fichier illisible : " + path)
		return false
	var sim := build_sim(figures_data, roster_ids, start_ids, player.run_seed)
	var total_ticks := player.last_tick()
	for t: int in range(total_ticks):
		sim.step(player.input_for_tick(sim.tick + 1))
	print("[replay] %s : seed=%d, %d ticks rejoués, empreinte finale=%d" % [path, player.run_seed, sim.tick, StateHash.of_world(sim)])
	return true


## Charge nominale de la roadmap (§1.4) : 24 figures + 300 Oublis, budget 4 ms.
## (60 projectiles : sans objet, la sim n'a pas encore de projectiles.)
static func bench(figures_data: Array, roster_ids: Array, start_ids: Array, p_seed: int) -> void:
	var sim := build_sim(figures_data, roster_ids, start_ids, p_seed)
	for t: int in range(BENCH_WARMUP_TICKS):
		sim.debug_populate(BENCH_FIGURES, BENCH_ENEMIES)
		sim.step(_bot_frame(sim, t))
	var samples_usec: Array[int] = []
	for t: int in range(BENCH_MEASURE_TICKS):
		sim.debug_populate(BENCH_FIGURES, BENCH_ENEMIES)
		var frame := _bot_frame(sim, BENCH_WARMUP_TICKS + t)
		var before := Time.get_ticks_usec()
		sim.step(frame)
		samples_usec.append(Time.get_ticks_usec() - before)
	samples_usec.sort()
	var total := 0
	for sample: int in samples_usec:
		total += sample
	var avg_ms := float(total) / float(samples_usec.size()) / 1000.0
	var p95_ms := float(samples_usec[int(samples_usec.size() * 0.95)]) / 1000.0
	var max_ms := float(samples_usec[samples_usec.size() - 1]) / 1000.0
	print("[bench] charge : %d figures + %d Oublis (projectiles : N/A), %d ticks mesurés" % [sim.figures.size(), sim.enemies.size(), BENCH_MEASURE_TICKS])
	print("[bench] tick : moyenne %.3f ms · p95 %.3f ms · max %.3f ms — budget %.1f ms" % [avg_ms, p95_ms, max_ms, BENCH_BUDGET_MS])
	if p95_ms > BENCH_BUDGET_MS:
		print("[bench] AU-DESSUS du budget : instruire la bascule GDExtension (roadmap §1.4)")
	elif p95_ms > BENCH_BUDGET_MS * 0.5:
		print("[bench] dans le budget, marge < ×2 : à surveiller à chaque ajout de système")
	else:
		print("[bench] confortablement dans le budget")


# --- Le pilote synthétique ----------------------------------------------------

## L'input d'un tick, calculé depuis le tick et l'état LU de la sim (jamais
## modifié). Stratégie : drafter au plus près de la fusion ; cap sur le Volume
## le plus proche si la Ferveur suffit, sinon le gisement le plus proche (les
## ennemis vaincus en déposent : suivre l'argent, c'est suivre le combat) ;
## fuite tangentielle en dernier recours seulement — les figures engagées
## tiennent leur ligne, le cortège ne survit qu'en nourrissant le draft.
## Esquive et interaction en impulsions d'un tick, comme main.gd.
const BOT_FLEE_RADIUS: float = 90.0

static func _bot_frame(sim: SimWorld, t: int) -> Dictionary:
	if not sim.pending_offer.is_empty():
		return {"move": Vector2.ZERO, "dodge": false, "interact": false, "draft_pick": _greedy_pick(sim)}
	var pos := sim.conteur_pos
	var direction := Vector2.from_angle(float(t) * 0.02)
	var threat := _nearest_enemy(sim)
	if threat != Vector2.INF and pos.distance_to(threat) < BOT_FLEE_RADIUS:
		var away := (pos - threat).normalized()
		direction = (away + away.orthogonal()).normalized()
	else:
		var target := _nearest(pos, sim.chests) if sim.ferveur >= sim.current_chest_cost() else Vector2.INF
		if target == Vector2.INF:
			target = _nearest(pos, sim.gisements)
		if target != Vector2.INF and pos.distance_to(target) > 8.0:
			direction = (target - pos).normalized()
	return {
		"move": InputRecorder.quantize_move(direction),
		"dodge": t % 173 == 0 and t > 0,
		"interact": t % 7 == 0 and sim.nearest_chest_distance() <= SimWorld.CHEST_INTERACT_RADIUS,
		"draft_pick": -1,
	}


## Le choix qui rapproche le plus d'une fusion : la carte dont on possède déjà
## le plus d'exemplaires T1.
static func _greedy_pick(sim: SimWorld) -> int:
	var best_pick := 0
	var best_owned := -1
	for i: int in range(sim.pending_offer.size()):
		var owned := sim.owned_count(sim.pending_offer[i], 1)
		if owned > best_owned:
			best_owned = owned
			best_pick = i
	return best_pick


static func _nearest_enemy(sim: SimWorld) -> Vector2:
	var best := Vector2.INF
	var best_dist_sq := INF
	for enemy: SimEnemy in sim.enemies:
		var dist_sq := sim.conteur_pos.distance_squared_to(enemy.pos)
		if dist_sq < best_dist_sq:
			best = enemy.pos
			best_dist_sq = dist_sq
	return best


static func _nearest(from: Vector2, entries: Array[Dictionary]) -> Vector2:
	var best := Vector2.INF
	var best_dist := INF
	for entry: Dictionary in entries:
		var dist: float = from.distance_to(entry["pos"])
		if dist < best_dist:
			best = entry["pos"]
			best_dist = dist
	return best


## Encode un frame d'input dans les flags du journal — le miroir exact de main.gd.
static func _frame_flags(frame: Dictionary) -> int:
	var flags := 0
	if bool(frame.get("dodge", false)):
		flags |= 1
	if bool(frame.get("interact", false)):
		flags |= 2
	var pick := int(frame.get("draft_pick", -1))
	if pick >= 0:
		flags |= (pick + 1) << 2
	return flags
