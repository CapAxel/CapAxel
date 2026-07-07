class_name DraftUi
extends CanvasLayer
## Le draft « 1 parmi 3 » : trois pages qui se tournent (bible §2). L'UI émet un
## choix ; main.gd le journalise comme input et la simulation le consomme au tick
## suivant — le clic passe par le même chemin déterministe que le clavier.

signal pick_chosen(index: int)

var _root: CenterContainer
var _cards: Array[PanelContainer] = []
var _name_labels: Array[Label] = []
var _role_labels: Array[Label] = []
var _owned_labels: Array[Label] = []


func _ready() -> void:
	_root = CenterContainer.new()
	_root.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(_root)
	var row := HBoxContainer.new()
	row.add_theme_constant_override("separation", 24)
	_root.add_child(row)
	for i: int in range(3):
		var card := PanelContainer.new()
		card.custom_minimum_size = Vector2(240.0, 180.0)
		var column := VBoxContainer.new()
		column.add_theme_constant_override("separation", 8)
		card.add_child(column)

		var name_label := Label.new()
		name_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		name_label.add_theme_font_size_override("font_size", 20)
		column.add_child(name_label)

		var role_label := Label.new()
		role_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		column.add_child(role_label)

		var owned_label := Label.new()
		owned_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		owned_label.add_theme_color_override("font_color", Color(1.0, 1.0, 1.0, 0.7))
		column.add_child(owned_label)

		var button := Button.new()
		button.text = "Choisir (%d)" % (i + 1)
		button.pressed.connect(_on_pick_pressed.bind(i))
		column.add_child(button)

		row.add_child(card)
		_cards.append(card)
		_name_labels.append(name_label)
		_role_labels.append(role_label)
		_owned_labels.append(owned_label)
	visible = false


func show_offer(offer: Array[String], sim: SimWorld) -> void:
	for i: int in range(3):
		var figure_id := offer[i]
		var data := sim.figure_data(figure_id)
		_name_labels[i].text = String(data.get("nom", figure_id))
		_role_labels[i].text = String(data.get("role", "?"))
		var t1 := sim.owned_count(figure_id, 1)
		var t2 := sim.owned_count(figure_id, 2)
		var owned_text := "Possédé : %d T1" % t1
		if t2 > 0:
			owned_text += " · %d T2" % t2
		if t1 == 2:
			owned_text += "  → fusion !"
		_owned_labels[i].text = owned_text
	visible = true


func hide_offer() -> void:
	visible = false


func _on_pick_pressed(index: int) -> void:
	pick_chosen.emit(index)
