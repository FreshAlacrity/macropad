# @todo condense these more
def all_faces():
    return [
        "  o  ",
        "  O  ",
        "∩ _ ∩",  # 2
        "O ◡ O",
        "- ◡ -",
        "• _ •",
        "- _ -",
        "> _ >",
        "< _ <",  # 8
        "> _ <",
        "X _ X",  # 10
        "° _ °",
        "- o -",
        "- w -",
        "- θ -",  # 14
        "¬ ◡ ¬",
        "¬ _ ¬",
        "υ _ υ",  # 17
        "џ _ џ",
        "ὺ _ ύ",
        "ὸ _ ό",
        "O Д O",
        "; Д ;",
        "T _ T",  # 23
        "τ _ τ",
        "v _ v",
        "υ _ υ",
        "n _ n",
        "O ω O",
        "ὲ ◡ έ",
        "ὶ ◡ ί",
        "Ξ ◡ Ξ",
        "' o '",
        "∩ _ ∩",
        "- ◡ O",  # 34
        "c(_)  ",
        "⚆ _ ⚆",
        "# _ #",
        "..zZz",
        "..zzZ",
    ]


def tam_tam_faces(mood):
    faces = {
        "egg": {
            "faces": [0, 1], 
            "frames": 10
        },
        "happy": {
            "faces": [3, 4],
            "frames": 4,
        },
        "neutral": {
            "faces": [5, 7, 5, 8, 5, 6],
            "frames": 6,
        },
        "tea": {
            "faces": [2, 35],
            "frames": 6,
        },
        "eating": {
            "faces": [2, 12, 14],
            "frames": 6,
        },
        "sick": {
            "faces": [10, 9],
            "frames": 6,
        },
        "asleep": {
            "faces": [6, 6, 12, 38, 39],
            "frames": 21,
        },
        "sad": {
            "faces": [17, 18, 19],
            "frames": 6,
        },
        "scared": {
            "faces": [11, 21, 22],
            "frames": 4,
        },
        "angry": {
            "faces": [16, 20, 9],
            "frames": 4,
        },
        "hungry": {
            "faces": [24, 9],
            "frames": 4,
        },
        "tired": {
            "faces": [25, 26, 27],
            "frames": 3,
        },
        "sneaky": {
            "faces": [15, 28, 29, 30],
            "frames": 4,
        },
        "random": {
            "faces": [31, 32, 33, 34],
            "frames": 1,
        },
    }
    return faces[mood]["faces"]
