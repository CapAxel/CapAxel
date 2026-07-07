extends Node
## RngService — autoload. Flux de hasard nommés et seedés séparément (annexe systèmes §3.6).
## Consommer du hasard dans un flux ne décale JAMAIS les autres : le draft reste
## identique pour tous à seed égale, quel que soit le déroulé du combat.
## La simulation ne touche jamais au RNG global de Godot (randi/randf interdits).

const STREAM_NAMES: Array[String] = ["draft", "spawns", "degats"]

var run_seed: int = 0
var _streams: Dictionary = {}


func init_run(p_seed: int) -> void:
	run_seed = p_seed
	_streams.clear()
	for stream_name: String in STREAM_NAMES:
		var rng := RandomNumberGenerator.new()
		# Dérivation stable : seed de run combinée au nom du flux.
		rng.seed = hash(str(p_seed) + ":" + stream_name)
		_streams[stream_name] = rng


func stream(stream_name: String) -> RandomNumberGenerator:
	assert(_streams.has(stream_name), "Flux RNG inconnu : " + stream_name)
	return _streams[stream_name]
