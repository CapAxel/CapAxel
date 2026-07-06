class_name ConteurView
extends Node2D
## Le Conteur : volontairement humble — une lanterne-encrier, pas un guerrier
## (bible §2). L'anneau indique la recharge de l'esquive.

const BODY_COLOR: Color = Color(0.93, 0.9, 0.82)
const FLAME_COLOR: Color = Color(1.0, 0.78, 0.35)
const COOLDOWN_COLOR: Color = Color(0.93, 0.9, 0.82, 0.5)
const RADIUS: float = 10.0

var dodge_ready_ratio: float = 1.0


func update_state(p_ratio: float) -> void:
	if not is_equal_approx(dodge_ready_ratio, p_ratio):
		dodge_ready_ratio = p_ratio
		queue_redraw()


func _draw() -> void:
	draw_circle(Vector2.ZERO, RADIUS, BODY_COLOR)
	draw_colored_polygon(PackedVector2Array([
		Vector2(0.0, -RADIUS - 9.0),
		Vector2(4.0, -RADIUS - 1.0),
		Vector2(-4.0, -RADIUS - 1.0),
	]), FLAME_COLOR)
	if dodge_ready_ratio < 1.0:
		draw_arc(Vector2.ZERO, RADIUS + 5.0, -PI / 2.0, -PI / 2.0 + TAU * dodge_ready_ratio, 24, COOLDOWN_COLOR, 2.0)
