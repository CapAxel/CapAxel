class_name ChestView
extends Node2D
## Un Volume scellé : les coffres sont des livres (bible §2). Rectangle-couverture
## et tranche claire ; l'ouverture (le draft) est gérée par l'UI.

const COVER_COLOR: Color = Color(0.45, 0.29, 0.17)
const PAGES_COLOR: Color = Color(0.9, 0.85, 0.7)
const CLASP_COLOR: Color = Color(0.95, 0.78, 0.3)


func _draw() -> void:
	draw_rect(Rect2(-14.0, -10.0, 28.0, 20.0), COVER_COLOR)
	draw_rect(Rect2(-11.0, -7.0, 22.0, 14.0), PAGES_COLOR)
	draw_rect(Rect2(-2.0, -10.0, 4.0, 20.0), CLASP_COLOR)
