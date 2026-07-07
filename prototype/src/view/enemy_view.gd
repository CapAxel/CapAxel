class_name EnemyView
extends Node2D
## Un Silence : désaturé et froid, à l'opposé de la palette chaude du cortège
## (GDD §10). La brume se lit dans la transparence.

const BODY_COLOR: Color = Color(0.36, 0.42, 0.47, 0.9)
const RADIUS: float = 9.0

var pv_ratio: float = 1.0


func update_state(p_ratio: float) -> void:
	if not is_equal_approx(pv_ratio, p_ratio):
		pv_ratio = p_ratio
		queue_redraw()


func _draw() -> void:
	draw_circle(Vector2.ZERO, RADIUS, BODY_COLOR)
	if pv_ratio < 1.0:
		draw_arc(Vector2.ZERO, RADIUS + 3.0, -PI / 2.0, -PI / 2.0 + TAU * clampf(pv_ratio, 0.0, 1.0), 16, Color(0.7, 0.75, 0.8, 0.7), 1.5)
