class_name FigureView
extends Node2D
## Silhouette d'une figure du cortège. Une forme par rôle, testable en aplat
## (GDD §10) ; le tier se lit par la taille et l'auréole, jamais par un chiffre.
## Cette vue LIT la simulation via main.gd ; elle n'écrit jamais dedans.

const ROLE_COLORS: Dictionary = {
	"Cogneur": Color(0.83, 0.31, 0.18),
	"Tireur": Color(0.91, 0.64, 0.24),
	"Soutien": Color(0.95, 0.82, 0.42),
	"Récolteur": Color(0.85, 0.56, 0.13),
	"Filou": Color(0.79, 0.37, 0.54),
	"Bâtisseur": Color(0.62, 0.44, 0.26),
}
const TIER_SCALES: Array[float] = [1.0, 1.4, 1.9]
const BASE_RADIUS: float = 12.0
const HALO_COLOR: Color = Color(0.98, 0.9, 0.55)

var role: String = ""
var tier: int = 1
var pv_ratio: float = 1.0


func setup(p_role: String, p_tier: int) -> void:
	role = p_role
	tier = p_tier
	queue_redraw()


func update_state(p_pv_ratio: float, p_tier: int) -> void:
	if not is_equal_approx(pv_ratio, p_pv_ratio) or tier != p_tier:
		pv_ratio = p_pv_ratio
		tier = p_tier
		queue_redraw()


func _draw() -> void:
	var radius := BASE_RADIUS * TIER_SCALES[clampi(tier, 1, 3) - 1]
	var color: Color = ROLE_COLORS.get(role, Color.WHITE)
	match role:
		"Cogneur":
			var half := radius
			draw_rect(Rect2(-half, -half, half * 2.0, half * 2.0), color)
		"Tireur":
			draw_colored_polygon(_triangle(radius, 1.0), color)
		"Soutien":
			draw_circle(Vector2.ZERO, radius, color)
		"Récolteur":
			draw_colored_polygon(_diamond(radius), color)
		"Filou":
			draw_colored_polygon(_triangle(radius, 0.55), color)
		"Bâtisseur":
			draw_colored_polygon(_pentagon(radius), color)
		_:
			draw_circle(Vector2.ZERO, radius, color)
	if tier >= 3:
		# La Légende porte l'auréole (GDD §10).
		draw_arc(Vector2.ZERO, radius + 6.0, 0.0, TAU, 32, HALO_COLOR, 2.5)
	# Barre de vie discrète, au-dessus de la silhouette.
	var bar_width := radius * 2.0
	var bar_y := -radius - 8.0
	draw_rect(Rect2(-bar_width / 2.0, bar_y, bar_width, 3.0), Color(0.1, 0.1, 0.12, 0.8))
	draw_rect(
		Rect2(-bar_width / 2.0, bar_y, bar_width * clampf(pv_ratio, 0.0, 1.0), 3.0),
		Color(0.55, 0.85, 0.4)
	)


func _triangle(radius: float, width_ratio: float) -> PackedVector2Array:
	return PackedVector2Array([
		Vector2(0.0, -radius),
		Vector2(radius * width_ratio, radius),
		Vector2(-radius * width_ratio, radius),
	])


func _diamond(radius: float) -> PackedVector2Array:
	return PackedVector2Array([
		Vector2(0.0, -radius),
		Vector2(radius, 0.0),
		Vector2(0.0, radius),
		Vector2(-radius, 0.0),
	])


func _pentagon(radius: float) -> PackedVector2Array:
	var points := PackedVector2Array()
	for i: int in range(5):
		var angle := -PI / 2.0 + TAU * float(i) / 5.0
		points.append(Vector2.from_angle(angle) * radius)
	return points
