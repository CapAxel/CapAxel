class_name SimDraft
extends RefCounted
## Le draft « 1 parmi 3 » depuis le roster préparé (GDD §4.1) — tiré du flux
## RNG « draft » exclusivement. Pas encore de pondération de pitié : c'est la
## première itération listée dans le README ; l'accroche est déjà en place.

var roster_ids: Array[String] = []


func _init(p_roster: Array) -> void:
	for entry: Variant in p_roster:
		roster_ids.append(String(entry))


## Trois propositions tirées du roster (doublons permis : c'est ce qui nourrit
## la fusion). La pondération de pitié remplacera ce tirage uniforme.
func draw_three(rng: RandomNumberGenerator) -> Array[String]:
	var offer: Array[String] = []
	for i: int in range(3):
		var index := rng.randi_range(0, roster_ids.size() - 1)
		offer.append(roster_ids[index])
	return offer
