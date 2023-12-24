# ControlToolAssist
Basic control macro tool

Current State (semi functional):
- Records input
- Save/load input
- Playback through virtual Xbox360 controller
- No limitations on GUI (easy to break if you dont press right buttons)
- No ability to modify saved macros

Intended features will be to record controller input and then be able to replay, modify and save recorded input or even create input without any previous. I am making this to be used with Skate 3 but
it will not be limited to any game as it will just record and repeat detected controller input. Later on i want to add a feature where it simalteneously records you play the game while you press the inputs so you can more easily analyse how your inputs effect your character in game.

utils.py was stolen from [TensorKart](https://github.com/kevinhughes27/TensorKart/blob/master/utils.py) (it's now in the controller file, only the controller reader).
