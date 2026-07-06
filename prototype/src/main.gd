extends Node2D
## Orchestrateur : possède la simulation, la fait avancer à pas fixe depuis
## _physics_process (30 Hz, réglé dans project.godot), journalise chaque input,
## et synchronise la couche de présentation en interpolant entre deux ticks.
## RÈGLE : la présentation lit la sim ; elle n'écrit JAMAIS dedans.

const DEFAULT_SEED: int = 20260706
const REPLAY_PATH: String = "user://replay_last.json"
const FLOOR_COLOR: Color = Color(0.16, 0.15, 0.19)
const BORDER_COLOR: Color = Color(0.55, 0.5, 0.62, 0.6)

var sim: SimWorld
var recorder := InputRecorder.new()
var run_seed: int = DEFAULT_SEED
var replay_saved: bool = false
var pending_draft_pick: int = -1

var figures_data: Array = []
var roster_ids: Array = []
var start_ids: Array = []

var world_layer: Node2D
var camera: Camera2D
var conteur_view: ConteurView
var hud: HudLayer
var draft_ui: DraftUi
var figure_views: Dictionary = {}
var enemy_views: Dictionary = {}
var pickup_views: Dictionary = {}
var chest_views: Dictionary = {}


func _ready() -> void:
	_load_data()
	world_layer = Node2D.new()
	add_child(world_layer)
	conteur_view = ConteurView.new()
	world_layer.add_child(conteur_view)
	camera = Camera2D.new()
	add_child(camera)
	camera.make_current()
	hud = HudLayer.new()
	add_child(hud)
	draft_ui = DraftUi.new()
	draft_ui.pick_chosen.connect(_on_draft_pick)
	add_child(draft_ui)
	_start_run(DEFAULT_SEED)
	queue_redraw()


func _load_data() -> void:
	var file := FileAccess.open("res://data/figures.json", FileAccess.READ)
	assert(file != null, "data/figures.json introuvable")
	var parsed: Variant = JSON.parse_string(file.get_as_text())
	assert(parsed is Dictionary, "data/figures.json invalide")
	var data: Dictionary = parsed
	figures_data = data["figures"]
	roster_ids = data["roster_prototype"]
	start_ids = data["cortege_depart"]


func _start_run(p_seed: int) -> void:
	run_seed = p_seed
	RngService.init_run(p_seed)
	recorder.start_run(p_seed)
	replay_saved = false
	pending_draft_pick = -1
	sim = SimWorld.new(
		figures_data,
		roster_ids,
		start_ids,
		RngService.stream("draft"),
		RngService.stream("spawns"),
		RngService.stream("degats")
	)
	SimClock.current_tick = 0
	for views: Dictionary in [figure_views, enemy_views, pickup_views, chest_views]:
		for view: Node in views.values():
			view.queue_free()
		views.clear()
	draft_ui.hide_offer()
	hud.set_game_over(false)


func _physics_process(_delta: float) -> void:
	if Input.is_action_just_pressed("restart"):
		# Même seed = même monde : la reproductibilité se constate à la main.
		_start_run(run_seed)
		return
	var move := InputRecorder.quantize_move(
		Input.get_vector("move_left", "move_right", "move_up", "move_down")
	)
	var dodge := Input.is_action_just_pressed("dodge")
	var interact := Input.is_action_just_pressed("interact")
	var pick := pending_draft_pick
	pending_draft_pick = -1
	if Input.is_action_just_pressed("draft_1"):
		pick = 0
	elif Input.is_action_just_pressed("draft_2"):
		pick = 1
	elif Input.is_action_just_pressed("draft_3"):
		pick = 2
	var flags := 0
	if dodge:
		flags |= 1
	if interact:
		flags |= 2
	if pick >= 0:
		flags |= (pick + 1) << 2
	recorder.record(sim.tick + 1, move, flags)
	sim.step({"move": move, "dodge": dodge, "interact": interact, "draft_pick": pick})
	SimClock.current_tick = sim.tick
	_consume_events()
	if sim.game_over and not replay_saved:
		recorder.save_to_file(REPLAY_PATH)
		replay_saved = true
		hud.set_game_over(true)


func _process(_delta: float) -> void:
	var alpha := Engine.get_physics_interpolation_fraction()
	var conteur_render := sim.conteur_prev_pos.lerp(sim.conteur_pos, alpha)
	conteur_view.position = conteur_render
	var cooldown_ratio := 1.0
	if SimWorld.DODGE_COOLDOWN_TICKS > 0:
		cooldown_ratio = 1.0 - float(sim.dodge_cooldown) / float(SimWorld.DODGE_COOLDOWN_TICKS)
	conteur_view.update_state(cooldown_ratio)
	_sync_figures(alpha)
	_sync_enemies(alpha)
	_sync_static_views(sim.gisements, pickup_views, PickupView)
	_sync_static_views(sim.chests, chest_views, ChestView)
	camera.position = conteur_render
	var zoom_target := clampf(1.05 - 0.018 * float(sim.figures.size()), 0.7, 1.05)
	camera.zoom = camera.zoom.lerp(Vector2(zoom_target, zoom_target), 0.05)
	hud.update_stats(sim, run_seed)
	if sim.pending_offer.is_empty() and draft_ui.visible:
		draft_ui.hide_offer()


