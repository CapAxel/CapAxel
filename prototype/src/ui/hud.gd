class_name HudLayer
extends CanvasLayer
## HUD de debug du jouet : seed, tick, taille du cortège en T1-eq, Ferveur.
## Tout est construit par code — aucune scène complexe à maintenir.

var _debug_label: Label
var _ferveur_label: Label
var _hint_label: Label
var _game_over_label: Label


func _ready() -> void:
	_debug_label = _make_label(HORIZONTAL_ALIGNMENT_LEFT)
	_debug_label.position = Vector2(12.0, 8.0)
	add_child(_debug_label)

	_ferveur_label = _make_label(HORIZONTAL_ALIGNMENT_RIGHT)
	_ferveur_label.position = Vector2(1000.0, 8.0)
	_ferveur_label.size = Vector2(268.0, 30.0)
	_ferveur_label.add_theme_font_size_override("font_size", 22)
	_ferveur_label.add_theme_color_override("font_color", Color(0.95, 0.78, 0.3))
	add_child(_ferveur_label)

	_hint_label = _make_label(HORIZONTAL_ALIGNMENT_CENTER)
	_hint_label.position = Vector2(0.0, 690.0)
	_hint_label.size = Vector2(1280.0, 24.0)
	_hint_label.add_theme_color_override("font_color", Color(1.0, 1.0, 1.0, 0.65))
	add_child(_hint_label)

	_game_over_label = _make_label(HORIZONTAL_ALIGNMENT_CENTER)
	_game_over_label.position = Vector2(0.0, 300.0)
	_game_over_label.size = Vector2(1280.0, 120.0)
	_game_over_label.add_theme_font_size_override("font_size", 32)
	_game_over_label.text = "Le cortège s'est tu.\nLes Oublis reprennent la Mémoire… [R] pour raconter à nouveau."
	_game_over_label.visible = false
	add_child(_game_over_label)


func update_stats(sim: SimWorld, run_seed: int) -> void:
	_debug_label.text = "seed %d · tick %d · manche %d\ncortège %d figures (%d T1-eq) · Oublis %d" % [
		run_seed, sim.tick, sim.wave_index, sim.figures.size(), sim.t1_eq_total(), sim.enemies.size(),
	]
	_ferveur_label.text = "Ferveur : %d" % sim.ferveur
	if sim.game_over:
		_hint_label.text = ""
	elif not sim.pending_offer.is_empty():
		_hint_label.text = "Trois pages se tournent — choisissez un récit (1/2/3 ou clic)"
	elif sim.nearest_chest_distance() <= SimWorld.CHEST_INTERACT_RADIUS:
		_hint_label.text = "[E] ouvrir le Volume — coût : %d Ferveur" % sim.current_chest_cost()
	else:
		_hint_label.text = "ZQSD/WASD : déplacer · Espace : esquive · E : ouvrir un Volume · R : recommencer"


func set_game_over(is_over: bool) -> void:
	_game_over_label.visible = is_over


func _make_label(alignment: HorizontalAlignment) -> Label:
	var label := Label.new()
	label.horizontal_alignment = alignment
	label.add_theme_color_override("font_outline_color", Color(0.05, 0.05, 0.08))
	label.add_theme_constant_override("outline_size", 4)
	return label
