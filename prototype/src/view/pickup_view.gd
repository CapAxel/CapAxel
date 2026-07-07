class_name PickupView
extends Node2D
## Un gisement de Ferveur — la teinte dorée est RÉSERVÉE à la ressource (GDD §10).

const FERVEUR_COLOR: Color = Color(0.95, 0.78, 0.3)
const RADIUS: float = 6.0


func _draw() -> void:
	draw_circle(Vector2.ZERO, RADIUS, FERVEUR_COLOR)
	draw_arc(Vector2.ZERO, RADIUS + 2.0, 0.0, TAU, 16, Color(0.95, 0.78, 0.3, 0.35), 1.5)