func _draw() -> void:
	draw_rect(SimWorld.ARENA, FLOOR_COLOR)
	draw_rect(SimWorld.ARENA, BORDER_COLOR, false, 4.0)


func _on_draft_pick(index: int) -> void:
	pending_draft_pick = index


func _consume_events() -> void:
	for event: Dictionary in sim.events:
		match event["type"]:
			"fusion":
				var tier_name := "Héros"
				if int(event["tier"]) >= 3:
					tier_name = "Légende"
				_float_text("%s devient %s !" % [event["name"], tier_name], event["pos"], Color(0.98, 0.9, 0.55), 20)
			"figure_added":
				_float_text("%s rejoint le cortège" % event["name"], event["pos"], Color.WHITE, 14)
			"figure_died":
				_float_text("%s s'efface…" % event["name"], event["pos"], Color(0.6, 0.65, 0.75), 14)
			"pickup":
				_float_text("+%d" % int(event["amount"]), event["pos"], Color(0.95, 0.78, 0.3), 12)
			"chest_refused":
				_float_text("Ferveur insuffisante (%d)" % int(event["cost"]), event["pos"], Color(0.9, 0.4, 0.35), 14)
			"overflow":
				_float_text("Cortège plein : +%d Ferveur" % int(event["amount"]), event["pos"], Color(0.95, 0.78, 0.3), 14)
			"draft_offered":
				draft_ui.show_offer(sim.pending_offer, sim)
			"wave_started":
				_float_text("Manche %d — les Oublis approchent" % int(event["wave"]), sim.conteur_pos + Vector2(0.0, -80.0), Color(0.7, 0.75, 0.85), 18)


func _float_text(text: String, at: Vector2, color: Color, font_size: int) -> void:
	var label := Label.new()
	label.text = text
	label.position = at + Vector2(-60.0, -30.0)
	label.add_theme_color_override("font_color", color)
	label.add_theme_font_size_override("font_size", font_size)
	label.add_theme_color_override("font_outline_color", Color(0.05, 0.05, 0.08))
	label.add_theme_constant_override("outline_size", 4)
	world_layer.add_child(label)
	var tween := create_tween()
	tween.tween_property(label, "position", label.position + Vector2(0.0, -40.0), 1.1)
	tween.parallel().tween_property(label, "modulate:a", 0.0, 1.1)
	tween.tween_callback(label.queue_free)


func _sync_figures(alpha: float) -> void:
	var seen: Dictionary = {}
	for figure: SimFigure in sim.figures:
		seen[figure.uid] = true
		var view: FigureView = figure_views.get(figure.uid)
		if view == null:
			view = FigureView.new()
			view.setup(figure.role, figure.tier)
			world_layer.add_child(view)
			figure_views[figure.uid] = view
		view.position = figure.prev_pos.lerp(figure.pos, alpha)
		view.update_state(figure.pv / figure.pv_max, figure.tier)
	_prune_views(figure_views, seen)


func _sync_enemies(alpha: float) -> void:
	var seen: Dictionary = {}
	for enemy: SimEnemy in sim.enemies:
		seen[enemy.uid] = true
		var view: EnemyView = enemy_views.get(enemy.uid)
		if view == null:
			view = EnemyView.new()
			world_layer.add_child(view)
			enemy_views[enemy.uid] = view
		view.position = enemy.prev_pos.lerp(enemy.pos, alpha)
		view.update_state(enemy.pv / SimEnemy.SILENCE_PV)
	_prune_views(enemy_views, seen)


func _sync_static_views(entries: Array[Dictionary], views: Dictionary, view_class: Variant) -> void:
	var seen: Dictionary = {}
	for entry: Dictionary in entries:
		var uid: int = entry["uid"]
		seen[uid] = true
		var view: Node2D = views.get(uid)
		if view == null:
			view = view_class.new()
			world_layer.add_child(view)
			views[uid] = view
		view.position = entry["pos"]
	_prune_views(views, seen)


func _prune_views(views: Dictionary, seen: Dictionary) -> void:
	var stale: Array = []
	for uid: Variant in views.keys():
		if not seen.has(uid):
			stale.append(uid)
	for uid: Variant in stale:
		views[uid].queue_free()
		views.erase(uid)
